import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import LOCATION_TYPE

class Location(Base, TimestampMixin):
    __tablename__ = "locations"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location_type: Mapped[str] = mapped_column(LOCATION_TYPE, nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    coord_x: Mapped[int] = mapped_column(Integer, nullable=False)
    coord_y: Mapped[int] = mapped_column(Integer, nullable=False)
    danger_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    ai_description_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_safe: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_shop: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_tavern: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    __table_args__ = (
        Index("idx_locations_type", "location_type"),
        Index("idx_locations_region", "region"),
        Index("idx_locations_coords", "coord_x", "coord_y"),
    )

class LocationConnection(Base):
    __tablename__ = "location_connections"
    
    from_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    to_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    distance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    travel_difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    __table_args__ = (
        CheckConstraint("from_location_id != to_location_id", name="no_self_connection"),
        Index("idx_connections_from", "from_location_id"),
        Index("idx_connections_to", "to_location_id"),
    )
