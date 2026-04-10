#!/usr/bin/env bash
set -euo pipefail

echo "🌱 Подэтап 2.7: Заполнение БД (Seed данные)"
echo "============================================="

cd ~/legends-of-elara/backend
mkdir -p seeds

# Создаём скрипт загрузки
cat > seeds/load_seeds.py <<'PYEOF'
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.models.location import Location
from app.models.enums import LOCATION_TYPE
from app.models.item import Item
from app.models.enums import ITEM_TYPE, ITEM_RARITY
from app.models.combat import Enemy
from app.models.system import GameLog
from loguru import logger

LOCATIONS = [
    {"name": "Деревня Элдарион", "location_type": "city", "region": "Центральный", "coord_x": 0, "coord_y": 0, "danger_level": 0, "min_level": 1, "is_safe": True, "has_shop": True, "has_tavern": True},
    {"name": "Шёпот Лесов", "location_type": "forest", "region": "Север", "coord_x": 1, "coord_y": 2, "danger_level": 2, "min_level": 1, "is_safe": False},
    {"name": "Пещера Теней", "location_type": "cave", "region": "Восток", "coord_x": 3, "coord_y": 1, "danger_level": 4, "min_level": 3, "is_safe": False},
    {"name": "Дорога торговцев", "location_type": "road", "region": "Центральный", "coord_x": 0, "coord_y": 1, "danger_level": 1, "min_level": 1, "is_safe": False}
]

ITEMS = [
    {"name": "Ржавый меч", "item_type": "weapon", "rarity": "common", "base_cost": 50, "damage_min": 2, "damage_max": 4, "slot": "weapon", "is_stackable": False},
    {"name": "Кожаная броня", "item_type": "armor", "rarity": "common", "base_cost": 40, "armor": 2, "slot": "armor", "is_stackable": False},
    {"name": "Зелье здоровья", "item_type": "consumable", "rarity": "common", "base_cost": 15, "is_stackable": True, "modifiers": {"hp_restore": 20}},
    {"name": "Стальной щит", "item_type": "armor", "rarity": "uncommon", "base_cost": 120, "armor": 4, "slot": "accessory", "is_stackable": False}
]

ENEMIES = [
    {"name": "Бешеный волк", "enemy_type": "beast", "level": 1, "hp": 30, "strength": 6, "agility": 12, "intelligence": 2, "damage_min": 3, "damage_max": 6, "xp_reward": 10, "gold_min": 5, "gold_max": 12},
    {"name": "Гоблин-воришка", "enemy_type": "humanoid", "level": 2, "hp": 45, "strength": 8, "agility": 14, "intelligence": 6, "damage_min": 5, "damage_max": 9, "xp_reward": 25, "gold_min": 15, "gold_max": 30}
]

async def seed():
    async with async_session() as session:
        try:
            # Locations
            for loc in LOCATIONS:
                exists = await session.execute(Location.select().where(Location.name == loc["name"]))
                if not exists.scalar_one_or_none():
                    session.add(Location(**loc))
            await session.flush()
            logger.info("✅ Локации добавлены.")

            # Items
            for itm in ITEMS:
                exists = await session.execute(Item.select().where(Item.name == itm["name"]))
                if not exists.scalar_one_or_none():
                    session.add(Item(**itm))
            await session.flush()
            logger.info("✅ Предметы добавлены.")

            # Enemies
            for enm in ENEMIES:
                exists = await session.execute(Enemy.select().where(Enemy.name == enm["name"]))
                if not exists.scalar_one_or_none():
                    session.add(Enemy(**enm))
            await session.flush()
            logger.info("✅ Враги добавлены.")

            await session.commit()
            logger.info("🎉 Seed данные успешно загружены!")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Ошибка seed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(seed())
PYEOF

# Установка loguru (если вдруг не в venv)
pip install loguru > /dev/null 2>&1

# Запуск
echo "🚀 Запуск скрипта seed..."
python seeds/load_seeds.py

echo "============================================="
echo "✅ Подэтап 2.7 успешно выполнен!"