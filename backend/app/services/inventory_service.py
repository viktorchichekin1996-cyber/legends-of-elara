"""Бизнес-логика инвентаря и экипировки (с фиксом UUID)."""
import uuid
import logging
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, and_, func, update
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
LOW_DURABILITY_THRESHOLD = 0.3

def _to_uuid(val: str | UUID) -> UUID:
    """Конвертирует строку или UUID в объект UUID."""
    return val if isinstance(val, UUID) else UUID(val)

async def get_equipped_items(session: AsyncSession, character_id: str | UUID) -> Dict[str, Equipment]:
    char_uuid = _to_uuid(character_id)
    stmt = (
        select(Equipment)
        .options(selectinload(Equipment.inventory).selectinload(Inventory.item))
        .where(Equipment.character_id == char_uuid)
    )
    result = await session.execute(stmt)
    equipped_list = result.scalars().all()
    return {eq.slot: eq for eq in equipped_list}

def calculate_equipment_modifiers(equipped: Dict[str, Equipment]) -> Dict[str, float]:
    total_mods: Dict[str, float] = {}
    for slot, eq in equipped.items():
        item = eq.inventory.item
        durability_mult = 1.0
        if eq.inventory.durability is not None and item.max_durability > 0:
            if eq.inventory.durability <= 0:
                durability_mult = BROKEN_ITEM_PENALTY
            elif eq.inventory.durability < item.max_durability * LOW_DURABILITY_THRESHOLD:
                durability_mult = 0.75
        for key, val in item.modifiers.items():
            if isinstance(val, (int, float)):
                total_mods[key] = total_mods.get(key, 0) + (val * durability_mult)
    return total_mods

async def get_inventory_full(session: AsyncSession, character_id: str | UUID) -> InventoryFullResponse:
    char_uuid = _to_uuid(character_id)
    inv_stmt = select(Inventory).options(selectinload(Inventory.item)).where(Inventory.character_id == char_uuid)
    inv_result = await session.execute(inv_stmt)
    inv_items = inv_result.scalars().all()
    
    equipped = await get_equipped_items(session, char_uuid)
    equipped_inv_ids = {eq.inventory_id for eq in equipped.values()}
    
    char_res = await session.execute(select(Character).where(Character.id == char_uuid))
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

async def equip_item(session: AsyncSession, character_id: str | UUID, inventory_id: str | UUID) -> dict:
    char_uuid = _to_uuid(character_id)
    inv_uuid = _to_uuid(inventory_id)
    
    char_res = await session.execute(select(Character).where(Character.id == char_uuid))
    character = char_res.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    
    inv_stmt = select(Inventory).options(selectinload(Inventory.item)).where(Inventory.id == inv_uuid)
    inv_res = await session.execute(inv_stmt)
    inv_item = inv_res.scalar_one_or_none()
    
    if not inv_item or inv_item.character_id != char_uuid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    
    if inv_item.item.item_type == "consumable":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Расходники нельзя экипировать")
    if not inv_item.item.slot:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У предмета нет слота экипировки")
    if inv_item.item.required_level and character.level < inv_item.item.required_level:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Требуется уровень {inv_item.item.required_level}")
    if inv_item.item.required_class and character.character_class not in inv_item.item.required_class:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Класс не соответствует требованиям")
    
    existing = await session.execute(
        select(Equipment).where(Equipment.character_id == char_uuid, Equipment.slot == inv_item.item.slot)
    )
    old_eq = existing.scalar_one_or_none()
    if old_eq:
        await session.delete(old_eq)
    
    new_eq = Equipment(character_id=char_uuid, slot=inv_item.item.slot, inventory_id=inv_item.id)
    session.add(new_eq)
    await session.flush()
    return {"message": f"Экипировано: {inv_item.item.name}", "slot": inv_item.item.slot}

async def unequip_item(session: AsyncSession, character_id: str | UUID, slot: str) -> dict:
    char_uuid = _to_uuid(character_id)
    eq_res = await session.execute(
        select(Equipment).where(Equipment.character_id == char_uuid, Equipment.slot == slot)
    )
    equipment = eq_res.scalar_one_or_none()
    if not equipment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Слот пуст")
    await session.delete(equipment)
    await session.flush()
    return {"message": "Предмет снят", "slot": slot}

