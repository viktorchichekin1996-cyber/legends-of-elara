import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class AiPrompt(Base, TimestampMixin):
    __tablename__ = "ai_prompts"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    prompt_type: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer)

class GameLog(Base):
    __tablename__ = "game_logs"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    component: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    character_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("characters.id"))
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default="now()")
    
    __table_args__ = (
        Index("idx_game_logs_level", "level"),
        Index("idx_game_logs_component", "component"),
        Index("idx_game_logs_character", "character_id"),
    )
