"""Эндпоинты инвентаря и экипировки."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.schemas.inventory import InventoryFullResponse, EquipRequest, UnequipRequest, UseItemRequest
from app.services.inventory_service import (
    get_inventory_full, equip_item, unequip_item, use_item, reduce_item_durability, expand_inventory
)
from app.services.combat_service import get_active_combat

router = APIRouter(prefix="/inventory", tags=["Inventory & Equipment"])

@router.get("/", response_model=InventoryFullResponse)
async def get_inventory(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.1 Получение состояния инвентаря и экипировки."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    return await get_inventory_full(db, str(char.id))

@router.post("/equip", status_code=status.HTTP_200_OK)
async def equip_item_endpoint(request: EquipRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.2 Экипировка предмета."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    result = await equip_item(db, str(char.id), str(request.inventory_id))
    await db.commit()
    return result

@router.post("/unequip", status_code=status.HTTP_200_OK)
async def unequip_item_endpoint(request: UnequipRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.2 Снятие предмета."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    result = await unequip_item(db, str(char.id), request.slot.value)
    await db.commit()
    return result

@router.post("/use", status_code=status.HTTP_200_OK)
async def use_item_endpoint(request: UseItemRequest, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.3 Использование расходника (валидация боя/вне боя)."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    
    active_combat = await get_active_combat(db, str(char.id))
    in_combat = active_combat is not None and active_combat.is_active
    
    result = await use_item(db, str(char.id), str(request.inventory_id), in_combat=in_combat, target_id=request.target_id)
    await db.commit()
    return result

@router.post("/repair", status_code=status.HTTP_200_OK)
async def repair_item_endpoint(inventory_id: str, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.4 Ремонт предмета (восстановление прочности)."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    
    inv = (await db.execute(select(Inventory).where(Inventory.id == inventory_id, Inventory.character_id == char.id))).scalar_one_or_none()
    if not inv or inv.durability is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден или не имеет прочности")
    
    repair_cost = max(1, (inv.item.max_durability - inv.durability) // 10)
    if char.gold < repair_cost:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Недостаточно золота (нужно {repair_cost})")
    
    char.gold -= repair_cost
    inv.durability = inv.item.max_durability
    await db.commit()
    return {"message": f"Предмет отремонтирован за {repair_cost} золота", "durability": inv.durability}

@router.post("/expand", status_code=status.HTTP_200_OK)
async def expand_inventory_endpoint(bag_inventory_id: str, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """8.5 Активация сумки для расширения инвентаря."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Персонаж не найден")
    result = await expand_inventory(db, str(char.id), bag_inventory_id)
    await db.commit()
    return result