async def use_item(session: AsyncSession, character_id: str | UUID, inventory_id: str | UUID, in_combat: bool = False, target_id: Optional[str] = None) -> dict:
    """8.3 Использование расходника с корректной обработкой UUID."""
    char_uuid = _to_uuid(character_id)
    inv_uuid = _to_uuid(inventory_id)
    
    inv_stmt = select(Inventory).options(selectinload(Inventory.item)).where(Inventory.id == inv_uuid)
    inv_res = await session.execute(inv_stmt)
    inv_item = inv_res.scalar_one_or_none()
    
    # Ключевой фикс: сравниваем UUID с UUID
    if not inv_item or inv_item.character_id != char_uuid:
        logger.warning(f"Item not found: inv_id={inventory_id}, char_id={character_id}, db_char_id={inv_item.character_id if inv_item else None}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    
    if inv_item.item.item_type != "consumable":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Можно использовать только расходники")
    
    if in_combat and inv_item.item.modifiers.get("combat_use", True) is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Этот предмет нельзя использовать в бою")
    
    char = (await session.execute(select(Character).where(Character.id == char_uuid))).scalar_one()
    mods = inv_item.item.modifiers
    effects_applied = []
    
    if "hp_restore" in mods:
        char.hp_current = clamp_value(char.hp_current + mods["hp_restore"], 0, char.hp_max)
        effects_applied.append(f"+{mods['hp_restore']} HP")
    if "mana_restore" in mods:
        char.mana_current = clamp_value(char.mana_current + mods["mana_restore"], 0, char.mana_max)
        effects_applied.append(f"+{mods['mana_restore']} MP")
    if "stamina_restore" in mods:
        char.stamina_current = clamp_value(char.stamina_current + mods["stamina_restore"], 0, char.stamina_max)
        effects_applied.append(f"+{mods['stamina_restore']} STA")
    if "fatigue_reduce" in mods:
        char.fatigue = clamp_value(char.fatigue - mods["fatigue_reduce"], 0, 100)
        effects_applied.append(f"-{mods['fatigue_reduce']} Усталость")
    
    if not effects_applied:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Предмет не имеет эффектов")
    
    # Уменьшение прочности (8.4)
    if inv_item.durability is not None and inv_item.item.max_durability > 0:
        inv_item.durability = max(0, inv_item.durability - 1)
        if inv_item.durability == 0:
            effects_applied.append("⚠️ Предмет сломан!")
    
    # Уменьшение количества или удаление
    if inv_item.quantity > 1:
        inv_item.quantity -= 1
    else:
        await session.delete(inv_item)
    
    await session.flush()
    return {"message": f"Использовано {inv_item.item.name}: {', '.join(effects_applied)}"}

async def reduce_item_durability(session: AsyncSession, inventory_id: str | UUID, amount: int = 1) -> Optional[Dict]:
    inv_uuid = _to_uuid(inventory_id)
    inv_item = (await session.execute(select(Inventory).where(Inventory.id == inv_uuid))).scalar_one_or_none()
    if not inv_item or inv_item.durability is None:
        return None
    inv_item.durability = max(0, inv_item.durability - amount)
    await session.flush()
    status = "ok"
    if inv_item.durability == 0:
        status = "broken"
    elif inv_item.durability < inv_item.item.max_durability * LOW_DURABILITY_THRESHOLD:
        status = "low"
    return {"inventory_id": str(inv_item.id), "durability": inv_item.durability, "max_durability": inv_item.item.max_durability, "status": status}

async def expand_inventory(session: AsyncSession, character_id: str | UUID, bag_item_id: str | UUID) -> dict:
    char_uuid = _to_uuid(character_id)
    bag_uuid = _to_uuid(bag_item_id)
    char = (await session.execute(select(Character).where(Character.id == char_uuid))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    inv = (await session.execute(select(Inventory).where(Inventory.id == bag_uuid, Inventory.character_id == char_uuid))).scalar_one_or_none()
    if not inv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сумка не найдена в инвентаре")
    if inv.item.item_type != "bag":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Это не сумка")
    slot_bonus = inv.item.modifiers.get("slot_bonus", 0)
    if slot_bonus <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Сумка не добавляет слоты")
    return {"message": f"Сумка '{inv.item.name}' добавляет +{slot_bonus} слотов", "new_max_slots": char.inventory_slots + slot_bonus}
