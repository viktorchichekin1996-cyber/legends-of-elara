"""Бизнес-логика боевой системы с интеграцией экипировки, квестов и памяти."""
import asyncio
import random
import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import get_gpt_client, get_prompt_cache
from app.ai.prompts import COMBAT_NARRATIVE_PROMPT
from app.models.character import Character
from app.models.combat import Enemy, CombatSession
from app.models.location import Location
from app.schemas.combat import (
    CombatActionResult, CombatStateResponse, CombatLogEntry
)
from app.services.character_service import apply_level_up
from app.services.inventory_service import get_equipped_items, calculate_equipment_modifiers
from app.utils.calculations import calculate_modifier, clamp_value, check_level_up
from app.utils.dice import roll_d20, roll_damage, check_success, calculate_dc

# Этап 9: Интеграция квестов и памяти
from app.services.quest_service import update_quest_progress
from app.services.memory_service import add_memory

logger = logging.getLogger(__name__)

# Константы боя
BASE_AC = 10
BASE_DC = 10
CRIT_MULTIPLIER = 2
FLEE_DC_BASE = 15
BROKEN_WEAPON_PENALTY = 0.5


async def get_active_combat(session: AsyncSession, character_id: str) -> Optional[CombatSession]:
    result = await session.execute(
        select(CombatSession).where(
            CombatSession.character_id == character_id,
            CombatSession.is_active == True
        )
    )
    return result.scalar_one_or_none()


async def start_combat(
    session: AsyncSession,
    character_id: str,
    enemy_id: Optional[str] = None
) -> CombatSession:
    existing = await get_active_combat(session, character_id)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Бой уже активен")
    
    char_result = await session.execute(select(Character).where(Character.id == character_id))
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    if enemy_id:
        enemy_result = await session.execute(select(Enemy).where(Enemy.id == enemy_id))
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(status_code=404, detail="Enemy not found")
    else:
        enemy_result = await session.execute(
            select(Enemy)
            .where(and_(Enemy.level >= max(1, character.level - 2), Enemy.level <= character.level + 2))
            .order_by(func.random()).limit(1)
        )
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No suitable enemies found")
    
    combat = CombatSession(
        character_id=character.id,
        enemy_id=enemy.id,
        enemy_name=enemy.name,
        enemy_hp_current=enemy.hp,
        enemy_hp_max=enemy.hp,
        enemy_stats={
            "strength": enemy.strength, "agility": enemy.agility, "intelligence": enemy.intelligence,
            "damage_min": enemy.damage_min, "damage_max": enemy.damage_max, "armor": enemy.armor,
            "dodge_chance": enemy.dodge_chance, "crit_chance": enemy.crit_chance,
        },
        is_active=True, current_turn=1,
        combat_log=[f"Бой начался! На вас напал {enemy.name}!"],
    )
    session.add(combat)
    await session.flush()
    await session.refresh(combat)
    return combat


def calculate_player_attack_dc(character: Character) -> int:
    return BASE_DC + calculate_modifier(character.agility)

def calculate_enemy_attack_dc(enemy_stats: dict) -> int:
    return BASE_DC + calculate_modifier(enemy_stats.get("agility", 10))

async def calculate_player_armor(session: AsyncSession, character_id: str) -> int:
    equipped = await get_equipped_items(session, character_id)
    mods = calculate_equipment_modifiers(equipped)
    return int(mods.get("armor", 0))

async def calculate_player_weapon_damage(session: AsyncSession, character: Character, is_critical: bool = False) -> tuple[int, int]:
    equipped = await get_equipped_items(session, str(character.id))
    mods = calculate_equipment_modifiers(equipped)
    base_min = character.strength // 2
    base_max = character.strength
    weapon_dmg_min = int(mods.get("damage_min", 0))
    weapon_dmg_max = int(mods.get("damage_max", 0))
    total_min = base_min + weapon_dmg_min
    total_max = base_max + weapon_dmg_max
    for slot, eq in equipped.items():
        if slot == "weapon" and eq.inventory.durability is not None and eq.inventory.durability <= 0:
            total_min = int(total_min * BROKEN_WEAPON_PENALTY)
            total_max = int(total_max * BROKEN_WEAPON_PENALTY)
            break
    return max(0, total_min), max(total_min, total_max)

def calculate_damage(attacker_str: int, defender_armor: int, min_dmg: int, max_dmg: int, is_critical: bool = False) -> int:
    str_mod = calculate_modifier(attacker_str)
    base_dmg = roll_damage(min_dmg, max_dmg, str_mod, is_critical)
    return max(0, base_dmg - defender_armor)

