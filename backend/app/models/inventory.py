import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import EQUIPMENT_SLOT

class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    durability: Mapped[Optional[int]] = mapped_column(Integer)
    
    character: Mapped["Character"] = relationship("Character", back_populates="inventory")
    item: Mapped["Item"] = relationship("Item", back_populates="inventory_items")
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="inventory_quantity_positive"),
        CheckConstraint("durability IS NULL OR durability >= 0", name="inventory_durability_valid"),
        UniqueConstraint("character_id", "item_id", name="unique_stackable"),
        Index("idx_inventory_character", "character_id"),
    )

class Equipment(Base, TimestampMixin):
    __tablename__ = "equipment"
    
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True)
    slot: Mapped[str] = mapped_column(EQUIPMENT_SLOT, primary_key=True)
    inventory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("inventory.id", ondelete="CASCADE"), unique=True)
    equipped_at: Mapped[datetime] = mapped_column(server_default="now()")
    
    inventory: Mapped["Inventory"] = relationship("Inventory")
