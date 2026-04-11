"""Бизнес-логика операций с персонажем."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.character import Character
from app.models.location import Location
from app.models.enums import CHARACTER_CLASS, CHARACTER_STATUS
from app.utils.constants import CLASS_STARTING_STATS, STARTING_LOCATION_NAME, XP_THRESHOLDS, LEVEL_UP_BONUSES, MAX_FATIGUE, FATIGUE_ACTION_BLOCK
from app.utils.calculations import calculate_modifier, clamp_value, check_level_up, calculate_effective_stat
from app.schemas.character import CharacterCreateRequest, CharacterStatsResponse, CharacterResourcesResponse

async def validate_character_name(session: AsyncSession, name: str, exclude_id: str = None) -> bool:
    """Проверяет уникальность имени персонажа."""
    stmt = select(Character).where(Character.name == name)
    if exclude_id:
        stmt = stmt.where(Character.id != exclude_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is None

async def get_starting_location(session: AsyncSession) -> Location:
    """Получает стартовую локацию по имени."""
    result = await session.execute(
        select(Location).where(Location.name == STARTING_LOCATION_NAME)
    )
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=500, detail="Starting location not found")
    return location

def calculate_character_stats(character: Character) -> CharacterStatsResponse:
    """Рассчитывает характеристики с модификаторами."""
    # Базовые значения
    strength = character.strength
    agility = character.agility
    intelligence = character.intelligence
    
    # Модификаторы
    strength_mod = calculate_modifier(strength)
    agility_mod = calculate_modifier(agility)
    intelligence_mod = calculate_modifier(intelligence)
    
    # Эффективные (пока без экипировки - будет добавлено позже)
    strength_eff = calculate_effective_stat(strength)
    agility_eff = calculate_effective_stat(agility)
    intelligence_eff = calculate_effective_stat(intelligence)
    
    return CharacterStatsResponse(
        strength=strength,
        agility=agility,
        intelligence=intelligence,
        strength_mod=strength_mod,
        agility_mod=agility_mod,
        intelligence_mod=intelligence_mod,
        strength_effective=strength_eff,
        agility_effective=agility_eff,
        intelligence_effective=intelligence_eff,
    )

def calculate_character_resources(character: Character, inventory_used: int = None) -> CharacterResourcesResponse:
    """Рассчитывает ресурсы персонажа."""
    return CharacterResourcesResponse(
        hp_current=character.hp_current,
        hp_max=character.hp_max,
        mana_current=character.mana_current,
        mana_max=character.mana_max,
        stamina_current=character.stamina_current,
        stamina_max=character.stamina_max,
        fatigue=character.fatigue,
        gold=character.gold,
        inventory_slots=character.inventory_slots,
        inventory_slots_used=inventory_used,
    )

def check_action_allowed(character: Character) -> tuple[bool, str]:
    """Проверяет, может ли персонаж выполнять активные действия."""
    if character.fatigue >= FATIGUE_ACTION_BLOCK:
        return False, f"Слишком высокая усталость ({character.fatigue}%). Отдохните."
    if character.hp_current <= 0:
        return False, "Персонаж без сознания."
    return True, "OK"

async def create_character(
    session: AsyncSession,
    user_id: str,
    request: CharacterCreateRequest
) -> Character:
    """Создаёт нового персонажа."""
    # Проверка уникальности имени
    if not await validate_character_name(session, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Персонаж с таким именем уже существует"
        )
    
    # Получение стартовой локации
    starting_location = await get_starting_location(session)
    
    # Получение стартовых характеристик класса
    class_stats = CLASS_STARTING_STATS.get(request.character_class)
    if not class_stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный класс персонажа"
        )
    
    # Создание персонажа
    character = Character(
        user_id=user_id,
        name=request.name,
        character_class=request.character_class,
        current_location_id=starting_location.id,
        # Характеристики класса
        strength=class_stats["strength"],
        agility=class_stats["agility"],
        intelligence=class_stats["intelligence"],
        # Ресурсы
        hp_current=class_stats["hp_max"],
        hp_max=class_stats["hp_max"],
        mana_current=class_stats["mana_max"],
        mana_max=class_stats["mana_max"],
        stamina_current=class_stats["stamina_max"],
        stamina_max=class_stats["stamina_max"],
        # Остальное
        level=1,
        experience=0,
        status=CHARACTER_STATUS.alive,
        fatigue=0,
        gold=0,
        inventory_slots=10,
    )
    
    session.add(character)
    await session.flush()
    await session.refresh(character)
    
    return character

async def apply_level_up(character: Character) -> dict:
    """Применяет повышение уровня персонажа."""
    from app.utils.constants import LEVEL_UP_BONUSES
    
    stats_increased = {}
    
    # Увеличение характеристик
    for stat, bonus in LEVEL_UP_BONUSES.items():
        if hasattr(character, stat):
            old_value = getattr(character, stat)
            new_value = old_value + bonus
            setattr(character, stat, new_value)
            stats_increased[stat] = {"old": old_value, "new": new_value}
    
    # Полное восстановление ресурсов
    character.hp_current = character.hp_max
    character.mana_current = character.mana_max
    character.stamina_current = character.stamina_max
    character.fatigue = 0
    
    return stats_increased