async def generate_combat_narrative(character: Character, enemy_name: str, action_type: str, result_desc: str, damage: int, enemy_hp: int, enemy_max: int) -> str:
    try:
        client = get_gpt_client()
        cache = get_prompt_cache()
        prompt_text = COMBAT_NARRATIVE_PROMPT.format(
            char_name=character.name, char_class=character.character_class, char_level=character.level,
            enemy_name=enemy_name, action_type=action_type, result_desc=result_desc,
            damage=damage if damage else 0, enemy_hp=enemy_hp, enemy_max=enemy_max,
            char_hp=character.hp_current, char_max=character.hp_max
        )
        messages = [{"role": "user", "text": prompt_text}]
        prompt_hash = cache.hash_prompt(messages)
        cached_response = await cache.get(prompt_hash)
        if cached_response:
            return cached_response.strip()
        response = await asyncio.wait_for(client.generate(messages, temperature=0.8, max_tokens=100), timeout=3.0)
        await cache.set(prompt_hash, response.strip())
        return response.strip()
    except Exception as e:
        logger.warning(f"AI narrative generation failed: {e}")
        return f"{result_desc} (Урон: {damage if damage else 0})"

async def process_player_attack(session: AsyncSession, combat: CombatSession, character: Character) -> CombatActionResult:
    enemy_stats = combat.enemy_stats
    attack_mod = calculate_modifier(character.strength)
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_enemy_attack_dc(enemy_stats)
    
    if attack_roll == 1:
        log_entry = "Вы промахнулись критически!"
        ai_description = await generate_combat_narrative(character, combat.enemy_name, "player_attack", log_entry, 0, combat.enemy_hp_current, combat.enemy_hp_max)
        combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="player", action="attack", description=ai_description, is_miss=True).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True, is_critical=False)
    
    if is_crit:
        log_entry = "Критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = "Вы попали! "
    else:
        log_entry = "Вы промахнулись. "
        ai_description = await generate_combat_narrative(character, combat.enemy_name, "player_attack", log_entry, 0, combat.enemy_hp_current, combat.enemy_hp_max)
        combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="player", action="attack", description=ai_description, is_miss=True).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    min_dmg, max_dmg = await calculate_player_weapon_damage(session, character, is_crit)
    enemy_armor = enemy_stats.get("armor", 0)
    damage = calculate_damage(character.strength, enemy_armor, min_dmg, max_dmg, is_crit)
    combat.enemy_hp_current = max(0, combat.enemy_hp_current - damage)
    log_entry += f"Урон: {damage}. HP врага: {combat.enemy_hp_current}/{combat.enemy_hp_max}"
    
    ai_description = await generate_combat_narrative(character, combat.enemy_name, "player_attack", log_entry, damage, combat.enemy_hp_current, combat.enemy_hp_max)
    combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="player", action="attack", description=ai_description, damage=damage, is_critical=is_crit).model_dump())
    
    if combat.enemy_hp_current <= 0:
        return await finish_combat(session, combat, character, victory=True)
    
    await session.flush()
    return CombatActionResult(success=True, message=log_entry, enemy_damage_taken=damage, is_critical=is_crit)

async def process_enemy_turn(session: AsyncSession, combat: CombatSession, character: Character) -> CombatActionResult:
    enemy_stats = combat.enemy_stats
    attack_mod = calculate_modifier(enemy_stats.get("strength", 10))
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_player_attack_dc(character)
    
    if attack_roll == 1:
        log_entry = f"{combat.enemy_name} промахнулся критически!"
        ai_description = await generate_combat_narrative(character, combat.enemy_name, "enemy_attack", log_entry, 0, combat.enemy_hp_current, combat.enemy_hp_max)
        combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="enemy", action="attack", description=ai_description, is_miss=True).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    if is_crit:
        log_entry = f"{combat.enemy_name} наносит критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = f"{combat.enemy_name} атакует! "
    else:
        log_entry = f"{combat.enemy_name} промахнулся. "
        ai_description = await generate_combat_narrative(character, combat.enemy_name, "enemy_attack", log_entry, 0, combat.enemy_hp_current, combat.enemy_hp_max)
        combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="enemy", action="attack", description=ai_description, is_miss=True).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    player_armor = await calculate_player_armor(session, str(character.id))
    damage = calculate_damage(enemy_stats.get("strength", 10), player_armor, enemy_stats.get("damage_min", 1), enemy_stats.get("damage_max", 5), is_crit)
    character.hp_current = max(0, character.hp_current - damage)
    log_entry += f"Урон: {damage}. Ваше HP: {character.hp_current}/{character.hp_max}"
    
    ai_description = await generate_combat_narrative(character, combat.enemy_name, "enemy_attack", log_entry, damage, combat.enemy_hp_current, combat.enemy_hp_max)
    combat.combat_log.append(CombatLogEntry(turn=combat.current_turn, actor="enemy", action="attack", description=ai_description, damage=damage, is_critical=is_crit).model_dump())
    
    if character.hp_current <= 0:
        return await finish_combat(session, combat, character, victory=False)
    
    combat.current_turn += 1
    await session.flush()
    return CombatActionResult(success=True, message=log_entry, player_damage_taken=damage, is_critical=is_crit)

