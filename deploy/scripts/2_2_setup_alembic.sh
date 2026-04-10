#!/usr/bin/env bash
set -euo pipefail

echo "🗄️ Подэтап 2.2: Настройка Alembic и базовых классов"
echo "===================================================="

cd ~/legends-of-elara/backend

# 1. Инициализация Alembic
echo "⚙️ Инициализация Alembic..."
if [ ! -d "alembic" ]; then
    alembic init alembic
    echo "   Alembic инициализирован."
else
    echo "   Alembic уже инициализирован."
fi

# 2. Создание базового класса и миксина
echo "📦 Создание backend/app/db/base.py..."
cat > app/db/base.py <<'PYEOF'
from datetime import datetime
from typing import Any
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime, func

class Base(MappedAsDataclass, DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass

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
PYEOF
echo "   ✅ base.py создан."

# 3. Настройка alembic/env.py для асинхронной работы
echo "🔧 Настройка alembic/env.py (async)..."
cat > alembic/env.py <<'PYEOF'
import asyncio
import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Добавляем корень backend в sys.path для импортов
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Импортируем метаданные и конфиг
from app.db.base import Base
from app.config import settings
from app import models  # Важно: импортируем модели, чтобы Alembic их увидел

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Переопределяем URL из .env
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
PYEOF
echo "   ✅ env.py настроен."

# 4. Проверка подключения
echo "🔍 Проверка подключения к БД..."
python -c "
from app.db.session import engine
import asyncio
async def test():
    async with engine.connect() as conn:
        print('   ✅ Подключение к БД успешно.')
asyncio.run(test())
" || { echo "   ❌ Ошибка подключения. Проверьте .env и статус PostgreSQL."; exit 1; }

echo "===================================================="
echo "✅ Подэтап 2.2 успешно выполнен!"