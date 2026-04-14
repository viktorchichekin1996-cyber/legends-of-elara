import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import CHARACTER_CLASS, CHARACTER_STATUS
from app.schemas.enums import CharacterStatus  # Добавлен импорт Enum

class Character(Base, TimestampMixin):
    __tablename__ = "characters"
    
    # === Первичный ключ ===
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # === Обязательные поля без дефолтов ===
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    character_class: Mapped[str] = mapped_column(CHARACTER_CLASS, nullable=False)
    current_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id"), index=True, nullable=False)
    hp_current: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_max: Mapped[int] = mapped_column(Integer, nullable=False)
    mana_current: Mapped[int] = mapped_column(Integer, nullable=False)
    mana_max: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_current: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_max: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # === Поля с дефолтами ===
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # ИСПРАВЛЕНО: Используем Enum вместо строки "alive"
    status: Mapped[str] = mapped_column(CHARACTER_STATUS, default=CharacterStatus.ALIVE, nullable=False)
    strength: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    fatigue: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    gold: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    inventory_slots: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    # === Связи ===
    user: Mapped["User"] = relationship("User", back_populates="characters")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="character", cascade="all, delete-orphan")
    
    # === Ограничения ===
    __table_args__ = (
        CheckConstraint("level BETWEEN 1 AND 15", name="characters_level_range"),
        CheckConstraint("fatigue BETWEEN 0 AND 100", name="characters_fatigue_range"),
        CheckConstraint("gold >= 0", name="characters_gold_non_negative"),
        CheckConstraint("strength > 0 AND agility > 0 AND intelligence > 0", name="characters_stats_positive"),
        CheckConstraint("hp_current BETWEEN 0 AND hp_max", name="characters_hp_valid"),
        CheckConstraint("mana_current BETWEEN 0 AND mana_max", name="characters_mana_valid"),
        CheckConstraint("stamina_current BETWEEN 0 AND stamina_max", name="characters_stamina_valid"),
        Index("idx_characters_name", "name"),
        Index("idx_characters_level", "level"),
    )