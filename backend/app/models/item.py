import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ARRAY, Boolean, CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import CHARACTER_CLASS, EQUIPMENT_SLOT, ITEM_RARITY, ITEM_TYPE

class Item(Base, TimestampMixin):
    __tablename__ = "items"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    item_type: Mapped[str] = mapped_column(ITEM_TYPE, nullable=False)
    rarity: Mapped[str] = mapped_column(ITEM_RARITY, default="common", nullable=False)
    base_cost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sell_multiplier: Mapped[float] = mapped_column(Numeric(3,2), default=0.5, nullable=False)
    required_level: Mapped[Optional[int]] = mapped_column(Integer, default=1)
    required_class: Mapped[Optional[List[str]]] = mapped_column(ARRAY(CHARACTER_CLASS))
    modifiers: Mapped[dict] = mapped_column(JSONB, default={}, nullable=False)
    damage_min: Mapped[int] = mapped_column(Integer, default=0)
    damage_max: Mapped[int] = mapped_column(Integer, default=0)
    armor: Mapped[int] = mapped_column(Integer, default=0)
    max_durability: Mapped[int] = mapped_column(Integer, default=100)
    slot: Mapped[Optional[str]] = mapped_column(EQUIPMENT_SLOT)
    is_stackable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    inventory_items: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="item")
