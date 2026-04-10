import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from app.models.enums import TRANSACTION_TYPE

class ShopItem(Base):
    __tablename__ = "shop_items"
    
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    buy_price: Mapped[int] = mapped_column(Integer, nullable=False)
    sell_price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[Optional[int]] = mapped_column(Integer)
    
    __table_args__ = (
        CheckConstraint("buy_price > 0 AND sell_price > 0", name="prices_positive"),
        CheckConstraint("stock IS NULL OR stock >= 0", name="stock_valid"),
        Index("idx_shop_location", "location_id"),
    )

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    transaction_type: Mapped[str] = mapped_column(TRANSACTION_TYPE, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint("amount != 0", name="transactions_amount_nonzero"),
        CheckConstraint("balance_after >= 0", name="transactions_balance_nonnegative"),
    )
