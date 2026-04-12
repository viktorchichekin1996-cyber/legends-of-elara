"""Бизнес-логика боевой системы с интеграцией экипировки."""
import asyncio
import random
import logging
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, and_, func
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

logger = logging.getLogger(__name__)

# Константы боя
BASE_AC = 10  # Базовый класс брони
BASE_DC = 10  # Базовая сложность проверки
CRIT_MULTIPLIER = 2  # Множитель урона при крите
FLEE_DC_BASE = 15  # Базовая сложность побега
BROKEN_WEAPON_PENALTY = 0.5  # Штраф урона для сломанного оружия


async def get_active_combat(session: AsyncSession, character_id: str) -> Optional[CombatSession]:
    """Получает активную боевую сессию персонажа."""
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
    """Инициализирует новый бой."""
    # Проверяем, нет ли уже активного боя
    existing = await get_active_combat(session, character_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бой уже активен"
        )
    
    # Получаем персонажа
    char_result = await session.execute(
        select(Character).where(Character.id == character_id)
    )
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Получаем или выбираем врага
    if enemy_id:
        enemy_result = await session.execute(
            select(Enemy).where(Enemy.id == enemy_id)
        )
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(status_code=404, detail="Enemy not found")
    else:
        # Выбираем случайного врага подходящего уровня
        enemy_result = await session.execute(
            select(Enemy)
            .where(
                and_(
                    Enemy.level >= max(1, character.level - 2),
                    Enemy.level <= character.level + 2
                )
            )
            .order_by(func.random())
            .limit(1)
        )
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No suitable enemies found"
            )
    
    # Создаём боевую сессию
    combat = CombatSession(
        character_id=character.id,
        enemy_id=enemy.id,
        enemy_name=enemy.name,
        enemy_hp_current=enemy.hp,
        enemy_hp_max=enemy.hp,
        enemy_stats={
            "strength": enemy.strength,
            "agility": enemy.agility,
            "intelligence": enemy.intelligence,
            "damage_min": enemy.damage_min,
            "damage_max": enemy.damage_max,
            "armor": enemy.armor,
            "dodge_chance": enemy.dodge_chance,
            "crit_chance": enemy.crit_chance,
        },
        is_active=True,
        current_turn=1,
        combat_log=[f"Бой начался! На вас напал {enemy.name}!"],
    )
    
    session.add(combat)
    await session.flush()
    await session.refresh(combat)
    
    return combat


def calculate_player_attack_dc(character: Character) -> int:
    """Рассчитывает сложность атаки игрока."""
    enemy_agi_mod = calculate_modifier(character.agility)
    return BASE_DC + enemy_agi_mod


def calculate_enemy_attack_dc(enemy_stats: dict) -> int:
    """Рассчитывает сложность атаки врага."""
    return BASE_DC + calculate_modifier(enemy_stats.get("agility", 10))


async def calculate_player_armor(session: AsyncSession, character_id: str) -> int:
    """8.4 Рассчитывает броню игрока на основе экипированной брони/аксессуаров."""
    equipped = await get_equipped_items(session, character_id)
    mods = calculate_equipment_modifiers(equipped)
    return int(mods.get("armor", 0))


async def calculate_player_weapon_damage(
    session: AsyncSession, 
    character: Character, 
    is_critical: bool = False
) -> tuple[int, int]:
    """8.4 Возвращает (min_dmg, max_dmg) с учётом экипированного оружия и прочности."""
    equipped = await get_equipped_items(session, str(character.id))
    mods = calculate_equipment_modifiers(equipped)
    
    # Базовый урон от силы
    base_min = character.strength // 2
    base_max = character.strength
    
    # Модификаторы от оружия
    weapon_dmg_min = int(mods.get("damage_min", 0))
    weapon_dmg_max = int(mods.get("damage_max", 0))
    
    total_min = base_min + weapon_dmg_min
    total_max = base_max + weapon_dmg_max
    
    # Проверка на сломанное оружие (штраф к урону)
    for slot, eq in equipped.items():
        if slot == "weapon" and eq.inventory.durability is not None:
            if eq.inventory.durability <= 0:
                total_min = int(total_min * BROKEN_WEAPON_PENALTY)
                total_max = int(total_max * BROKEN_WEAPON_PENALTY)
                break
    
    return max(0, total_min), max(total_min, total_max)


