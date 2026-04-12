"""Бизнес-логика операций с персонажем."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.character import Character
from app.models.location import Location
from app.models.enums import CHARACTER_STATUS
from app.utils.constants import CLASS_STARTING_STATS, STARTING_LOCATION_NAME, LEVEL_UP_BONUSES
from app.utils.calculations import calculate_modifier, clamp_value, check_level_up, calculate_effective_stat
from app.schemas.character import CharacterCreateRequest, CharacterStatsResponse, CharacterResourcesResponse
from app.services.inventory_service import get_equipped_items, calculate_equipment_modifiers

async def validate_character_name(session: AsyncSession, name: str, exclude_id: str = None) -> bool:
    stmt = select(Character).where(Character.name == name)
    if exclude_id:
        stmt = stmt.where(Character.id != exclude_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is None

async def get_starting_location(session: AsyncSession) -> Location:
    result = await session.execute(select(Location).where(Location.name == STARTING_LOCATION_NAME))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=500, detail="Starting location not found")
    return location

async def calculate_character_stats(session: AsyncSession, character: Character) -> tuple[CharacterStatsResponse, int, int, int]:
    """Рассчитывает характеристики с учётом экипировки. Возвращает (stats, hp_max, mana_max, stamina_max)."""
    equipped = await get_equipped_items(session, str(character.id))
    eq_mods = calculate_equipment_modifiers(equipped)
    
    strength = character.strength + int(eq_mods.get("strength", 0))
    agility = character.agility + int(eq_mods.get("agility", 0))
    intelligence = character.intelligence + int(eq_mods.get("intelligence", 0))
    
    strength_mod = calculate_modifier(strength)
    agility_mod = calculate_modifier(agility)
    intelligence_mod = calculate_modifier(intelligence)
    
    hp_max = character.hp_max + int(eq_mods.get("hp_max", 0))
    mana_max = character.mana_max + int(eq_mods.get("mana_max", 0))
    stamina_max = character.stamina_max + int(eq_mods.get("stamina_max", 0))
    
    return CharacterStatsResponse(
        strength=character.strength, agility=character.agility, intelligence=character.intelligence,
        strength_mod=strength_mod, agility_mod=agility_mod, intelligence_mod=intelligence_mod,
        strength_effective=strength, agility_effective=agility, intelligence_effective=intelligence,
    ), hp_max, mana_max, stamina_max

def calculate_character_resources(character: Character, hp_max: int, mana_max: int, stamina_max: int, inventory_used: int = None) -> CharacterResourcesResponse:
    return CharacterResourcesResponse(
        hp_current=character.hp_current, hp_max=hp_max,
        mana_current=character.mana_current, mana_max=mana_max,
        stamina_current=character.stamina_current, stamina_max=stamina_max,
        fatigue=character.fatigue, gold=character.gold,
        inventory_slots=character.inventory_slots, inventory_slots_used=inventory_used,
    )

def check_action_allowed(character: Character) -> tuple[bool, str]:
    if character.fatigue >= 80:
        return False, f"Слишком высокая усталость ({character.fatigue}%). Отдохните."
    if character.hp_current <= 0:
        return False, "Персонаж без сознания."
    return True, "OK"

async def create_character(session: AsyncSession, user_id: str, request: CharacterCreateRequest) -> Character:
    if not await validate_character_name(session, request.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Персонаж с таким именем уже существует")
    starting_location = await get_starting_location(session)
    class_stats = CLASS_STARTING_STATS.get(request.character_class)
    if not class_stats:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный класс персонажа")
    character = Character(
        user_id=user_id, name=request.name, character_class=request.character_class,
        current_location_id=starting_location.id,
        strength=class_stats["strength"], agility=class_stats["agility"], intelligence=class_stats["intelligence"],
        hp_current=class_stats["hp_max"], hp_max=class_stats["hp_max"],
        mana_current=class_stats["mana_max"], mana_max=class_stats["mana_max"],
        stamina_current=class_stats["stamina_max"], stamina_max=class_stats["stamina_max"],
        level=1, experience=0, status="alive", fatigue=0, gold=0, inventory_slots=10,
    )
    session.add(character)
    await session.flush()
    await session.refresh(character)
    return character

async def apply_level_up(character: Character) -> dict:
    stats_increased = {}
    for stat, bonus in LEVEL_UP_BONUSES.items():
        if hasattr(character, stat):
            old_value = getattr(character, stat)
            new_value = old_value + bonus
            setattr(character, stat, new_value)
            stats_increased[stat] = {"old": old_value, "new": new_value}
    character.hp_current = character.hp_max
    character.mana_current = character.mana_max
    character.stamina_current = character.stamina_max
    character.fatigue = 0
    return stats_increased
