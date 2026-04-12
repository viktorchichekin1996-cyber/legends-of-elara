import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import QUEST_STATUS

class Quest(Base, TimestampMixin):
    __tablename__ = "quests"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    goals: Mapped[dict] = mapped_column(JSONB, nullable=False)
    rewards: Mapped[dict] = mapped_column(JSONB, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_repeatable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class CharacterQuest(Base, TimestampMixin):
    __tablename__ = "character_quests"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    quest_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("quests.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(QUEST_STATUS, default="active", nullable=False)
    progress: Mapped[dict] = mapped_column(JSONB, nullable=False)
    accepted_at: Mapped[datetime] = mapped_column(server_default="now()")
    completed_at: Mapped[Optional[datetime]]
    
    # === FIX: Добавляем relationship к Quest ===
    quest: Mapped["Quest"] = relationship("Quest", lazy="select")
    
    __table_args__ = (
        Index("idx_character_quests_status", "status"),
    )
