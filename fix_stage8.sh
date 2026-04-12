#!/bin/bash
# fix_stage8_imports.sh - Исправление импортов Этапа 8

cd ~/legends-of-elara/backend

echo "🔧 Создаём inventory_service.py..."
cat > app/services/inventory_service.py << 'INVENTORY_EOF'
"""Бизнес-логика инвентаря и экипировки."""
import uuid
import logging
from typing import Dict, Any, List, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.inventory import Inventory, Equipment
from app.models.item import Item
from app.models.character import Character
from app.schemas.inventory import InventoryItemResponse, InventoryFullResponse
from app.utils.calculations import clamp_value

logger = logging.getLogger(__name__)
BROKEN_ITEM_PENALTY = 0.5

async def get_equipped_items(session: AsyncSession, character_id: str) -> Dict[str, Equipment]:
    """Загружает экипированные предметы персонажа."""
    stmt = (
        select(Equipment)
        .options(selectinload(Equipment.inventory).selectinload(Inventory.item))
        .where(Equipment.character_id == character_id)
    )
    result = await session.execute(stmt)
    equipped_list = result.scalars().all()
    return {eq.slot: eq for eq in equipped_list}

def calculate_equipment_modifiers(equipped: Dict[str, Equipment]) -> Dict[str, float]:
    """Суммирует модификаторы экипировки с учётом прочности."""
    total_mods: Dict[str, float] = {}
    for slot, eq in equipped.items():
        item = eq.inventory.item
        durability_mult = 1.0
        if eq.inventory.durability is not None and item.max_durability > 0:
            if eq.inventory.durability <= 0:
                durability_mult = BROKEN_ITEM_PENALTY
            elif eq.inventory.durability < item.max_durability * 0.3:
                durability_mult = 0.75
        for key, val in item.modifiers.items():
            if isinstance(val, (int, float)):
                total_mods[key] = total_mods.get(key, 0) + (val * durability_mult)
    return total_mods

async def get_inventory_full(session: AsyncSession, character_id: str) -> InventoryFullResponse:
    """Возвращает полное состояние инвентаря и экипировки."""
    inv_stmt = select(Inventory).options(selectinload(Inventory.item)).where(Inventory.character_id == character_id)
    inv_result = await session.execute(inv_stmt)
    inv_items = inv_result.scalars().all()
    
    equipped = await get_equipped_items(session, character_id)
    equipped_inv_ids = {eq.inventory_id for eq in equipped.values()}
    
    char_res = await session.execute(select(Character).where(Character.id == character_id))
    character = char_res.scalar_one()
    
    base_slots = character.inventory_slots
    bag_bonus = sum(
        item.quantity * item.item.modifiers.get("slot_bonus", 0)
        for item in inv_items
        if item.item.item_type == "bag"
    )
    max_slots = base_slots + bag_bonus
    
    items_response = [
        InventoryItemResponse(
            id=item.id, item_id=item.item_id, name=item.item.name,
            description=item.item.description, item_type=item.item.item_type,
            rarity=item.item.rarity, quantity=item.quantity,
            durability=item.durability,
            max_durability=item.item.max_durability if item.item.max_durability > 0 else None,
            is_equipped=item.id in equipped_inv_ids,
            slot=item.item.slot,
        )
        for item in inv_items
    ]
    
    equipment_response = {}
    for slot_name in ["weapon", "armor", "helmet", "gloves", "boots", "accessory", "ring1", "ring2"]:
        eq = equipped.get(slot_name)
        if eq:
            equipment_response[slot_name] = InventoryItemResponse(
                id=eq.inventory.id, item_id=eq.inventory.item.id,
                name=eq.inventory.item.name, description=eq.inventory.item.description,
                item_type=eq.inventory.item.item_type, rarity=eq.inventory.item.rarity,
                quantity=1, durability=eq.inventory.durability,
                max_durability=eq.inventory.item.max_durability if eq.inventory.item.max_durability > 0 else None,
                is_equipped=True, slot=eq.inventory.item.slot,
            )
        else:
            equipment_response[slot_name] = None

    return InventoryFullResponse(
        used_slots=len(inv_items), max_slots=max_slots,
        items=items_response, equipment=equipment_response
    )
