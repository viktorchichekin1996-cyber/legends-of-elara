"""Эндпоинты магазина и экономики."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location
from app.schemas.shop import (
    ShopItemResponse, BuyRequest, SellRequest, RepairRequest,
    EconomyOperationResponse
)
from app.services.shop_service import (
    get_shop_items, buy_item, sell_item, repair_item
)

router = APIRouter(prefix="/shop", tags=["Shop & Economy"])

@router.get("/", response_model=list[ShopItemResponse])
async def get_shop(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    location = (await db.execute(select(Location).where(Location.id == char.current_location_id))).scalar_one_or_none()
    if not location or not location.has_shop:
        raise HTTPException(status_code=400, detail="В этой локации нет магазина")
    
    return await get_shop_items(db, location.id)

@router.post("/buy", response_model=EconomyOperationResponse)
async def buy_from_shop(
    request: BuyRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    result = await buy_item(db, char.id, request.item_id, request.quantity)
    await db.commit()
    return result

@router.post("/sell", response_model=EconomyOperationResponse)
async def sell_to_shop(
    request: SellRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    result = await sell_item(db, char.id, request.inventory_id, request.quantity)
    await db.commit()
    return result

@router.post("/repair", response_model=EconomyOperationResponse)
async def repair_equipment(
    request: RepairRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    result = await repair_item(db, char.id, request.inventory_id)
    await db.commit()
    return result