def calculate_damage(
    attacker_str: int,
    defender_armor: int,
    min_dmg: int,
    max_dmg: int,
    is_critical: bool = False
) -> int:
    """Рассчитывает итоговый урон с учётом брони и крита."""
    str_mod = calculate_modifier(attacker_str)
    base_dmg = roll_damage(min_dmg, max_dmg, str_mod, is_critical)
    return max(0, base_dmg - defender_armor)


async def generate_combat_narrative(
    character: Character,
    enemy_name: str,
    action_type: str,
    result_desc: str,
    damage: int,
    enemy_hp: int,
    enemy_max: int
) -> str:
    """Генерирует атмосферное описание хода через ИИ."""
    try:
        client = get_gpt_client()
        cache = get_prompt_cache()
        
        prompt_text = COMBAT_NARRATIVE_PROMPT.format(
            char_name=character.name,
            char_class=character.character_class,
            char_level=character.level,
            enemy_name=enemy_name,
            action_type=action_type,
            result_desc=result_desc,
            damage=damage if damage else 0,
            enemy_hp=enemy_hp,
            enemy_max=enemy_max,
            char_hp=character.hp_current,
            char_max=character.hp_max
        )
        
        messages = [{"role": "user", "text": prompt_text}]
        prompt_hash = cache.hash_prompt(messages)
        
        # Проверяем кэш
        cached_response = await cache.get(prompt_hash)
        if cached_response:
            return cached_response.strip()
        
        # Запрос к ИИ с таймаутом
        response = await asyncio.wait_for(
            client.generate(messages, temperature=0.8, max_tokens=100),
            timeout=3.0
        )
        
        # Кэшируем результат
        await cache.set(prompt_hash, response.strip())
        return response.strip()
        
    except Exception as e:
        logger.warning(f"AI narrative generation failed: {e}")
        return f"{result_desc} (Урон: {damage if damage else 0})"


async def process_player_attack(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatActionResult:
    """Обрабатывает атаку игрока с учётом экипировки."""
    enemy_stats = combat.enemy_stats
    
    # Бросок атаки
    attack_mod = calculate_modifier(character.strength)
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_enemy_attack_dc(enemy_stats)
    
    # Проверка попадания
    if attack_roll == 1:
        log_entry = "Вы промахнулись критически!"
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="player_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="player",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(
            success=True,
            message=log_entry,
            is_miss=True,
            is_critical=False
        )
    
    if is_crit:
        log_entry = "Критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = "Вы попали! "
    else:
        log_entry = "Вы промахнулись. "
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="player_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="player",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    # Расчёт урона с учётом экипировки
    min_dmg, max_dmg = await calculate_player_weapon_damage(session, character, is_crit)
    enemy_armor = enemy_stats.get("armor", 0)
    
    damage = calculate_damage(
        attacker_str=character.strength,
        defender_armor=enemy_armor,
        min_dmg=min_dmg,
        max_dmg=max_dmg,
        is_critical=is_crit
    )
    
    # Применение урона
    combat.enemy_hp_current = max(0, combat.enemy_hp_current - damage)
    
    log_entry += f"Урон: {damage}. HP врага: {combat.enemy_hp_current}/{combat.enemy_hp_max}"
    
    # Генерация ИИ описания
    ai_description = await generate_combat_narrative(
        character=character,
        enemy_name=combat.enemy_name,
        action_type="player_attack",
        result_desc=log_entry,
        damage=damage,
        enemy_hp=combat.enemy_hp_current,
        enemy_max=combat.enemy_hp_max
    )
    
    combat.combat_log.append(CombatLogEntry(
        turn=combat.current_turn,
        actor="player",
        action="attack",
        description=ai_description,
        damage=damage,
        is_critical=is_crit
    ).model_dump())
    
    # Проверка победы
    if combat.enemy_hp_current <= 0:
        return await finish_combat(session, combat, character, victory=True)
    
    await session.flush()
    return CombatActionResult(
        success=True,
        message=log_entry,
        enemy_damage_taken=damage,
        is_critical=is_crit
    )


