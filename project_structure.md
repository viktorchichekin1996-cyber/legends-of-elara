# Структура проекта: legends-of-elara

*Сгенерировано: 2026-04-10 22:12:48*

*Путь: `/root/legends-of-elara`*

---

## Структура проекта

Дерево файлов и директорий проекта:



- **legends-of-elara//**
  - **backend/**
    - **alembic/**
      - **versions/**
        - `f10436cfd78e_init_full_schema_fixed.py` (21.9 KB)
      - `env.py` (1.8 KB)
      - `README` (0.0 KB)
      - `script.py.mako` (0.6 KB)
    - **app/**
      - **api/**
        - **v1/**
          - `__init__.py` (0.0 KB)
          - `auth.py` (2.6 KB)
          - `router.py` (0.1 KB)
        - `__init__.py` (0.0 KB)
        - `deps.py` (0.9 KB)
        - `router.py` (0.1 KB)
      - **core/**
        - `__init__.py` (0.0 KB)
        - `security.py` (1.5 KB)
        - `vk_auth.py` (1.2 KB)
      - **db/**
        - `__init__.py` (0.0 KB)
        - `base.py` (0.8 KB)
        - `session.py` (0.3 KB)
      - **models/**
        - `__init__.py` (0.7 KB)
        - `character.py` (3.2 KB)
        - `combat.py` (2.9 KB)
        - `enums.py` (1.2 KB)
        - `inventory.py` (1.9 KB)
        - `item.py` (1.8 KB)
        - `location.py` (2.3 KB)
        - `memory.py` (1.2 KB)
        - `quest.py` (1.8 KB)
        - `shop.py` (1.9 KB)
        - `system.py` (1.7 KB)
        - `user.py` (0.7 KB)
      - **schemas/**
        - `__init__.py` (0.0 KB)
        - `auth.py` (0.7 KB)
      - `__init__.py` (0.0 KB)
      - `config.py` (0.6 KB)
      - `main.py` (1.5 KB)
    - **seeds/**
      - `load_seeds.py` (6.0 KB)
    - `.env` (0.5 KB) 📝
    - `alembic.ini` (3.5 KB)
    - `requirements.txt` (0.6 KB)
  - **deploy/**
    - **backups/**
    - **scripts/**
  - **docs/**
  - **frontend/**
  - **nginx/**
    - **conf.d/**
      - `api.conf` (0.4 KB)
    - **ssl/**
    - `nginx.conf` (0.5 KB)
  - `.env` (0.5 KB) 📝
  - `.env.example` (0.7 KB)
  - `.gitignore` (0.6 KB)
  - `README.md` (0.5 KB)
  - `scan_project.py` (13.7 KB)


---

## Файлы кода

Найдено файлов кода: **40**



### 1. `.env`

**Размер:** 0.5 KB

**Язык:** `env`

⚠️ **Внимание:** Значения переменных окружения скрыты для безопасности.



```env
# База данных
DATABASE_URL=[REDACTED]

# Redis
REDIS_URL=[REDACTED]

# JWT
JWT_SECRET_KEY=[REDACTED]
JWT_ALGORITHM=[REDACTED]
JWT_EXPIRE_DAYS=[REDACTED]

# VK (заглушки)
VK_APP_ID=[REDACTED]
VK_APP_SECRET=[REDACTED]

# Yandex (заглушки)
YANDEX_API_KEY=[REDACTED]
YANDEX_FOLDER_ID=[REDACTED]

```



### 2. `.env.example`

**Размер:** 0.7 KB



```
# Общие
PROJECT_NAME=legends-of-elara
ENVIRONMENT=development

# База данных
POSTGRES_USER=elara_user
POSTGRES_PASSWORD=change_me_strong_password
POSTGRES_DB=elara_db
DATABASE_URL=postgresql+asyncpg://elara_user:change_me_strong_password@postgres:5432/elara_db

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
JWT_SECRET_KEY=change_me_to_64_random_chars_or_more
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# VK Mini App
VK_APP_ID=your_vk_app_id
VK_APP_SECRET=your_vk_app_secret

# Yandex Cloud
YANDEX_API_KEY=your_yandex_cloud_api_key
YANDEX_FOLDER_ID=your_yandex_folder_id

# Домены
API_DOMAIN=api.chichekin-tech.ru
APP_DOMAIN=app.chichekin-tech.ru
FRONTEND_URL=http://localhost:5173

```



### 3. `README.md`

**Размер:** 0.5 KB

**Язык:** `markdown`



```markdown
# 🐉 Легенды Элары
Браузерная текстовая RPG с ИИ-генерацией событий, интегрированная с VK Mini Apps.

## 🚀 Быстрый старт
1. `cp .env.example .env` и заполните секреты.
2. `docker compose up -d --build`
3. Backend Swagger: `http://localhost:8000/docs`
4. Frontend (dev): `cd frontend && npm run dev`

## 🛠️ Стек
Python 3.11 | FastAPI | SQLAlchemy 2.0 | PostgreSQL 15 | Redis 7 | React 18 | VKUI | Docker Compose

```



### 4. `backend/.env`

**Размер:** 0.5 KB

**Язык:** `env`

⚠️ **Внимание:** Значения переменных окружения скрыты для безопасности.



```env
# База данных
DATABASE_URL=[REDACTED]

# Redis
REDIS_URL=[REDACTED]

# JWT
JWT_SECRET_KEY=[REDACTED]
JWT_ALGORITHM=[REDACTED]
JWT_EXPIRE_DAYS=[REDACTED]

# VK (заглушки)
VK_APP_ID=[REDACTED]
VK_APP_SECRET=[REDACTED]

# Yandex (заглушки)
YANDEX_API_KEY=[REDACTED]
YANDEX_FOLDER_ID=[REDACTED]
```



### 5. `backend/alembic.ini`

**Размер:** 3.5 KB

**Язык:** `ini`



```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```



### 6. `backend/alembic/env.py`

**Размер:** 1.8 KB

**Язык:** `python`



```python
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

```



### 7. `backend/alembic/versions/f10436cfd78e_init_full_schema_fixed.py`

**Размер:** 21.9 KB

**Язык:** `python`



```python
"""init_full_schema_fixed

Revision ID: f10436cfd78e
Revises: 
Create Date: 2026-04-10 20:50:53.766239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f10436cfd78e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ai_prompts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('prompt_hash', sa.String(length=64), nullable=False),
    sa.Column('prompt_type', sa.String(length=50), nullable=False),
    sa.Column('prompt_text', sa.Text(), nullable=False),
    sa.Column('response_text', sa.Text(), nullable=False),
    sa.Column('tokens_used', sa.Integer(), nullable=True),
    sa.Column('latency_ms', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('prompt_hash')
    )
    op.create_table('enemies',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('enemy_type', sa.String(length=50), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('hp', sa.Integer(), nullable=False),
    sa.Column('strength', sa.Integer(), nullable=False),
    sa.Column('agility', sa.Integer(), nullable=False),
    sa.Column('intelligence', sa.Integer(), nullable=False),
    sa.Column('damage_min', sa.Integer(), nullable=False),
    sa.Column('damage_max', sa.Integer(), nullable=False),
    sa.Column('armor', sa.Integer(), nullable=False),
    sa.Column('dodge_chance', sa.Integer(), nullable=False),
    sa.Column('crit_chance', sa.Integer(), nullable=False),
    sa.Column('xp_reward', sa.Integer(), nullable=False),
    sa.Column('gold_min', sa.Integer(), nullable=False),
    sa.Column('gold_max', sa.Integer(), nullable=False),
    sa.Column('loot_table', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('item_type', postgresql.ENUM('weapon', 'armor', 'accessory', 'consumable', 'quest_item', 'bag', name='item_type'), nullable=False),
    sa.Column('rarity', postgresql.ENUM('common', 'uncommon', 'rare', 'epic', 'legendary', name='item_rarity'), nullable=False),
    sa.Column('base_cost', sa.Integer(), nullable=False),
    sa.Column('sell_multiplier', sa.Numeric(precision=3, scale=2), nullable=False),
    sa.Column('required_level', sa.Integer(), nullable=True),
    sa.Column('required_class', sa.ARRAY(postgresql.ENUM('warrior', 'priest', 'paladin', 'mage', 'summoner', 'necromancer', 'barbarian', 'hunter', 'druid', 'rogue', 'werewolf', name='character_class')), nullable=True),
    sa.Column('modifiers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('damage_min', sa.Integer(), nullable=False),
    sa.Column('damage_max', sa.Integer(), nullable=False),
    sa.Column('armor', sa.Integer(), nullable=False),
    sa.Column('max_durability', sa.Integer(), nullable=False),
    sa.Column('slot', postgresql.ENUM('weapon', 'armor', 'helmet', 'gloves', 'boots', 'accessory', 'ring1', 'ring2', name='equipment_slot'), nullable=True),
    sa.Column('is_stackable', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('location_type', postgresql.ENUM('city', 'forest', 'road', 'dungeon', 'cave', 'mountain', 'swamp', name='location_type'), nullable=False),
    sa.Column('region', sa.String(length=50), nullable=False),
    sa.Column('coord_x', sa.Integer(), nullable=False),
    sa.Column('coord_y', sa.Integer(), nullable=False),
    sa.Column('danger_level', sa.Integer(), nullable=False),
    sa.Column('min_level', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('ai_description_generated', sa.Boolean(), nullable=False),
    sa.Column('is_safe', sa.Boolean(), nullable=False),
    sa.Column('has_shop', sa.Boolean(), nullable=False),
    sa.Column('has_tavern', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_locations_coords', 'locations', ['coord_x', 'coord_y'], unique=False)
    op.create_index('idx_locations_region', 'locations', ['region'], unique=False)
    op.create_index('idx_locations_type', 'locations', ['location_type'], unique=False)
    op.create_table('quests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('goals', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('rewards', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('min_level', sa.Integer(), nullable=False),
    sa.Column('is_repeatable', sa.Boolean(), nullable=False),
    sa.Column('ai_generated', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('vk_user_id', sa.BigInteger(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_vk_user_id'), 'users', ['vk_user_id'], unique=True)
    op.create_table('characters',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('character_class', postgresql.ENUM('warrior', 'priest', 'paladin', 'mage', 'summoner', 'necromancer', 'barbarian', 'hunter', 'druid', 'rogue', 'werewolf', name='character_class'), nullable=False),
    sa.Column('current_location_id', sa.UUID(), nullable=False),
    sa.Column('hp_current', sa.Integer(), nullable=False),
    sa.Column('hp_max', sa.Integer(), nullable=False),
    sa.Column('mana_current', sa.Integer(), nullable=False),
    sa.Column('mana_max', sa.Integer(), nullable=False),
    sa.Column('stamina_current', sa.Integer(), nullable=False),
    sa.Column('stamina_max', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('status', postgresql.ENUM('alive', 'dead', 'resting', name='character_status'), nullable=False),
    sa.Column('strength', sa.Integer(), nullable=False),
    sa.Column('agility', sa.Integer(), nullable=False),
    sa.Column('intelligence', sa.Integer(), nullable=False),
    sa.Column('fatigue', sa.Integer(), nullable=False),
    sa.Column('gold', sa.Integer(), nullable=False),
    sa.Column('inventory_slots', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('fatigue BETWEEN 0 AND 100', name='characters_fatigue_range'),
    sa.CheckConstraint('gold >= 0', name='characters_gold_non_negative'),
    sa.CheckConstraint('hp_current BETWEEN 0 AND hp_max', name='characters_hp_valid'),
    sa.CheckConstraint('level BETWEEN 1 AND 15', name='characters_level_range'),
    sa.CheckConstraint('mana_current BETWEEN 0 AND mana_max', name='characters_mana_valid'),
    sa.CheckConstraint('stamina_current BETWEEN 0 AND stamina_max', name='characters_stamina_valid'),
    sa.CheckConstraint('strength > 0 AND agility > 0 AND intelligence > 0', name='characters_stats_positive'),
    sa.ForeignKeyConstraint(['current_location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index('idx_characters_level', 'characters', ['level'], unique=False)
    op.create_index('idx_characters_name', 'characters', ['name'], unique=False)
    op.create_index(op.f('ix_characters_current_location_id'), 'characters', ['current_location_id'], unique=False)
    op.create_index(op.f('ix_characters_user_id'), 'characters', ['user_id'], unique=False)
    op.create_table('location_connections',
    sa.Column('from_location_id', sa.UUID(), nullable=False),
    sa.Column('to_location_id', sa.UUID(), nullable=False),
    sa.Column('distance', sa.Integer(), nullable=False),
    sa.Column('travel_difficulty', sa.Integer(), nullable=False),
    sa.CheckConstraint('from_location_id != to_location_id', name='no_self_connection'),
    sa.ForeignKeyConstraint(['from_location_id'], ['locations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_location_id'], ['locations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('from_location_id', 'to_location_id')
    )
    op.create_index('idx_connections_from', 'location_connections', ['from_location_id'], unique=False)
    op.create_index('idx_connections_to', 'location_connections', ['to_location_id'], unique=False)
    op.create_table('shop_items',
    sa.Column('location_id', sa.UUID(), nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=False),
    sa.Column('buy_price', sa.Integer(), nullable=False),
    sa.Column('sell_price', sa.Integer(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=True),
    sa.CheckConstraint('buy_price > 0 AND sell_price > 0', name='prices_positive'),
    sa.CheckConstraint('stock IS NULL OR stock >= 0', name='stock_valid'),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('location_id', 'item_id')
    )
    op.create_index('idx_shop_location', 'shop_items', ['location_id'], unique=False)
    op.create_table('character_memories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('memory_type', postgresql.ENUM('boss_defeat', 'ally_death', 'important_choice', 'discovery', 'quest_complete', 'level_up', 'unique_event', name='memory_type'), nullable=False),
    sa.Column('title', sa.String(length=150), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('importance', sa.Integer(), nullable=False),
    sa.Column('tags', sa.ARRAY(sa.Text()), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('importance BETWEEN 1 AND 5', name='memory_importance_range'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_memories_importance', 'character_memories', ['importance'], unique=False)
    op.create_index(op.f('ix_character_memories_character_id'), 'character_memories', ['character_id'], unique=False)
    op.create_table('character_quests',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('quest_id', sa.UUID(), nullable=False),
    sa.Column('status', postgresql.ENUM('active', 'completed', 'failed', 'cancelled', name='quest_status'), nullable=False),
    sa.Column('progress', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('accepted_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['quest_id'], ['quests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_character_quests_status', 'character_quests', ['status'], unique=False)
    op.create_index(op.f('ix_character_quests_character_id'), 'character_quests', ['character_id'], unique=False)
    op.create_table('combat_sessions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('enemy_id', sa.UUID(), nullable=True),
    sa.Column('enemy_name', sa.String(length=100), nullable=False),
    sa.Column('enemy_hp_current', sa.Integer(), nullable=False),
    sa.Column('enemy_hp_max', sa.Integer(), nullable=False),
    sa.Column('enemy_stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('current_turn', sa.Integer(), nullable=False),
    sa.Column('combat_log', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('result', sa.String(length=20), nullable=True),
    sa.Column('rewards', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('started_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.Column('ended_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['enemy_id'], ['enemies.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('character_id', 'is_active', name='combat_unique_active')
    )
    op.create_index('idx_combat_active', 'combat_sessions', ['is_active'], unique=False)
    op.create_index(op.f('ix_combat_sessions_character_id'), 'combat_sessions', ['character_id'], unique=False)
    op.create_table('game_logs',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('level', sa.String(length=10), nullable=False),
    sa.Column('component', sa.String(length=50), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('character_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_game_logs_character', 'game_logs', ['character_id'], unique=False)
    op.create_index('idx_game_logs_component', 'game_logs', ['component'], unique=False)
    op.create_index('idx_game_logs_level', 'game_logs', ['level'], unique=False)
    op.create_table('inventory',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('item_id', sa.UUID(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('durability', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('durability IS NULL OR durability >= 0', name='inventory_durability_valid'),
    sa.CheckConstraint('quantity > 0', name='inventory_quantity_positive'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('character_id', 'item_id', name='unique_stackable')
    )
    op.create_index('idx_inventory_character', 'inventory', ['character_id'], unique=False)
    op.create_index(op.f('ix_inventory_character_id'), 'inventory', ['character_id'], unique=False)
    op.create_index(op.f('ix_inventory_item_id'), 'inventory', ['item_id'], unique=False)
    op.create_table('transactions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('transaction_type', postgresql.ENUM('quest_reward', 'combat_reward', 'shop_buy', 'shop_sell', 'tavern_rest', 'repair', 'training', 'penalty', name='transaction_type'), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('reference_id', sa.UUID(), nullable=True),
    sa.Column('balance_after', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('amount != 0', name='transactions_amount_nonzero'),
    sa.CheckConstraint('balance_after >= 0', name='transactions_balance_nonnegative'),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_character_id'), 'transactions', ['character_id'], unique=False)
    op.create_table('equipment',
    sa.Column('character_id', sa.UUID(), nullable=False),
    sa.Column('slot', postgresql.ENUM('weapon', 'armor', 'helmet', 'gloves', 'boots', 'accessory', 'ring1', 'ring2', name='equipment_slot'), nullable=False),
    sa.Column('inventory_id', sa.UUID(), nullable=False),
    sa.Column('equipped_at', sa.DateTime(), server_default='now()', nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('character_id', 'slot'),
    sa.UniqueConstraint('inventory_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('equipment')
    op.drop_index(op.f('ix_transactions_character_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_inventory_item_id'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_character_id'), table_name='inventory')
    op.drop_index('idx_inventory_character', table_name='inventory')
    op.drop_table('inventory')
    op.drop_index('idx_game_logs_level', table_name='game_logs')
    op.drop_index('idx_game_logs_component', table_name='game_logs')
    op.drop_index('idx_game_logs_character', table_name='game_logs')
    op.drop_table('game_logs')
    op.drop_index(op.f('ix_combat_sessions_character_id'), table_name='combat_sessions')
    op.drop_index('idx_combat_active', table_name='combat_sessions')
    op.drop_table('combat_sessions')
    op.drop_index(op.f('ix_character_quests_character_id'), table_name='character_quests')
    op.drop_index('idx_character_quests_status', table_name='character_quests')
    op.drop_table('character_quests')
    op.drop_index(op.f('ix_character_memories_character_id'), table_name='character_memories')
    op.drop_index('idx_memories_importance', table_name='character_memories')
    op.drop_table('character_memories')
    op.drop_index('idx_shop_location', table_name='shop_items')
    op.drop_table('shop_items')
    op.drop_index('idx_connections_to', table_name='location_connections')
    op.drop_index('idx_connections_from', table_name='location_connections')
    op.drop_table('location_connections')
    op.drop_index(op.f('ix_characters_user_id'), table_name='characters')
    op.drop_index(op.f('ix_characters_current_location_id'), table_name='characters')
    op.drop_index('idx_characters_name', table_name='characters')
    op.drop_index('idx_characters_level', table_name='characters')
    op.drop_table('characters')
    op.drop_index(op.f('ix_users_vk_user_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('quests')
    op.drop_index('idx_locations_type', table_name='locations')
    op.drop_index('idx_locations_region', table_name='locations')
    op.drop_index('idx_locations_coords', table_name='locations')
    op.drop_table('locations')
    op.drop_table('items')
    op.drop_table('enemies')
    op.drop_table('ai_prompts')
    # ### end Alembic commands ###

```



### 8. `backend/app/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python

```



### 9. `backend/app/api/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 10. `backend/app/api/deps.py`

**Размер:** 0.9 KB

**Язык:** `python`



```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import async_session
from app.core.security import decode_token
from app.models.user import User

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = decode_token(credentials.credentials)
    user_id = payload.sub

    stmt = select(User).where(User.id == user_id, User.is_active == True)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or inactive")
    return user

```



### 11. `backend/app/api/router.py`

**Размер:** 0.1 KB

**Язык:** `python`



```python
from fastapi import APIRouter
from app.api.v1.router import v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")

```



### 12. `backend/app/api/v1/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 13. `backend/app/api/v1/auth.py`

**Размер:** 2.6 KB

**Язык:** `python`



```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user, security
from app.core.security import create_access_token, create_refresh_token
from app.core.vk_auth import validate_vk_init_data
from app.config import settings
from app.models.user import User
from app.schemas.auth import VKAuthRequest, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/vk", response_model=Token)
async def auth_vk(data: VKAuthRequest, db: AsyncSession = Depends(get_db)):
    """Авторизация через VK initData. Валидирует подпись, создаёт/находит пользователя, возвращает JWT."""
    vk_data = validate_vk_init_data(data.initData, settings.VK_APP_SECRET)
    vk_user_id = vk_data.get("user", {}).get("id")
    
    if not vk_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="vk_user_id not found in initData")

    vk_user_id_int = int(vk_user_id)

    stmt = select(User).where(User.vk_user_id == vk_user_id_int)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # SQLAlchemy 2.0 без MappedAsDataclass: создаём объект и устанавливаем поля
        user = User()
        user.vk_user_id = vk_user_id_int
        user.is_active = True
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token(user.id, user.vk_user_id)
    refresh_token = create_refresh_token(user.id, user.vk_user_id)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Получение данных текущего авторизованного пользователя."""
    return user

@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user)
):
    """Обновление пары access/refresh токенов."""
    # В продакшене здесь можно добавить проверку revocation списка или типа токена
    access_token = create_access_token(user.id, user.vk_user_id)
    refresh_token = create_refresh_token(user.id, user.vk_user_id)
    return Token(access_token=access_token, refresh_token=refresh_token)

```



### 14. `backend/app/api/v1/router.py`

**Размер:** 0.1 KB

**Язык:** `python`



```python
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router

v1_router = APIRouter()
v1_router.include_router(auth_router)

```



### 15. `backend/app/config.py`

**Размер:** 0.6 KB

**Язык:** `python`



```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legends of Elara"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7
    VK_APP_ID: str
    VK_APP_SECRET: str
    YANDEX_API_KEY: str
    YANDEX_FOLDER_ID: str
    API_DOMAIN: str = "api.chichekin-tech.ru"
    APP_DOMAIN: str = "app.chichekin-tech.ru"
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()

```



### 16. `backend/app/core/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 17. `backend/app/core/security.py`

**Размер:** 1.5 KB

**Язык:** `python`



```python
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from fastapi import HTTPException, status
from app.config import settings
from app.schemas.auth import TokenPayload

def create_access_token(subject: UUID, vk_user_id: int, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.JWT_EXPIRE_DAYS))
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "vk_user_id": vk_user_id
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(subject: UUID, vk_user_id: int, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=30))
    to_encode = {
        "sub": str(subject),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "vk_user_id": vk_user_id,
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

```



### 18. `backend/app/core/vk_auth.py`

**Размер:** 1.2 KB

**Язык:** `python`



```python
import hmac
import hashlib
import json
from urllib.parse import parse_qsl, unquote
from fastapi import HTTPException, status

def validate_vk_init_data(init_data: str, secret: str) -> dict:
    parsed = dict(parse_qsl(init_data))
    if "hash" not in parsed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing hash in initData")

    check_hash = parsed.pop("hash")
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    
    # Спецификация VK требует использования "VK Web App Verify" как ключа для HMAC
    secret_key = hmac.new(b"VK Web App Verify", secret.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, check_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid VK signature")

    if "user" in parsed:
        try:
            parsed["user"] = json.loads(unquote(parsed["user"]))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data in initData")
            
    return parsed

```



### 19. `backend/app/db/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python

```



### 20. `backend/app/db/base.py`

**Размер:** 0.8 KB

**Язык:** `python`



```python
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
```



### 21. `backend/app/db/session.py`

**Размер:** 0.3 KB

**Язык:** `python`



```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,  # Явно указываем класс сессии
    expire_on_commit=False
)

```



### 22. `backend/app/main.py`

**Размер:** 1.5 KB

**Язык:** `python`



```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.api.router import api_router
from sqlalchemy import text
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "https://vk.com", "https://*.vk.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected", "api": "running"}
    except Exception as e:
        return {"status": "error", "db": "disconnected", "detail": str(e)}

```



### 23. `backend/app/models/__init__.py`

**Размер:** 0.7 KB

**Язык:** `python`



```python
from app.db.base import Base
from app.models.user import User
from app.models.character import Character
from app.models.item import Item
from app.models.inventory import Inventory, Equipment
from app.models.location import Location, LocationConnection
from app.models.quest import Quest, CharacterQuest
from app.models.memory import CharacterMemory
from app.models.combat import Enemy, CombatSession
from app.models.shop import ShopItem, Transaction
from app.models.system import AiPrompt, GameLog

__all__ = [
    "Base", "User", "Character", "Item", "Inventory", "Equipment",
    "Location", "LocationConnection", "Quest", "CharacterQuest",
    "CharacterMemory", "Enemy", "CombatSession", "ShopItem", "Transaction",
    "AiPrompt", "GameLog"
]

```



### 24. `backend/app/models/character.py`

**Размер:** 3.2 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import CHARACTER_CLASS, CHARACTER_STATUS

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
    status: Mapped[str] = mapped_column(CHARACTER_STATUS, default="alive", nullable=False)
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

```



### 25. `backend/app/models/combat.py`

**Размер:** 2.9 KB

**Язык:** `python`



```python
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

```



### 26. `backend/app/models/enums.py`

**Размер:** 1.2 KB

**Язык:** `python`



```python
from sqlalchemy.dialects.postgresql import ENUM

def pg_enum(name: str, *values: str) -> ENUM:
    return ENUM(*values, name=name, create_type=True)

CHARACTER_CLASS = pg_enum('character_class',
    'warrior', 'priest', 'paladin', 'mage', 'summoner',
    'necromancer', 'barbarian', 'hunter', 'druid', 'rogue', 'werewolf'
)
ITEM_TYPE = pg_enum('item_type',
    'weapon', 'armor', 'accessory', 'consumable', 'quest_item', 'bag'
)
ITEM_RARITY = pg_enum('item_rarity',
    'common', 'uncommon', 'rare', 'epic', 'legendary'
)
EQUIPMENT_SLOT = pg_enum('equipment_slot',
    'weapon', 'armor', 'helmet', 'gloves', 'boots',
    'accessory', 'ring1', 'ring2'
)
LOCATION_TYPE = pg_enum('location_type',
    'city', 'forest', 'road', 'dungeon', 'cave', 'mountain', 'swamp'
)
QUEST_STATUS = pg_enum('quest_status',
    'active', 'completed', 'failed', 'cancelled'
)
TRANSACTION_TYPE = pg_enum('transaction_type',
    'quest_reward', 'combat_reward', 'shop_buy', 'shop_sell',
    'tavern_rest', 'repair', 'training', 'penalty'
)
MEMORY_TYPE = pg_enum('memory_type',
    'boss_defeat', 'ally_death', 'important_choice', 'discovery',
    'quest_complete', 'level_up', 'unique_event'
)
CHARACTER_STATUS = pg_enum('character_status',
    'alive', 'dead', 'resting'
)

```



### 27. `backend/app/models/inventory.py`

**Размер:** 1.9 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import EQUIPMENT_SLOT

class Inventory(Base, TimestampMixin):
    __tablename__ = "inventory"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="RESTRICT"), index=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    durability: Mapped[Optional[int]] = mapped_column(Integer)
    
    character: Mapped["Character"] = relationship("Character", back_populates="inventory")
    item: Mapped["Item"] = relationship("Item", back_populates="inventory_items")
    
    __table_args__ = (
        CheckConstraint("quantity > 0", name="inventory_quantity_positive"),
        CheckConstraint("durability IS NULL OR durability >= 0", name="inventory_durability_valid"),
        UniqueConstraint("character_id", "item_id", name="unique_stackable"),
        Index("idx_inventory_character", "character_id"),
    )

class Equipment(Base, TimestampMixin):
    __tablename__ = "equipment"
    
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True)
    slot: Mapped[str] = mapped_column(EQUIPMENT_SLOT, primary_key=True)
    inventory_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("inventory.id", ondelete="CASCADE"), unique=True)
    equipped_at: Mapped[datetime] = mapped_column(server_default="now()")
    
    inventory: Mapped["Inventory"] = relationship("Inventory")

```



### 28. `backend/app/models/item.py`

**Размер:** 1.8 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ARRAY, Boolean, CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import CHARACTER_CLASS, EQUIPMENT_SLOT, ITEM_RARITY, ITEM_TYPE

class Item(Base, TimestampMixin):
    __tablename__ = "items"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    item_type: Mapped[str] = mapped_column(ITEM_TYPE, nullable=False)
    rarity: Mapped[str] = mapped_column(ITEM_RARITY, default="common", nullable=False)
    base_cost: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sell_multiplier: Mapped[float] = mapped_column(Numeric(3,2), default=0.5, nullable=False)
    required_level: Mapped[Optional[int]] = mapped_column(Integer, default=1)
    required_class: Mapped[Optional[List[str]]] = mapped_column(ARRAY(CHARACTER_CLASS))
    modifiers: Mapped[dict] = mapped_column(JSONB, default={}, nullable=False)
    damage_min: Mapped[int] = mapped_column(Integer, default=0)
    damage_max: Mapped[int] = mapped_column(Integer, default=0)
    armor: Mapped[int] = mapped_column(Integer, default=0)
    max_durability: Mapped[int] = mapped_column(Integer, default=100)
    slot: Mapped[Optional[str]] = mapped_column(EQUIPMENT_SLOT)
    is_stackable: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    inventory_items: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="item")

```



### 29. `backend/app/models/location.py`

**Размер:** 2.3 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import LOCATION_TYPE

class Location(Base, TimestampMixin):
    __tablename__ = "locations"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location_type: Mapped[str] = mapped_column(LOCATION_TYPE, nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    coord_x: Mapped[int] = mapped_column(Integer, nullable=False)
    coord_y: Mapped[int] = mapped_column(Integer, nullable=False)
    danger_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    ai_description_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_safe: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_shop: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_tavern: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    __table_args__ = (
        Index("idx_locations_type", "location_type"),
        Index("idx_locations_region", "region"),
        Index("idx_locations_coords", "coord_x", "coord_y"),
    )

class LocationConnection(Base):
    __tablename__ = "location_connections"
    
    from_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    to_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    distance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    travel_difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    __table_args__ = (
        CheckConstraint("from_location_id != to_location_id", name="no_self_connection"),
        Index("idx_connections_from", "from_location_id"),
        Index("idx_connections_to", "to_location_id"),
    )

```



### 30. `backend/app/models/memory.py`

**Размер:** 1.2 KB

**Язык:** `python`



```python
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

```



### 31. `backend/app/models/quest.py`

**Размер:** 1.8 KB

**Язык:** `python`



```python
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
    
    __table_args__ = (
        Index("idx_character_quests_status", "status"),
    )

```



### 32. `backend/app/models/shop.py`

**Размер:** 1.9 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base, TimestampMixin
from app.models.enums import TRANSACTION_TYPE

class ShopItem(Base):
    __tablename__ = "shop_items"
    
    location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), primary_key=True)
    item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), primary_key=True)
    buy_price: Mapped[int] = mapped_column(Integer, nullable=False)
    sell_price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[Optional[int]] = mapped_column(Integer)
    
    __table_args__ = (
        CheckConstraint("buy_price > 0 AND sell_price > 0", name="prices_positive"),
        CheckConstraint("stock IS NULL OR stock >= 0", name="stock_valid"),
        Index("idx_shop_location", "location_id"),
    )

class Transaction(Base, TimestampMixin):
    __tablename__ = "transactions"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    character_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("characters.id", ondelete="CASCADE"), index=True)
    transaction_type: Mapped[str] = mapped_column(TRANSACTION_TYPE, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True))
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)
    
    __table_args__ = (
        CheckConstraint("amount != 0", name="transactions_amount_nonzero"),
        CheckConstraint("balance_after >= 0", name="transactions_balance_nonnegative"),
    )

```



### 33. `backend/app/models/system.py`

**Размер:** 1.7 KB

**Язык:** `python`



```python
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

```



### 34. `backend/app/models/user.py`

**Размер:** 0.7 KB

**Язык:** `python`



```python
import uuid
from datetime import datetime
from typing import List
from sqlalchemy import BigInteger, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vk_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="user", cascade="all, delete-orphan")

```



### 35. `backend/app/schemas/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 36. `backend/app/schemas/auth.py`

**Размер:** 0.7 KB

**Язык:** `python`



```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class VKAuthRequest(BaseModel):
    initData: str = Field(..., min_length=10, description="VK initData строка с подписью")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class TokenPayload(BaseModel):
    sub: uuid.UUID
    exp: datetime
    iat: datetime
    vk_user_id: int
    type: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    vk_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Pydantic V2 стиль
    model_config = {"from_attributes": True}

```



### 37. `backend/seeds/load_seeds.py`

**Размер:** 6.0 KB

**Язык:** `python`



```python
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

```



### 38. `nginx/conf.d/api.conf`

**Размер:** 0.4 KB

**Язык:** `ini`



```ini
server {
    listen 80;
    server_name _;
    location /health {
        return 200 'Nginx OK';
        add_header Content-Type text/plain;
    }
    location /api/ {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 10M;
    }
}

```



### 39. `nginx/nginx.conf`

**Размер:** 0.5 KB

**Язык:** `ini`



```ini
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;
events { worker_connections 1024; }
http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    sendfile on;
    keepalive_timeout 65;
    include /etc/nginx/conf.d/*.conf;
}

```



### 40. `scan_project.py`

**Размер:** 13.7 KB

**Язык:** `python`



```python
#!/usr/bin/env python3
"""
Скрипт для сканирования проекта и сохранения структуры с кодом в Markdown формате
"""

import os
import sys
from pathlib import Path
from typing import List, Set, Optional
from datetime import datetime


# Расширения файлов кода, которые нужно сканировать
CODE_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.java', '.cpp', '.c', '.h',
    '.hpp', '.cs', '.rb', '.php', '.go', '.rs', '.kt', '.swift', '.html',
    '.css', '.scss', '.sass', '.less', '.sql', '.sh', '.bash', '.md',
    '.env', '.yaml', '.yml', '.json', '.toml', '.ini', '.cfg', '.conf'
}

# Файлы и папки, которые нужно игнорировать
IGNORE_PATTERNS = {
    '__pycache__', '.git', '.idea', '.vscode', 'venv', 'env', 
    'node_modules', '.DS_Store', '.pytest_cache', '.mypy_cache',
    'dist', 'build', 'target', '.egg-info', '.tox'
}

# Маппинг расширений для подсветки синтаксиса в Markdown
LANGUAGE_MAPPING = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.rb': 'ruby',
    '.php': 'php',
    '.go': 'go',
    '.rs': 'rust',
    '.kt': 'kotlin',
    '.swift': 'swift',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.less': 'less',
    '.sql': 'sql',
    '.sh': 'bash',
    '.bash': 'bash',
    '.md': 'markdown',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.json': 'json',
    '.toml': 'toml',
    '.ini': 'ini',
    '.cfg': 'ini',
    '.conf': 'ini',
    '.txt': 'text',
    '.env': 'env',
    '.dockerfile': 'dockerfile'
}


class MarkdownBuilder:
    """Класс для построения Markdown документа"""
    
    def __init__(self):
        self.lines: List[str] = []
    
    def add_header(self, text: str, level: int = 1) -> None:
        """Добавить заголовок"""
        self.lines.append(f"{'#' * level} {text}\n")
    
    def add_paragraph(self, text: str) -> None:
        """Добавить параграф"""
        self.lines.append(f"{text}\n")
    
    def add_horizontal_rule(self) -> None:
        """Добавить горизонтальную линию"""
        self.lines.append("---\n")
    
    def add_code_block(self, code: str, language: str = "") -> None:
        """Добавить блок кода"""
        self.lines.append(f"```{language}")
        self.lines.append(code)
        self.lines.append("```\n")
    
    def add_unordered_list_item(self, text: str, indent: int = 0) -> None:
        """Добавить элемент списка"""
        prefix = "  " * indent + "- "
        self.lines.append(f"{prefix}{text}")
    
    def add_bold(self, text: str) -> str:
        """Добавить жирный текст"""
        return f"**{text}**"
    
    def add_italic(self, text: str) -> str:
        """Добавить курсив"""
        return f"*{text}*"
    
    def add_link(self, text: str, url: str) -> str:
        """Добавить ссылку"""
        return f"[{text}]({url})"
    
    def get_content(self) -> str:
        """Получить итоговый контент"""
        return "\n".join(self.lines)


def should_ignore(path: Path, base_path: Path) -> bool:
    """Проверяет, нужно ли игнорировать путь"""
    # Проверяем по имени
    if path.name in IGNORE_PATTERNS:
        return True
    
    # Особая обработка для .env:
    # - файл .env НЕ игнорируем (для анализа структуры)
    # - директорию .env игнорируем
    if path.name == '.env':
        if path.is_dir():
            return True  # Игнорируем директорию .env
        else:
            return False  # НЕ игнорируем файл .env
    
    # Проверяем скрытые файлы и папки (кроме некоторых)
    if path.name.startswith('.') and path.name not in ['.gitignore', '.env', '.env.example']:
        return True
    
    # Проверяем относительный путь
    try:
        rel_path = path.relative_to(base_path)
        parts = rel_path.parts
        if any(part in IGNORE_PATTERNS for part in parts):
            return True
    except ValueError:
        return True
    
    return False


def get_file_size_kb(file_path: Path) -> float:
    """Возвращает размер файла в килобайтах"""
    try:
        return file_path.stat().st_size / 1024
    except Exception:
        return 0


def get_language_for_file(file_path: Path) -> str:
    """Определяет язык для подсветки синтаксиса по расширению файла"""
    # Специальная обработка для файла .env (без расширения)
    if file_path.name == '.env' and not file_path.suffix:
        return 'env'
    
    ext = file_path.suffix.lower()
    return LANGUAGE_MAPPING.get(ext, "")


def build_tree_structure(path: Path, base_path: Path, indent: int = 0) -> List[str]:
    """
    Рекурсивно строит структуру директории для Markdown
    
    Возвращает список строк для добавления в список
    """
    result = []
    
    # Определяем префикс для текущего уровня
    prefix = "  " * indent
    
    if path.is_file():
        size_kb = get_file_size_kb(path)
        file_name = path.name
        
        # Особая обработка для .env файла - скрываем чувствительные данные
        if file_name == '.env':
            result.append(f"{prefix}- `{file_name}` ({size_kb:.1f} KB) 📝")
        else:
            result.append(f"{prefix}- `{file_name}` ({size_kb:.1f} KB)")
    else:
        dir_name = path.name if path != base_path else path.name + "/"
        result.append(f"{prefix}- **{dir_name}/**")
    
    # Если это директория, обрабатываем её содержимое
    if path.is_dir():
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            items = [item for item in items if not should_ignore(item, base_path)]
            
            for item in items:
                result.extend(build_tree_structure(item, base_path, indent + 1))
        except PermissionError:
            result.append(f"{prefix}  - [Permission Denied]")
    
    return result


def read_file_content(file_path: Path) -> Optional[str]:
    """Читает содержимое файла с обработкой ошибок"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Если это .env файл, заменяем значения на [REDACTED] для безопасности
            if file_path.name == '.env':
                lines = content.split('\n')
                processed_lines = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        processed_lines.append(line)
                    elif '=' in line:
                        key, _ = line.split('=', 1)
                        processed_lines.append(f"{key}=[REDACTED]")
                    else:
                        processed_lines.append(line)
                content = '\n'.join(processed_lines)
            
            return content
    except UnicodeDecodeError:
        return f"[Бинарный файл или ошибка кодировки: {file_path.name}]"
    except Exception as e:
        return f"[Ошибка чтения файла: {e}]"


def scan_project_to_markdown(project_path: str = ".", output_file: Optional[str] = None) -> str:
    """
    Сканирует проект и возвращает содержимое в формате Markdown
    
    Args:
        project_path: Путь к проекту
        output_file: Путь к выходному файлу (если None, возвращает строку)
    
    Returns:
        Содержимое в формате Markdown
    """
    base_path = Path(project_path).resolve()
    
    if not base_path.exists():
        raise FileNotFoundError(f"Директория не существует: {base_path}")
    
    if not base_path.is_dir():
        raise NotADirectoryError(f"Указанный путь не является директорией: {base_path}")
    
    # Создаем строитель Markdown
    md = MarkdownBuilder()
    
    # Заголовок документа
    project_name = base_path.name
    md.add_header(f"Структура проекта: {project_name}", level=1)
    md.add_paragraph(f"*Сгенерировано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    md.add_paragraph(f"*Путь: `{base_path}`*")
    md.add_horizontal_rule()
    
    # Раздел: Структура проекта
    md.add_header("Структура проекта", level=2)
    md.add_paragraph("Дерево файлов и директорий проекта:")
    md.add_paragraph("")
    
    # Строим структуру дерева
    tree_lines = build_tree_structure(base_path, base_path)
    for line in tree_lines:
        md.lines.append(line)
    
    md.add_paragraph("")
    md.add_horizontal_rule()
    
    # Собираем все файлы кода
    code_files: List[Path] = []
    
    for root, dirs, files in os.walk(base_path):
        # Фильтруем директории для игнорирования
        dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d, base_path)]
        
        for file in files:
            file_path = Path(root) / file
            # Проверяем по расширению ИЛИ по имени файла (.env без расширения)
            if (file_path.suffix in CODE_EXTENSIONS or file_path.name in ['.env', '.env.example']) \
               and not should_ignore(file_path, base_path):
                code_files.append(file_path)
    
    # Раздел: Файлы кода
    md.add_header("Файлы кода", level=2)
    md.add_paragraph(f"Найдено файлов кода: **{len(code_files)}**")
    md.add_paragraph("")
    
    if not code_files:
        md.add_paragraph("*Файлы кода не найдены.*")
    else:
        # Выводим содержимое каждого файла кода
        for i, file_path in enumerate(sorted(code_files, key=lambda x: str(x.relative_to(base_path))), 1):
            rel_path = file_path.relative_to(base_path)
            file_name = file_path.name
            size_kb = get_file_size_kb(file_path)
            language = get_language_for_file(file_path)
            
            md.add_header(f"{i}. `{rel_path}`", level=3)
            md.add_paragraph(f"**Размер:** {size_kb:.1f} KB")
            if language:
                md.add_paragraph(f"**Язык:** `{language}`")
            
            # Предупреждение для .env файлов
            if file_name == '.env':
                md.add_paragraph("⚠️ **Внимание:** Значения переменных окружения скрыты для безопасности.")
            
            md.add_paragraph("")
            
            # Читаем и добавляем код
            content = read_file_content(file_path)
            md.add_code_block(content, language)
            md.add_paragraph("")
    
    md.add_horizontal_rule()
    md.add_paragraph(f"*Всего файлов кода: {len(code_files)}*")
    
    # Получаем итоговый контент
    content = md.get_content()
    
    # Сохраняем в файл, если указан путь
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Отчет сохранен в: {output_path.absolute()}")
        print(f"📊 Найдено файлов кода: {len(code_files)}")
    
    return content


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Сканирование проекта и сохранение структуры с кодом в Markdown формате"
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Путь к проекту (по умолчанию: текущая директория)"
    )
    parser.add_argument(
        "-o", "--output",
        default="project_structure.md",
        help="Путь к выходному файлу (по умолчанию: project_structure.md)"
    )
    parser.add_argument(
        "-p", "--print",
        action="store_true",
        help="Также вывести результат в консоль"
    )
    parser.add_argument(
        "--no-redact",
        action="store_true",
        help="Не скрывать значения в .env файлах (ОСТОРОЖНО!)"
    )
    
    args = parser.parse_args()
    
    try:
        content = scan_project_to_markdown(args.project_path, args.output)
        
        if args.print:
            print("\n" + "="*80)
            print(content)
            print("="*80)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
```



---

*Всего файлов кода: 40*
