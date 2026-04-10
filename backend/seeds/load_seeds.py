"""
Seed-скрипт для начального наполнения БД.
Идемпотентен: пропускает уже существующие записи.
"""
import sys
import os
import asyncio

# === FIX: Добавляем корень backend в sys.path ===
# Это решает ошибку "ModuleNotFoundError: No module named 'app'"
# При запуске из папки seeds/ мы поднимаемся на уровень выше (в backend/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select
from app.db.session import async_session
from app.models.location import Location, LocationConnection
from app.models.item import Item
from app.models.combat import Enemy
from loguru import logger

async def seed_locations(session):
    locations = [
        {"name": "Деревня Элдарион", "location_type": "city", "region": "Центральный", "coord_x": 0, "coord_y": 0, "danger_level": 0, "min_level": 1, "is_safe": True, "has_shop": True, "has_tavern": True, "description": "Тихая деревня на окраине королевства."},
        {"name": "Шёпот Лесов", "location_type": "forest", "region": "Север", "coord_x": 1, "coord_y": 2, "danger_level": 2, "min_level": 1, "is_safe": False, "description": "Густой древний лес, полный теней и шорохов."},
        {"name": "Пещера Теней", "location_type": "cave", "region": "Восток", "coord_x": 3, "coord_y": 1, "danger_level": 4, "min_level": 3, "is_safe": False, "description": "Мрачная пещера, откуда доносятся странные звуки."},
        {"name": "Дорога торговцев", "location_type": "road", "region": "Центральный", "coord_x": 0, "coord_y": 1, "danger_level": 1, "min_level": 1, "is_safe": False, "description": "Пыльная, но оживлённая тропа."}
    ]
    for loc in locations:
        if not (await session.execute(select(Location).where(Location.name == loc["name"]))).scalar_one_or_none():
            session.add(Location(**loc))
    await session.flush()
    logger.info("✅ Локации добавлены.")

async def seed_connections(session):
    names = ["Деревня Элдарион", "Шёпот Лесов", "Пещера Теней", "Дорога торговцев"]
    locs = {}
    for n in names:
        res = await session.execute(select(Location).where(Location.name == n))
        loc = res.scalar_one()
        if not loc:
            logger.error(f"Не найдена локация: {n}")
            return
        locs[n] = loc.id
        
    conns = [
        (locs["Деревня Элдарион"], locs["Дорога торговцев"], 1, 1),
        (locs["Дорога торговцев"], locs["Деревня Элдарион"], 1, 1),
        (locs["Деревня Элдарион"], locs["Шёпот Лесов"], 1, 2),
        (locs["Шёпот Лесов"], locs["Деревня Элдарион"], 1, 2),
        (locs["Дорога торговцев"], locs["Пещера Теней"], 2, 2),
        (locs["Пещера Теней"], locs["Дорога торговцев"], 2, 2)
    ]
    for f, t, d, diff in conns:
        if not (await session.execute(select(LocationConnection).where(LocationConnection.from_location_id == f, LocationConnection.to_location_id == t))).scalar_one_or_none():
            session.add(LocationConnection(from_location_id=f, to_location_id=t, distance=d, travel_difficulty=diff))
    await session.flush()
    logger.info("✅ Связи локаций добавлены.")

async def seed_items(session):
    items = [
        {"name": "Ржавый меч", "item_type": "weapon", "rarity": "common", "base_cost": 50, "damage_min": 2, "damage_max": 4, "slot": "weapon", "is_stackable": False},
        {"name": "Кожаная броня", "item_type": "armor", "rarity": "common", "base_cost": 40, "armor": 2, "slot": "armor", "is_stackable": False},
        {"name": "Зелье здоровья", "item_type": "consumable", "rarity": "common", "base_cost": 15, "is_stackable": True, "modifiers": {"hp_restore": 20}},
        {"name": "Стальной щит", "item_type": "armor", "rarity": "uncommon", "base_cost": 120, "armor": 4, "slot": "accessory", "is_stackable": False}
    ]
    for itm in items:
        if not (await session.execute(select(Item).where(Item.name == itm["name"]))).scalar_one_or_none():
            session.add(Item(**itm))
    await session.flush()
    logger.info("✅ Предметы добавлены.")

async def seed_enemies(session):
    enemies = [
        {"name": "Бешеный волк", "enemy_type": "beast", "level": 1, "hp": 30, "strength": 6, "agility": 12, "intelligence": 2, "damage_min": 3, "damage_max": 6, "xp_reward": 10, "gold_min": 5, "gold_max": 12, "description": "Худой, но агрессивный хищник."},
        {"name": "Гоблин-воришка", "enemy_type": "humanoid", "level": 2, "hp": 45, "strength": 8, "agility": 14, "intelligence": 6, "damage_min": 5, "damage_max": 9, "xp_reward": 25, "gold_min": 15, "gold_max": 30, "description": "Проворный гоблин с заточкой."}
    ]
    for enm in enemies:
        if not (await session.execute(select(Enemy).where(Enemy.name == enm["name"]))).scalar_one_or_none():
            session.add(Enemy(**enm))
    await session.flush()
    logger.info("✅ Враги добавлены.")

async def run_seed():
    async with async_session() as session:
        try:
            await seed_locations(session)
            await seed_connections(session)
            await seed_items(session)
            await seed_enemies(session)
            await session.commit()
            logger.success("🎉 Seed данные успешно загружены!")
        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Ошибка seed: {e}")
            raise

if __name__ == "__main__":
    asyncio.run(run_seed())