async def process_enemy_turn(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatActionResult:
    """Обрабатывает ход врага с учётом брони персонажа из экипировки."""
    enemy_stats = combat.enemy_stats
    
    # Логика врага: всегда атакует
    attack_mod = calculate_modifier(enemy_stats.get("strength", 10))
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_player_attack_dc(character)
    
    if attack_roll == 1:
        log_entry = f"{combat.enemy_name} промахнулся критически!"
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="enemy_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="enemy",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    if is_crit:
        log_entry = f"{combat.enemy_name} наносит критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = f"{combat.enemy_name} атакует! "
    else:
        log_entry = f"{combat.enemy_name} промахнулся. "
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="enemy_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="enemy",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    # Расчёт урона с учётом брони из экипировки
    player_armor = await calculate_player_armor(session, str(character.id))
    
    damage = calculate_damage(
        attacker_str=enemy_stats.get("strength", 10),
        defender_armor=player_armor,
        min_dmg=enemy_stats.get("damage_min", 1),
        max_dmg=enemy_stats.get("damage_max", 5),
        is_critical=is_crit
    )
    
    # Применение урона персонажу
    character.hp_current = max(0, character.hp_current - damage)
    
    log_entry += f"Урон: {damage}. Ваше HP: {character.hp_current}/{character.hp_max}"
    
    # Генерация ИИ описания
    ai_description = await generate_combat_narrative(
        character=character,
        enemy_name=combat.enemy_name,
        action_type="enemy_attack",
        result_desc=log_entry,
        damage=damage,
        enemy_hp=combat.enemy_hp_current,
        enemy_max=combat.enemy_hp_max
    )
    
    combat.combat_log.append(CombatLogEntry(
        turn=combat.current_turn,
        actor="enemy",
        action="attack",
        description=ai_description,
        damage=damage,
        is_critical=is_crit
    ).model_dump())
    
    # Проверка поражения
    if character.hp_current <= 0:
        return await finish_combat(session, combat, character, victory=False)
    
    # Следующий ход
    combat.current_turn += 1
    await session.flush()
    
    return CombatActionResult(
        success=True,
        message=log_entry,
        player_damage_taken=damage,
        is_critical=is_crit
    )


async def finish_combat(
    session: AsyncSession,
    combat: CombatSession,
    character: Character,
    victory: bool
) -> CombatActionResult:
    """Завершает бой и начисляет награды."""
    combat.is_active = False
    
    if victory:
        # Награды за победу
        xp_gain = 10
        gold_gain = random.randint(5, 15)
        
        character.experience += xp_gain
        character.gold += gold_gain
        
        # Проверка повышения уровня
        leveled_up, new_level = check_level_up(character.experience, character.level)
        if leveled_up:
            character.level = new_level
            await apply_level_up(character)
        
        combat.result = "victory"
        combat.rewards = {"xp": xp_gain, "gold": gold_gain}
        
        message = f"🎉 Победа! +{xp_gain} XP, +{gold_gain} золота"
        if leveled_up:
            message += f" | Уровень повышен до {new_level}!"
        
    else:
        # Штрафы за поражение
        character.gold = max(0, character.gold - 10)
        character.fatigue = clamp_value(character.fatigue + 20, 0, 100)
        
        combat.result = "defeat"
        message = "💀 Поражение... Вы потеряли 10 золота и устали."
    
    combat.ended_at = datetime.now()
    
    # Восстановление выносливости после боя
    character.stamina_current = clamp_value(
        character.stamina_current + 10,
        0,
        character.stamina_max
    )
    
    await session.flush()
    
    return CombatActionResult(
        success=True,
        message=message,
        battle_ended=True,
        battle_result=combat.result,
        rewards=combat.rewards if victory else None
    )


async def get_combat_state(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatStateResponse:
    """Возвращает текущее состояние боя."""
    return CombatStateResponse(
        combat_session_id=combat.id,
        enemy_name=combat.enemy_name,
        enemy_level=combat.enemy_stats.get("level", 1),
        enemy_hp_current=combat.enemy_hp_current,
        enemy_hp_max=combat.enemy_hp_max,
        player_hp_current=character.hp_current,
        player_hp_max=character.hp_max,
        player_mana_current=character.mana_current,
        player_mana_max=character.mana_max,
        current_turn=combat.current_turn,
        is_player_turn=True,
        combat_log=[
            CombatLogEntry(**(entry if isinstance(entry, dict) else {
                "turn": 1,
                "actor": "system",
                "action": "log",
                "description": str(entry),
                "is_critical": False,
                "is_miss": False
            }))
            for entry in combat.combat_log
        ]
    )