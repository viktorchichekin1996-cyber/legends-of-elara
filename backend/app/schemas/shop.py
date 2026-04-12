"""Схемы для магазина, экономики и отдыха."""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class ShopItemResponse(BaseModel):
    """Информация о товаре в магазине."""
    item_id: uuid.UUID
    name: str
    item_type: str
    rarity: str
    buy_price: int
    sell_price: int
    stock: Optional[int] = None
    description: Optional[str] = None
    model_config = {"from_attributes": True}

class BuyRequest(BaseModel):
    """Запрос на покупку предмета."""
    item_id: uuid.UUID = Field(..., description="ID предмета из items")
    quantity: int = Field(default=1, ge=1, le=100, description="Количество")

class SellRequest(BaseModel):
    """Запрос на продажу предмета."""
    inventory_id: uuid.UUID = Field(..., description="ID записи в инвентаре")
    quantity: int = Field(default=1, ge=1, description="Количество")

class RepairRequest(BaseModel):
    """Запрос на ремонт предмета."""
    inventory_id: uuid.UUID = Field(..., description="ID записи в инвентаре")

class TavernRequest(BaseModel):
    """Запрос на ночлег в таверне."""
    pass  # Без параметров, стоимость рассчитывается автоматически

class TransactionResponse(BaseModel):
    """Информация о транзакции."""
    id: uuid.UUID
    transaction_type: str
    amount: int
    description: Optional[str] = None
    balance_after: int
    created_at: datetime
    model_config = {"from_attributes": True}

class EconomyOperationResponse(BaseModel):
    """Универсальный ответ экономической операции."""
    success: bool
    message: str
    gold_before: int
    gold_after: int
    transaction_id: Optional[uuid.UUID] = None
