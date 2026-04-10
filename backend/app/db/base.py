from datetime import datetime
from sqlalchemy import MetaData, DateTime, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

# Метаданные для корректной работы с ENUM и другими типами
metadata = MetaData()

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    metadata = metadata

class TimestampMixin:
    """Миксин для автоматического добавления created_at и updated_at."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )