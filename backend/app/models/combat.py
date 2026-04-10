import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin

class Enemy(Base, TimestampMixin):
    __tablename__ = "enemies"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    enemy_type: Mapped[str] = mapped_column(String(50), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    hp: Mapped[int] = mapped_column(Integer, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_min: Mapped[int] = mapped_column(Integer, nullable=False)
    damage_max: Mapped[int] = mapped_column(Integer, nullable=False)
    armor: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    dodge_chance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    crit_chance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    gold_min: Mapped[int] = mapped_column(Integer, nullable=False)
    gold_max: Mapped[int] = mapped_column(Integer, nullable=False)
    loot_table: Mapped[dict] = mapped_column(JSONB, default=[], nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

class CombatSession(Base, TimestampMixin):
    __tablename__ = "combat_sessions"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    enemy_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("enemies.id"))
    enemy_name: Mapped[str] = mapped_column(String(100), nullable=False)
    enemy_hp_current: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_hp_max: Mapped[int] = mapped_column(Integer, nullable=False)
    enemy_stats: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    current_turn: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    combat_log: Mapped[dict] = mapped_column(JSONB, default=[], nullable=False)
    result: Mapped[Optional[str]] = mapped_column(String(20))
    rewards: Mapped[Optional[dict]] = mapped_column(JSONB)
    started_at: Mapped[datetime] = mapped_column(server_default="now()")
    ended_at: Mapped[Optional[datetime]]
    
    __table_args__ = (
        UniqueConstraint("character_id", "is_active", name="combat_unique_active"),
        Index("idx_combat_active", "is_active"),
    )