async def finish_combat(session: AsyncSession, combat: CombatSession, character: Character, victory: bool) -> CombatActionResult:
    """Завершает бой: удаляет запись, начисляет награды, обновляет квесты/память."""
    if victory:
        xp_gain = 10
        gold_gain = random.randint(5, 15)
        character.experience += xp_gain
        character.gold += gold_gain
        leveled_up, new_level = check_level_up(character.experience, character.level)
        if leveled_up:
            character.level = new_level
            await apply_level_up(character)
        combat.result = "victory"
        combat.rewards = {"xp": xp_gain, "gold": gold_gain}
        message = f"🎉 Победа! +{xp_gain} XP, +{gold_gain} золота"
        if leveled_up:
            message += f" | Уровень повышен до {new_level}!"
        
        # === ЭТАП 9.2: Хук прогресса квеста ===
        try:
            await update_quest_progress(session, str(character.id), "kill", combat.enemy_name, 1)
        except Exception as e:
            logger.error(f"Quest progress hook failed: {e}")
            await session.rollback()
        
        # === ЭТАП 9.4: Память о победе ===
        try:
            importance = 5 if combat.enemy_stats.get("level", 1) >= character.level + 2 else 4
            if importance >= 4:
                await add_memory(
                    session, str(character.id), "boss_defeat" if importance == 5 else "unique_event",
                    f"Победа над {combat.enemy_name}",
                    f"Герой одержал победу. Награда: {xp_gain} XP, {gold_gain} золота.",
                    importance, ["combat", "victory", combat.enemy_name.lower()],
                    {"enemy_name": combat.enemy_name, "enemy_level": combat.enemy_stats.get("level", 1), "xp_gained": xp_gain, "gold_gained": gold_gain}
                )
        except Exception as e:
            logger.error(f"Memory hook failed: {e}")
            await session.rollback()
    else:
        character.gold = max(0, character.gold - 10)
        character.fatigue = clamp_value(character.fatigue + 20, 0, 100)
        combat.result = "defeat"
        message = "💀 Поражение... Вы потеряли 10 золота и устали."
        try:
            if character.hp_max > 50:
                await add_memory(
                    session, str(character.id), "unique_event",
                    f"Поражение от {combat.enemy_name}",
                    f"Герой потерпел поражение. Потеряно 10 золота.",
                    4, ["combat", "defeat", combat.enemy_name.lower()],
                    {"enemy_name": combat.enemy_name, "gold_lost": 10}
                )
        except Exception as e:
            logger.error(f"Defeat memory hook failed: {e}")
            await session.rollback()
    
    combat.ended_at = datetime.now()
    character.stamina_current = clamp_value(character.stamina_current + 10, 0, character.stamina_max)
    
    # === ФИКС: Удаляем запись боя вместо обновления is_active=False ===
    await session.execute(delete(CombatSession).where(CombatSession.id == combat.id))
    await session.flush()
    
    return CombatActionResult(success=True, message=message, battle_ended=True, battle_result=combat.result, rewards=combat.rewards if victory else None)

async def get_combat_state(session: AsyncSession, combat: CombatSession, character: Character) -> CombatStateResponse:
    return CombatStateResponse(
        combat_session_id=combat.id, enemy_name=combat.enemy_name, enemy_level=combat.enemy_stats.get("level", 1),
        enemy_hp_current=combat.enemy_hp_current, enemy_hp_max=combat.enemy_hp_max,
        player_hp_current=character.hp_current, player_hp_max=character.hp_max,
        player_mana_current=character.mana_current, player_mana_max=character.mana_max,
        current_turn=combat.current_turn, is_player_turn=True,
        combat_log=[CombatLogEntry(**(entry if isinstance(entry, dict) else {"turn": 1, "actor": "system", "action": "log", "description": str(entry), "is_critical": False, "is_miss": False})) for entry in combat.combat_log]
    )
