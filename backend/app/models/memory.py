import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ARRAY, CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from app.models.enums import MEMORY_TYPE

class CharacterMemory(Base, TimestampMixin):
    __tablename__ = "character_memories"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    memory_type: Mapped[str] = mapped_column(MEMORY_TYPE, nullable=False)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    importance: Mapped[int] = mapped_column(Integer, nullable=False)
    tags: Mapped[List[str]] = mapped_column(ARRAY(Text))
    data: Mapped[dict] = mapped_column(JSONB, default={}, nullable=False)
    
    __table_args__ = (
        CheckConstraint("importance BETWEEN 1 AND 5", name="memory_importance_range"),
        Index("idx_memories_importance", "importance"),
    )