INVENTORY_EOF

echo "✅ inventory_service.py создан"

echo "🔧 Обновляем character_service.py (исправляем импорты и calculate_character_stats)..."
cat > app/services/character_service.py << 'CHAR_EOF'
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
CHAR_EOF

echo "✅ character_service.py обновлён"

echo "🔧 Создаём schemas/inventory.py..."
cat > app/schemas/inventory.py << 'SCHEMA_EOF'
"""Схемы для инвентаря и экипировки."""
from typing import Optional, List, Dict, Any
import uuid
from pydantic import BaseModel, Field
from app.schemas.enums import ItemType, ItemRarity, EquipmentSlot

class InventoryItemResponse(BaseModel):
    id: uuid.UUID
    item_id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_type: ItemType
    rarity: ItemRarity
    quantity: int
    durability: Optional[int] = None
    max_durability: Optional[int] = None
    is_equipped: bool = False
    slot: Optional[EquipmentSlot] = None
    model_config = {"from_attributes": True}

class InventoryFullResponse(BaseModel):
    used_slots: int
    max_slots: int
    items: List[InventoryItemResponse]
    equipment: Dict[str, Optional[InventoryItemResponse]] = Field(default_factory=dict)
    model_config = {"from_attributes": True}

class EquipRequest(BaseModel):
    inventory_id: uuid.UUID = Field(..., description="ID записи в инвентаре")

class UnequipRequest(BaseModel):
    slot: EquipmentSlot = Field(..., description="Слот экипировки")

class UseItemRequest(BaseModel):
    inventory_id: uuid.UUID = Field(..., description="ID записи в инвентаре")
    target_id: Optional[uuid.UUID] = Field(None, description="ID цели")
SCHEMA_EOF

echo "✅ schemas/inventory.py создан"

echo "🔧 Создаём api/v1/inventory.py..."
cat > app/api/v1/inventory.py << 'API_EOF'
"""Эндпоинты инвентаря и экипировки."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.schemas.inventory import InventoryFullResponse, EquipRequest, UnequipRequest, UseItemRequest
from app.services.inventory_service import get_inventory_full

router = APIRouter(prefix="/inventory", tags=["Inventory & Equipment"])

@router.get("/", response_model=InventoryFullResponse)
async def get_inventory(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    return await get_inventory_full(db, str(char.id))

@router.post("/equip", status_code=status.HTTP_200_OK)
async def equip_item_endpoint(request: EquipRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Экипировка будет реализована в подэтапе 8.2")

@router.post("/unequip", status_code=status.HTTP_200_OK)
async def unequip_item_endpoint(request: UnequipRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Снятие экипировки будет реализовано в подэтапе 8.2")

@router.post("/use", status_code=status.HTTP_200_OK)
async def use_item_endpoint(request: UseItemRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Использование предметов будет реализовано в подэтапе 8.3")
API_EOF

echo "✅ api/v1/inventory.py создан"

echo "🔧 Обновляем api/v1/router.py (добавляем inventory_router)..."
cat > app/api/v1/router.py << 'ROUTER_EOF'
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.character import router as character_router
from app.api.v1.combat import router as combat_router
from app.api.v1.locations import router as locations_router
from app.api.v1.inventory import router as inventory_router

v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(character_router)
v1_router.include_router(combat_router)
v1_router.include_router(locations_router)
v1_router.include_router(inventory_router)
ROUTER_EOF

echo "✅ api/v1/router.py обновлён"

echo ""
echo "🔄 Перезапускаем сервер..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 1

echo "🚀 Запуск uvicorn..."
nohup uvicorn app.main:app --host 127.0.0.1 --port 8000 > ~/legends-of-elara/backend/uvicorn.log 2>&1 &
sleep 3

echo ""
echo "✅ Проверка здоровья API:"
curl -s http://127.0.0.1:8000/health | python3 -m json.tool

echo ""
echo "🎉 Готово! Импорт ошибки устранены."
echo "📋 Логи сервера: tail -f ~/legends-of-elara/backend/uvicorn.log"