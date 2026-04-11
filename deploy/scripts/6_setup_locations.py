#!/usr/bin/env python3
"""
Этап 6: Локации и перемещение
Создаёт сервисы, схемы и эндпоинты для системы локаций.
"""
import os
import sys
from pathlib import Path

# === Пути ===
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

if not BACKEND_DIR.is_dir():
    print(f"❌ Ошибка: Директория backend не найдена: {BACKEND_DIR}")
    sys.exit(1)

def write_file(rel_path: str, content: str) -> None:
    """Создаёт файл, если он не существует."""
    full_path = BACKEND_DIR / rel_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    if full_path.exists():
        print(f"⚠️  Пропуск (уже существует): {rel_path}")
        return
    
    full_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"✅ Создан: {rel_path}")

# =============================================================================
# 1. app/schemas/location.py — Pydantic схемы для локаций
# =============================================================================
write_file("app/schemas/location.py", '''
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import uuid
from app.schemas.enums import LocationType

class LocationResponse(BaseModel):
    """Информация о локации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    region: str
    coord_x: int
    coord_y: int
    danger_level: int
    min_level: int
    description: Optional[str] = None
    ai_description_generated: bool
    is_safe: bool
    has_shop: bool
    has_tavern: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

class NeighborLocationResponse(BaseModel):
    """Соседняя локация для навигации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    distance: int
    travel_difficulty: int
    danger_level: int
    is_visited: bool = False
    
    model_config = {"from_attributes": True}

class MoveRequest(BaseModel):
    """Запрос на перемещение."""
    target_location_id: uuid.UUID = Field(..., description="ID целевой локации")

class MoveResponse(BaseModel):
    """Результат перемещения."""
    success: bool
    message: str
    new_location: LocationResponse
    fatigue_added: int
    encounter: Optional[dict] = None  # Информация о случайной встрече
    
    model_config = {"from_attributes": True}
''')

# =============================================================================
# 2. app/services/location_service.py — Бизнес-логика локаций
# =============================================================================
write_file("app/services/location_service.py", '''
"""Бизнес-логика операций с локациями."""
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
    "city": 0.0,      # Города безопасны
    "forest": 0.3,    # Леса опасны
    "road": 0.1,      # Дороги относительно безопасны
    "dungeon": 0.7,   # Подземелья очень опасны
    "cave": 0.5,      # Пещеры опасны
    "mountain": 0.4,  # Горы умеренно опасны
    "swamp": 0.6,     # Болота опасны
}

# Базовая усталость за перемещение
BASE_FATIGUE_COST = 5

async def get_location_by_id(session: AsyncSession, location_id: str) -> Location:
    """Получает локацию по ID."""
    result = await session.execute(
        select(Location).where(Location.id == location_id)
    )
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

async def get_current_location(session: AsyncSession, character_id: str) -> Location:
    """Получает текущую локацию персонажа."""
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
    """Получает список соседних локаций."""
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
    """Валидирует возможность перемещения."""
    # Получаем персонажа
    char_result = await session.execute(
        select(Character).where(Character.id == character_id)
    )
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Получаем целевую локацию
    target = await get_location_by_id(session, target_location_id)
    
    # Проверяем связь
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
        raise HTTPException(
            status_code=400,
            detail="Cannot move to this location directly"
        )
    
    # Проверяем усталость
    if character.fatigue >= FATIGUE_ACTION_BLOCK:
        raise HTTPException(
            status_code=400,
            detail=f"Too fatigued ({character.fatigue}%). Rest first."
        )
    
    return character, target, connection

def calculate_fatigue_cost(connection: LocationConnection, character: Character) -> int:
    """Рассчитывает усталость за перемещение."""
    # Базовая стоимость + сложность пути + штраф за низкий уровень
    base = BASE_FATIGUE_COST
    difficulty_bonus = connection.travel_difficulty * 2
    level_penalty = max(0, connection.danger_level - character.level) * 3
    
    total = base + difficulty_bonus + level_penalty
    return clamp_value(total, 1, 50)

async def check_random_encounter(
    session: AsyncSession,
    location: Location,
    character: Character
) -> Optional[dict]:
    """Проверяет и генерирует случайную встречу."""
    probability = ENCOUNTER_PROBABILITIES.get(location.location_type, 0.1)
    
    if random.random() > probability:
        return None
    
    # Получаем подходящего врага
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
    """Генерирует описание локации через ИИ (заглушка)."""
    # В реальной реализации здесь будет вызов app/ai/client.py
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
    """Выполняет перемещение персонажа."""
    # Валидация
    character, target, connection = await validate_move(
        session, character_id, target_location_id
    )
    
    # Расчёт усталости
    fatigue_cost = calculate_fatigue_cost(connection, character)
    character.fatigue = clamp_value(
        character.fatigue + fatigue_cost,
        0,
        100
    )
    
    # Обновление локации
    character.current_location_id = target_location_id
    
    # Проверка случайной встречи
    encounter = await check_random_encounter(session, target, character)
    
    # Генерация описания при первом посещении
    if not target.ai_description_generated:
        target.description = await generate_location_description(
            target, character.character_class, character.level
        )
        target.ai_description_generated = True
    
    await session.flush()
    
    # Формирование ответа
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
''')

