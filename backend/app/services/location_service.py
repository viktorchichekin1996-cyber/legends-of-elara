from typing import Optional
import random
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.location import Location, LocationConnection
from app.models.character import Character
from app.models.combat import Enemy, CombatSession
from app.utils.constants import FATIGUE_WARNING, FATIGUE_ACTION_BLOCK
from app.utils.calculations import clamp_value
from app.schemas.location import LocationResponse, NeighborLocationResponse, MoveResponse

# Вероятности случайных встреч по типам локаций
ENCOUNTER_PROBABILITIES = {
    "city": 0.0,
    "forest": 0.3,
    "road": 0.1,
    "dungeon": 0.7,
    "cave": 0.5,
    "mountain": 0.4,
    "swamp": 0.6,
}

BASE_FATIGUE_COST = 5

async def get_location_by_id(session: AsyncSession, location_id: str) -> Location:
    result = await session.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

async def get_current_location(session: AsyncSession, character_id: str) -> Location:
    result = await session.execute(
        select(Location)
        .join(Character, Character.current_location_id == Location.id)
        .where(Character.id == character_id)
    )
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Current location not found")
    return location

async def get_neighbors(session: AsyncSession, location_id: str) -> list[Location]:
    result = await session.execute(
        select(Location)
        .join(LocationConnection, Location.id == LocationConnection.to_location_id)
        .where(LocationConnection.from_location_id == location_id)
    )
    return result.scalars().all()

async def validate_move(
    session: AsyncSession,
    character_id: str,
    target_location_id: str
) -> tuple[Character, Location, LocationConnection]:
    char_result = await session.execute(select(Character).where(Character.id == character_id))
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    target = await get_location_by_id(session, target_location_id)
    
    conn_result = await session.execute(
        select(LocationConnection).where(
            and_(
                LocationConnection.from_location_id == character.current_location_id,
                LocationConnection.to_location_id == target_location_id
            )
        )
    )
    connection = conn_result.scalar_one_or_none()
    if not connection:
        raise HTTPException(status_code=400, detail="Cannot move to this location directly")
    
    if character.fatigue >= FATIGUE_ACTION_BLOCK:
        raise HTTPException(status_code=400, detail=f"Too fatigued ({character.fatigue}%). Rest first.")
    
    return character, target, connection

def calculate_fatigue_cost(connection: LocationConnection, character: Character) -> int:
    base = BASE_FATIGUE_COST
    difficulty_bonus = connection.travel_difficulty * 2
    level_penalty = max(0, connection.travel_difficulty - character.level) * 3
    total = base + difficulty_bonus + level_penalty
    return clamp_value(total, 1, 50)

async def check_random_encounter(
    session: AsyncSession,
    location: Location,
    character: Character
) -> Optional[dict]:
    probability = ENCOUNTER_PROBABILITIES.get(location.location_type, 0.1)
    
    if random.random() > probability:
        return None
    
    enemy_result = await session.execute(
        select(Enemy)
        .where(
            and_(
                Enemy.level >= max(1, character.level - 2),
                Enemy.level <= character.level + 2
            )
        )
        .order_by(Enemy.level)
        .limit(1)
    )
    enemy = enemy_result.scalar_one_or_none()
    
    if not enemy:
        return None
    
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
        },
        is_active=True,
        current_turn=1,
        combat_log=[f"Внезапная встреча с {enemy.name}!"],
    )
    session.add(combat)
    await session.flush()
    
    return {
        "type": "combat",
        "enemy_name": enemy.name,
        "enemy_level": enemy.level,
        "combat_session_id": str(combat.id),
        "message": f"На вас напал {enemy.name}!"
    }

async def generate_location_description(
    location: Location,
    character_class: str,
    character_level: int
) -> str:
    templates = {
        "city": f"Город {location.name} встречает вас шумом и суетой. Здесь можно найти торговцев и таверну.",
        "forest": f"Лес {location.name} окутан таинственной тишиной. Тени шевелятся между древними деревьями.",
        "road": f"Пыльная дорога {location.name} ведёт через {location.region}. Вдали виднеются силуэты путников.",
        "dungeon": f"Мрачный вход в {location.name} зияет темнотой. Оттуда доносится эхо чьих-то шагов.",
        "cave": f"Пещера {location.name} хранит секреты древних времён. Сталактиты сверкают в тусклом свете.",
        "mountain": f"Горы {location.name} возвышаются над облаками. Ветер свистит в ущельях.",
        "swamp": f"Болото {location.name} окутано туманом. Где-то вдалеке квакают невидимые лягушки.",
    }
    return templates.get(location.location_type, f"Вы находитесь в {location.name}.")

async def move_character(
    session: AsyncSession,
    character_id: str,
    target_location_id: str
) -> MoveResponse:
    character, target, connection = await validate_move(session, character_id, target_location_id)
    
    fatigue_cost = calculate_fatigue_cost(connection, character)
    character.fatigue = clamp_value(character.fatigue + fatigue_cost, 0, 100)
    
    character.current_location_id = target_location_id
    
    encounter = await check_random_encounter(session, target, character)
    
    if not target.ai_description_generated:
        target.description = await generate_location_description(target, character.character_class, character.level)
        target.ai_description_generated = True
    
    await session.flush()
    
    message = f"Вы прибыли в {target.name}."
    if character.fatigue >= FATIGUE_WARNING:
        message += f" Вы очень устали ({character.fatigue}%)."
    
    return MoveResponse(
        success=True,
        message=message,
        new_location=LocationResponse.model_validate(target),
        fatigue_added=fatigue_cost,
        encounter=encounter
    )
