"""Бизнес-логика магазина и отдыха. Этап 10.2-10.5"""
import uuid
from typing import List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.character import Character
from app.models.item import Item
from app.models.inventory import Inventory
from app.models.shop import ShopItem
from app.models.location import Location
from app.services.economy_service import record_transaction, can_afford, get_character_gold
from app.schemas.shop import ShopItemResponse, EconomyOperationResponse

async def get_shop_items(session: AsyncSession, location_id: uuid.UUID) -> List[ShopItemResponse]:
    """Получает список товаров в магазине локации."""
    stmt = (
        select(ShopItem, Item)
        .join(Item, ShopItem.item_id == Item.id)
        .where(ShopItem.location_id == location_id)
        .options(selectinload(ShopItem.item))
    )
    result = await session.execute(stmt)
    return [
        ShopItemResponse(
            item_id=item.id,
            name=item.name,
            item_type=item.item_type,
            rarity=item.rarity,
            buy_price=shop.buy_price,
            sell_price=shop.sell_price,
            stock=shop.stock,
            description=item.description,
        )
        for shop, item in result.all()
    ]

async def buy_item(session: AsyncSession, character_id: uuid.UUID, item_id: uuid.UUID, quantity: int = 1) -> EconomyOperationResponse:
    """Покупка предмета."""
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    location = (await session.execute(select(Location).where(Location.id == char.current_location_id))).scalar_one_or_none()
    if not location or not location.has_shop:
        raise HTTPException(status_code=400, detail="В этой локации нет магазина")
    
    shop_item = (await session.execute(
        select(ShopItem).where(and_(ShopItem.location_id == location.id, ShopItem.item_id == item_id))
    )).scalar_one_or_none()
    if not shop_item:
        raise HTTPException(status_code=404, detail="Товар не найден в магазине")
        
    item = (await session.execute(select(Item).where(Item.id == item_id))).scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Предмет не найден в БД")
        
    total_cost = shop_item.buy_price * quantity
    if not await can_afford(session, character_id, total_cost):
        raise HTTPException(status_code=400, detail="Недостаточно золота")
    
    gold_before = await get_character_gold(session, character_id)
    await record_transaction(session, character_id, 'shop_buy', -total_cost, f"Покупка: {item.name} x{quantity}", item_id)
    
    existing = (await session.execute(
        select(Inventory).where(and_(Inventory.character_id == character_id, Inventory.item_id == item_id))
    )).scalar_one_or_none()
    
    if existing and item.is_stackable:
        existing.quantity += quantity
    else:
        new_inv = Inventory(
            character_id=character_id,
            item_id=item_id,
            quantity=quantity,
            durability=item.max_durability if item.max_durability > 0 else None
        )
        session.add(new_inv)
        
    await session.flush()
    return EconomyOperationResponse(
        success=True, 
        message=f"Куплено: {item.name} x{quantity} за {total_cost} золота",
        gold_before=gold_before, 
        gold_after=await get_character_gold(session, character_id)
    )

async def sell_item(session: AsyncSession, character_id: uuid.UUID, inventory_id: uuid.UUID, quantity: int = 1) -> EconomyOperationResponse:
    """Продажа предмета из инвентаря."""
    inv = (await session.execute(
        select(Inventory).options(selectinload(Inventory.item)).where(Inventory.id == inventory_id)
    )).scalar_one_or_none()
    if not inv or inv.character_id != character_id:
        raise HTTPException(status_code=404, detail="Предмет не найден в инвентаре")
        
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    location = (await session.execute(select(Location).where(Location.id == char.current_location_id))).scalar_one_or_none()
    if not location or not location.has_shop:
        raise HTTPException(status_code=400, detail="В этой локации нет магазина")
        
    # Расчет цены продажи
    shop_item = (await session.execute(
        select(ShopItem).where(and_(ShopItem.location_id == location.id, ShopItem.item_id == inv.item_id))
    )).scalar_one_or_none()
    
    if shop_item:
        sell_value = int(shop_item.sell_price * quantity)
    else:
        # Если товара нет в магазине, продаем по дефолту предмета
        sell_value = int(inv.item.base_cost * inv.item.sell_multiplier * quantity)
        
    gold_before = await get_character_gold(session, character_id)
    await record_transaction(session, character_id, 'shop_sell', sell_value, f"Продажа: {inv.item.name} x{quantity}", inv.id)
    
    if inv.quantity > quantity:
        inv.quantity -= quantity
    else:
        await session.delete(inv)
        
    await session.flush()
    return EconomyOperationResponse(
        success=True, 
        message=f"Продано: {inv.item.name} x{quantity} за {sell_value} золота",
        gold_before=gold_before, 
        gold_after=await get_character_gold(session, character_id)
    )

async def repair_item(session: AsyncSession, character_id: uuid.UUID, inventory_id: uuid.UUID) -> EconomyOperationResponse:
    """Ремонт предмета."""
    inv = (await session.execute(
        select(Inventory).options(selectinload(Inventory.item)).where(Inventory.id == inventory_id)
    )).scalar_one_or_none()
    if not inv or inv.character_id != character_id or inv.durability is None:
        raise HTTPException(status_code=404, detail="Предмет не найден или не имеет прочности")
    if inv.durability >= inv.item.max_durability:
        raise HTTPException(status_code=400, detail="Предмет уже в идеальном состоянии")
        
    damage_ratio = (inv.item.max_durability - inv.durability) / inv.item.max_durability
    repair_cost = max(1, int(inv.item.base_cost * damage_ratio * 0.5))
    
    if not await can_afford(session, character_id, repair_cost):
        raise HTTPException(status_code=400, detail=f"Недостаточно золота (нужно {repair_cost})")
        
    gold_before = await get_character_gold(session, character_id)
    await record_transaction(session, character_id, 'repair', -repair_cost, f"Ремонт: {inv.item.name}", inv.id)
    
    inv.durability = inv.item.max_durability
    await session.flush()
    
    return EconomyOperationResponse(
        success=True, 
        message=f"Предмет '{inv.item.name}' отремонтирован за {repair_cost} золота",
        gold_before=gold_before, 
        gold_after=await get_character_gold(session, character_id)
    )

async def rest_in_tavern(session: AsyncSession, character_id: uuid.UUID) -> EconomyOperationResponse:
    """Ночлег в таверне."""
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    location = (await session.execute(select(Location).where(Location.id == char.current_location_id))).scalar_one_or_none()
    if not location or not location.has_tavern:
        raise HTTPException(status_code=400, detail="В этой локации нет таверны")
        
    tavern_cost = 10 + (char.level * 5)
    if not await can_afford(session, character_id, tavern_cost):
        raise HTTPException(status_code=400, detail=f"Недостаточно золота (нужно {tavern_cost})")
        
    gold_before = await get_character_gold(session, character_id)
    await record_transaction(session, character_id, 'tavern_rest', -tavern_cost, f"Ночлег в таверне: {location.name}", location.id)
    
    char.hp_current = char.hp_max
    char.mana_current = char.mana_max
    char.stamina_current = char.stamina_max
    char.fatigue = 0
    await session.flush()
    
    return EconomyOperationResponse(
        success=True, 
        message=f"Вы отлично отдохнули в таверне '{location.name}'. Все ресурсы восстановлены!",
        gold_before=gold_before, 
        gold_after=await get_character_gold(session, character_id)
    )
