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