# =============================================================================
# 3. app/api/v1/locations.py — Эндпоинты локаций
# =============================================================================
write_file("app/api/v1/locations.py", '''
"""Эндпоинты управления локациями."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location, LocationConnection
from app.schemas.location import (
    LocationResponse,
    NeighborLocationResponse,
    MoveRequest,
    MoveResponse,
)
from app.services.location_service import (
    get_current_location,
    get_neighbors,
    move_character,
)

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/current", response_model=LocationResponse)
async def get_current_location_endpoint(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    """Получение информации о текущей локации персонажа."""
    result = await db.execute(
        select(Location)
        .join(Character, Character.current_location_id == Location.id)
        .where(Character.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character or location not found"
        )
    
    return LocationResponse.model_validate(location)

@router.get("/neighbors", response_model=list[NeighborLocationResponse])
async def get_neighbor_locations(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[NeighborLocationResponse]:
    """Получение списка доступных соседних локаций."""
    # Получаем текущую локацию персонажа
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    # Получаем соседей
    neighbors = await get_neighbors(db, str(character.current_location_id))
    
    return [
        NeighborLocationResponse(
            id=n.id,
            name=n.name,
            location_type=n.location_type,
            distance=1,
            travel_difficulty=1,
            danger_level=n.danger_level,
            is_visited=False,
        )
        for n in neighbors
    ]

@router.post("/move", response_model=MoveResponse)
async def move_to_location(
    request: MoveRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MoveResponse:
    """Перемещение персонажа в соседнюю локацию."""
    # Получаем персонажа для получения его ID
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    # Выполняем перемещение через сервис
    result = await move_character(
        db,
        str(character.id),
        str(request.target_location_id)
    )
    
    await db.commit()
    
    return result
''')

# =============================================================================
# 4. Обновление app/api/v1/router.py — подключение роутера локаций
# =============================================================================
router_file = BACKEND_DIR / "app" / "api" / "v1" / "router.py"
if router_file.exists():
    content = router_file.read_text(encoding="utf-8")
    if "from app.api.v1.locations import router as locations_router" not in content:
        new_content = content.replace(
            "from app.api.v1.auth import router as auth_router",
            "from app.api.v1.auth import router as auth_router\nfrom app.api.v1.locations import router as locations_router"
        )
        if "v1_router.include_router(character_router)" in new_content:
            new_content = new_content.replace(
                "v1_router.include_router(character_router)",
                "v1_router.include_router(character_router)\nv1_router.include_router(locations_router)"
            )
        router_file.write_text(new_content, encoding="utf-8")
        print("✅ Обновлён: app/api/v1/router.py")
    else:
        print("⚠️  Пропуск: app/api/v1/router.py уже содержит locations_router")

print("\n🎉 Этап 6 (Локации и перемещение) успешно развёрнут!")
print("📂 Созданы файлы:")
print("   • app/schemas/location.py")
print("   • app/services/location_service.py")
print("   • app/api/v1/locations.py")
print("   • app/api/v1/router.py (обновлён)")
print("\n🔗 Новые эндпоинты:")
print("   • GET  /api/v1/locations/current  — текущая локация")
print("   • GET  /api/v1/locations/neighbors — соседние локации")
print("   • POST /api/v1/locations/move     — перемещение")
''')

# =============================================================================
# Запуск
# =============================================================================
if __name__ == "__main__":
    pass