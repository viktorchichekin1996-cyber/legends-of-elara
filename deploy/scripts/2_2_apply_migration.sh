#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Применение миграций БД"
echo "========================"

cd ~/legends-of-elara/backend

# 1. Генерация миграции
echo "📝 Генерация миграции..."
alembic revision --autogenerate -m "init_full_schema"

# 2. Применение
echo "⬆️ Применение миграции..."
alembic upgrade head

# 3. Проверка
echo "🔍 Проверка созданных таблиц..."
python -c "
import asyncio
from sqlalchemy import inspect, text
from app.db.session import engine

async def check():
    async with engine.connect() as conn:
        result = await conn.execute(text(\"SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;\"))
        tables = [r[0] for r in result.fetchall()]
        print(f'   ✅ Создано таблиц: {len(tables)}')
        for t in tables: print(f'      - {t}')
        if len(tables) < 15:
            print('   ⚠️  Ожидается 15+ таблиц.')
asyncio.run(check())
"

echo "========================"
echo "✅ Миграции успешно применены!"