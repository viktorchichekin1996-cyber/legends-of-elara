# Структура проекта: legends-of-elara

*Сгенерировано: 2026-04-12 11:35:41*

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
      - **ai/**
        - `__init__.py` (0.8 KB)
        - `cache.py` (1.2 KB)
        - `client.py` (2.2 KB)
        - `fallback.py` (1.3 KB)
        - `parser.py` (1.3 KB)
        - `prompts.py` (4.7 KB)
      - **api/**
        - **v1/**
          - `__init__.py` (0.0 KB)
          - `auth.py` (2.6 KB)
          - `character.py` (5.8 KB)
          - `combat.py` (6.2 KB)
          - `locations.py` (2.7 KB)
          - `router.py` (0.4 KB)
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
        - `character.py` (2.1 KB)
        - `combat.py` (2.4 KB)
        - `enums.py` (1.2 KB)
        - `location.py` (1.3 KB)
      - **services/**
        - `character_service.py` (6.5 KB)
        - `combat_service.py` (17.0 KB)
        - `location_service.py` (7.3 KB)
      - **utils/**
        - `calculations.py` (1.7 KB)
        - `constants.py` (2.2 KB)
        - `dice.py` (1.4 KB)
      - `__init__.py` (0.0 KB)
      - `config.py` (0.6 KB)
      - `main.py` (1.8 KB)
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
    - **public/**
      - `index.html` (1.6 KB)
  - **nginx/**
    - **conf.d/**
      - `api.conf` (0.4 KB)
      - `app.conf` (0.0 KB)
    - **ssl/**
    - `nginx.conf` (0.5 KB)
  - `.env` (0.5 KB) 📝
  - `.env.example` (0.7 KB)
  - `.gitignore` (0.6 KB)
  - `README.md` (0.5 KB)
  - `scan_project.py` (13.7 KB)


---

## Файлы кода

Найдено файлов кода: **61**



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



### 9. `backend/app/ai/__init__.py`

**Размер:** 0.8 KB

**Язык:** `python`



```python
"""Модуль интеграции с YandexGPT."""
from .client import YandexGPTClient
from .cache import PromptCache
from .parser import AiEventResponse, parse_ai_response
from .prompts import build_character_context, format_prompt
from .fallback import get_fallback_event

_gpt_client = None
_prompt_cache = None

def get_gpt_client() -> YandexGPTClient:
    global _gpt_client
    if _gpt_client is None:
        _gpt_client = YandexGPTClient()
    return _gpt_client

def get_prompt_cache() -> PromptCache:
    global _prompt_cache
    if _prompt_cache is None:
        _prompt_cache = PromptCache()
    return _prompt_cache

__all__ = [
    "get_gpt_client", "get_prompt_cache",
    "build_character_context", "format_prompt",
    "parse_ai_response", "AiEventResponse",
    "get_fallback_event"
]

```



### 10. `backend/app/ai/cache.py`

**Размер:** 1.2 KB

**Язык:** `python`



```python
import hashlib
import json
import logging
import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger(__name__)

class PromptCache:
    """Redis-кэш для промптов и ответов YandexGPT."""
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client = aioredis.from_url(self.redis_url, decode_responses=True)
        self.ttl = 3600  # 1 час

    async def get(self, prompt_hash: str) -> str | None:
        try:
            return await self.client.get(f"ai:prompt:{prompt_hash}")
        except Exception as e:
            logger.error(f"Redis cache GET error: {e}")
            return None

    async def set(self, prompt_hash: str, response: str) -> None:
        try:
            await self.client.set(f"ai:prompt:{prompt_hash}", response, ex=self.ttl)
        except Exception as e:
            logger.error(f"Redis cache SET error: {e}")

    def hash_prompt(self, prompt_data: list[dict]) -> str:
        content = json.dumps(prompt_data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def close(self):
        await self.client.close()

```



### 11. `backend/app/ai/client.py`

**Размер:** 2.2 KB

**Язык:** `python`



```python
import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class YandexGPTClient:
    """Асинхронный клиент для YandexGPT (yandexgpt-lite/latest)."""
    def __init__(self):
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Authorization": f"Api-Key {settings.YANDEX_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model_uri = f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite/latest"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def generate(self, messages: list[dict[str, str]], temperature: float = 0.7, max_tokens: int = 1500) -> str:
        payload = {
            "model_uri": self.model_uri,
            "completion_options": {"temperature": temperature, "max_tokens": max_tokens},
            "messages": messages
        }
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.post(self.base_url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["result"]["alternatives"][0]["message"]["text"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning(f"YandexGPT rate limit (429). Retry {attempt+1}/{max_retries} after {wait}s")
                    import asyncio
                    await asyncio.sleep(wait)
                    continue
                logger.error(f"YandexGPT HTTP Error {e.response.status_code}: {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"YandexGPT Network Error: {e}")
                if attempt == max_retries - 1:
                    raise
                import asyncio
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"YandexGPT Unexpected Error: {e}")
                raise
        raise RuntimeError("YandexGPT generation failed after retries")

    async def close(self):
        await self.client.aclose()

```



### 12. `backend/app/ai/fallback.py`

**Размер:** 1.3 KB

**Язык:** `python`



```python
import random
import logging
from app.ai.parser import AiEventResponse, Choice

logger = logging.getLogger(__name__)

FALLBACK_EVENTS = [
    AiEventResponse(
        description="Тропа петляет среди древних деревьев. Ветер доносит запах сырости и далёкий гул.",
        choices=[
            Choice(text="Идти на звук", action="move"),
            Choice(text="Осмотреть тропу", action="interact"),
            Choice(text="Свернуть в чащу", action="travel")
        ]
    ),
    AiEventResponse(
        description="Старый указатель раскачивается на ветру. Надпись почти стёрлась, но читается слово 'Осторожно'.",
        choices=[
            Choice(text="Обойти стороной", action="travel"),
            Choice(text="Проверить экипировку", action="interact"),
            Choice(text="Устроить привал", action="rest")
        ]
    )
]

def get_fallback_event(character_class: str, location_type: str) -> AiEventResponse:
    """Возвращает безопасное событие при сбое ИИ."""
    logger.warning("AI generation failed. Using fallback event.")
    return random.choice(FALLBACK_EVENTS)

```



### 13. `backend/app/ai/parser.py`

**Размер:** 1.3 KB

**Язык:** `python`



```python
import re
import json
import logging
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class Choice(BaseModel):
    text: str
    action: str

class AiEventResponse(BaseModel):
    type: str = "event"
    description: str
    choices: list[Choice]
    mood: str | None = None

async def parse_ai_response(raw_text: str, max_retries: int = 2) -> AiEventResponse:
    """Извлекает и валидирует JSON из ответа ИИ."""
    # Попытка найти JSON внутри markdown блоков ```json ... ```
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
    json_str = json_match.group(1) if json_match else raw_text

    for attempt in range(max_retries + 1):
        try:
            data = json.loads(json_str)
            return AiEventResponse(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"AI parse attempt {attempt+1} failed: {e}")
            if attempt == max_retries:
                raise ValueError(f"Failed to parse AI response: {e}")
            # В реальном сценарии здесь можно отправить запрос на исправление,
            # но для оптимизации переходим к fallback на уровне сервиса.
            raise

```



### 14. `backend/app/ai/prompts.py`

**Размер:** 4.7 KB

**Язык:** `python`



```python
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.character import Character
from app.models.location import Location
from app.models.quest import CharacterQuest, Quest
from app.models.memory import CharacterMemory

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты — нейросетевой движок событий для текстовой RPG "Легенды Элары".
Правила вывода:
1. Ответ СТРОГО в формате JSON. Никакого markdown, никаких пояснений вне JSON.
2. Схема: {"description": "атмосферное описание события", "choices": [{"text": "вариант", "action": "тип_действия"}]}
3. Допустимые action: "move", "fight", "rest", "interact", "loot", "travel", "shop", "tavern".
4. Учитывай класс, уровень, опасность локации, активные квесты и память.
5. Тон: тёмное фэнтези, погружение в мир Элары.
6. Генерируй 2-4 варианта выбора.
"""

async def build_character_context(session: AsyncSession, character_id: str) -> dict:
    """Собирает контекст персонажа для промпта."""
    stmt = select(Character).where(Character.id == character_id)
    char = (await session.execute(stmt)).scalar_one_or_none()
    if not char:
        raise ValueError("Character not found")

    loc_stmt = select(Location).where(Location.id == char.current_location_id)
    loc = (await session.execute(loc_stmt)).scalar_one_or_none()

    quests_stmt = (
        select(Quest.name, CharacterQuest.status)
        .join(CharacterQuest, Quest.id == CharacterQuest.quest_id)
        .where(CharacterQuest.character_id == char.id, CharacterQuest.status == "active")
        .limit(3)
    )
    quests_res = (await session.execute(quests_stmt)).fetchall()
    active_quests = [f"{q.name} ({status})" for q, status in quests_res]

    mem_stmt = (
        select(CharacterMemory.title, CharacterMemory.description)
        .where(CharacterMemory.character_id == char.id)
        .order_by(CharacterMemory.importance.desc())
        .limit(3)
    )
    mem_res = (await session.execute(mem_stmt)).fetchall()
    memories = [f"{t}: {d}" for t, d in mem_res]

    return {
        "name": char.name,
        "class": char.character_class,
        "level": char.level,
        "hp": f"{char.hp_current}/{char.hp_max}",
        "location_name": loc.name if loc else "Неизвестно",
        "location_type": loc.location_type if loc else "unknown",
        "danger_level": loc.danger_level if loc else 1,
        "quests": active_quests,
        "memories": memories,
    }

def format_prompt(context: dict, user_action: str) -> list[dict]:
    """Формирует сообщения для API YandexGPT."""
    context_str = (
        f"Персонаж: {context['name']} ({context['class']}, ур. {context['level']})\n"
        f"HP: {context['hp']}\n"
        f"Локация: {context['location_name']} ({context['location_type']}, опасность {context['danger_level']})\n"
        f"Квесты: {', '.join(context['quests']) or 'Нет'}\n"
        f"Память: {', '.join(context['memories']) or 'Пусто'}\n"
        f"Действие игрока: {user_action}"
    )
    return [
        {"role": "system", "text": SYSTEM_PROMPT},
        {"role": "user", "text": context_str}
    ]

COMBAT_NARRATIVE_PROMPT = """
Ты — мастер подземелий в мрачном фэнтези мире "Легенды Элары".
Твоя задача: создать короткое, атмосферное описание (нарратив) результата хода в бою.

Контекст боя:
- Персонаж: {char_name} ({char_class}, ур. {char_level})
- Враг: {enemy_name}
- Текущее действие: {action_type}
- Результат: {result_desc}
- Урон: {damage} HP
- Состояние: Враг {enemy_hp}/{enemy_max} HP, Герой {char_hp}/{char_max} HP

Правила:
1. Стиль: Тёмное фэнтези, серьёзный, кинематографичный.
2. Длина: 1-2 предложения (не больше 150 символов).
3. Не повторяй сухие цифры, опиши эффект (свист ветра, хруст, вспышка).
4. Если промах: опиши ловкое уклонение или неудачный удар.
5. Если крит: опиши сокрушительный удар.
6. Язык: Русский.
7. Вывод: ТОЛЬКО текст описания, без кавычек и пояснений.
"""

```



### 15. `backend/app/api/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 16. `backend/app/api/deps.py`

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



### 17. `backend/app/api/router.py`

**Размер:** 0.1 KB

**Язык:** `python`



```python
from fastapi import APIRouter
from app.api.v1.router import v1_router

api_router = APIRouter()
api_router.include_router(v1_router, prefix="/v1")

```



### 18. `backend/app/api/v1/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 19. `backend/app/api/v1/auth.py`

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



### 20. `backend/app/api/v1/character.py`

**Размер:** 5.8 KB

**Язык:** `python`



```python
"""Эндпоинты управления персонажем."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location
from app.models.enums import CHARACTER_CLASS as DB_CHARACTER_CLASS
from app.schemas.character import (
    CharacterCreateRequest,
    CharacterResponse,
    CharacterStatsResponse,
    LevelUpResponse,
)
from app.schemas.enums import CharacterClass
from app.services.character_service import (
    create_character,
    calculate_character_stats,
    calculate_character_resources,
    check_action_allowed,
    apply_level_up,
)
from app.utils.calculations import get_xp_for_level, get_next_level_xp, check_level_up

router = APIRouter(prefix="/character", tags=["Character"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_character_endpoint(
    request: CharacterCreateRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterResponse:
    """Создание нового персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть персонаж"
        )
    
    character = await create_character(db, str(current_user.id), request)
    await db.commit()
    await db.refresh(character)
    
    location_result = await db.execute(
        select(Location).where(Location.id == character.current_location_id)
    )
    location = location_result.scalar_one_or_none()
    
    return CharacterResponse(
        id=character.id,
        name=character.name,
        character_class=CharacterClass(character.character_class),
        level=character.level,
        experience=character.experience,
        status=character.status,
        current_location_id=character.current_location_id,
        current_location_name=location.name if location else None,
        stats=calculate_character_stats(character),
        resources=calculate_character_resources(character),
        created_at=character.created_at,
        updated_at=character.updated_at,
    )

@router.get("/", response_model=CharacterResponse)
async def get_character(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterResponse:
    """Получение полного состояния персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден. Создайте персонажа."
        )
    
    location_result = await db.execute(
        select(Location).where(Location.id == character.current_location_id)
    )
    location = location_result.scalar_one_or_none()
    
    return CharacterResponse(
        id=character.id,
        name=character.name,
        character_class=CharacterClass(character.character_class),
        level=character.level,
        experience=character.experience,
        status=character.status,
        current_location_id=character.current_location_id,
        current_location_name=location.name if location else None,
        stats=calculate_character_stats(character),
        resources=calculate_character_resources(character),
        created_at=character.created_at,
        updated_at=character.updated_at,
    )

@router.get("/stats", response_model=CharacterStatsResponse)
async def get_character_stats(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterStatsResponse:
    """Получение характеристик персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )
    
    return calculate_character_stats(character)

@router.post("/levelup", response_model=LevelUpResponse)
async def level_up_character(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LevelUpResponse:
    """Обработка повышения уровня персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )
    
    leveled_up, new_level = check_level_up(character.experience, character.level)
    
    if not leveled_up:
        next_xp = get_next_level_xp(character.level)
        current_xp_for_level = character.experience - get_xp_for_level(character.level)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недостаточно опыта. Нужно ещё {next_xp - current_xp_for_level} XP"
        )
    
    old_level = character.level
    character.level = new_level
    stats_increased = await apply_level_up(character)
    
    await db.commit()
    
    return LevelUpResponse(
        level=new_level,
        new_experience=character.experience,
        stats_increased=stats_increased,
        resources_restored=True,
        message=f"Поздравляем! Вы достигли {new_level} уровня!"
    )

```



### 21. `backend/app/api/v1/combat.py`

**Размер:** 6.2 KB

**Язык:** `python`



```python
"""Эндпоинты боевой системы."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.combat import CombatSession
from app.schemas.combat import (
    CombatActionRequest,
    CombatActionResult,
    CombatStateResponse,
    CombatStartRequest,
)
from app.services.combat_service import (
    start_combat,
    get_active_combat,
    get_combat_state,
    process_player_attack,
    process_enemy_turn,
)

router = APIRouter(prefix="/combat", tags=["Combat"])

@router.post("/start", response_model=CombatStateResponse)
async def start_combat_endpoint(
    request: CombatStartRequest = CombatStartRequest(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatStateResponse:
    """Начало боя с врагом."""
    # Получаем персонажа
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    # Проверяем, нет ли уже активного боя
    existing = await get_active_combat(db, str(character.id))
    if existing:
        return await get_combat_state(db, existing, character)
    
    # Начинаем бой
    combat = await start_combat(db, str(character.id), request.enemy_id)
    await db.commit()
    
    return await get_combat_state(db, combat, character)

@router.get("/state", response_model=CombatStateResponse)
async def get_combat_state_endpoint(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatStateResponse:
    """Получение текущего состояния боя."""
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    combat = await get_active_combat(db, str(character.id))
    if not combat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active combat session"
        )
    
    return await get_combat_state(db, combat, character)

@router.post("/action", response_model=CombatActionResult)
async def combat_action_endpoint(
    request: CombatActionRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatActionResult:
    """Выполнение действия в бою."""
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    combat = await get_active_combat(db, str(character.id))
    if not combat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active combat session"
        )
    
    # Обработка действий
    if request.action == "attack":
        result = await process_player_attack(db, combat, character)
    elif request.action == "defend":
        # Упрощённая защита: снижение урона на 50% в следующем ходе врага
        result = CombatActionResult(
            success=True,
            message="Вы заняли оборонительную позицию. Следующая атака врага будет слабее."
        )
    elif request.action == "use_item":
        # Упрощённо: использование зелья
        if request.item_id:
            result = CombatActionResult(
                success=True,
                message="Вы использовали предмет. (Реализация предметов — Этап 8)"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="item_id required for use_item action"
            )
    elif request.action == "flee":
        # Упрощённый побег: 50% шанс
        import random
        if random.random() > 0.5:
            result = await process_enemy_turn(db, combat, character)
            if not result.battle_ended:
                result.message += " | Побег не удался!"
        else:
            combat.is_active = False
            combat.result = "fled"
            await db.flush()
            result = CombatActionResult(
                success=True,
                message="Вы успешно сбежали из боя!",
                battle_ended=True,
                battle_result="fled"
            )
    elif request.action == "skill":
        result = CombatActionResult(
            success=True,
            message="Навыки будут реализованы на следующем этапе."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown action"
        )
    
    # Если бой не закончен — ход врага
    if not result.battle_ended and request.action == "attack":
        enemy_result = await process_enemy_turn(db, combat, character)
        result.player_damage_taken = enemy_result.player_damage_taken
        result.message += f" | {enemy_result.message}"
        if enemy_result.battle_ended:
            result.battle_ended = True
            result.battle_result = enemy_result.battle_result
    
    await db.commit()
    
    # Обновляем состояние боя в ответе
    if not result.battle_ended:
        updated_combat = await get_active_combat(db, str(character.id))
        if updated_combat:
            result.combat_state = await get_combat_state(db, updated_combat, character)
    
    return result

```



### 22. `backend/app/api/v1/locations.py`

**Размер:** 2.7 KB

**Язык:** `python`



```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location, LocationConnection
from app.schemas.location import (
    LocationResponse,
    NeighborLocationResponse,
    MoveRequest,
    MoveResponse,
)
from app.services.location_service import (
    get_neighbors,
    move_character,
)

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/current", response_model=LocationResponse)
async def get_current_location_endpoint(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    result = await db.execute(
        select(Location)
        .join(Character, Character.current_location_id == Location.id)
        .where(Character.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character or location not found")
    
    return LocationResponse.model_validate(location)

@router.get("/neighbors", response_model=list[NeighborLocationResponse])
async def get_neighbor_locations(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[NeighborLocationResponse]:
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    neighbors = await get_neighbors(db, str(character.current_location_id))
    
    return [
        NeighborLocationResponse(
            id=n.id,
            name=n.name,
            location_type=n.location_type,
            distance=1,
            travel_difficulty=1,
            danger_level=n.danger_level,
            is_visited=False,
        )
        for n in neighbors
    ]

@router.post("/move", response_model=MoveResponse)
async def move_to_location(
    request: MoveRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MoveResponse:
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    result = await move_character(
        db,
        str(character.id),
        str(request.target_location_id)
    )
    
    await db.commit()
    
    return result

```



### 23. `backend/app/api/v1/router.py`

**Размер:** 0.4 KB

**Язык:** `python`



```python
from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.character import router as character_router
from app.api.v1.combat import router as combat_router
from app.api.v1.locations import router as locations_router

v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(character_router)
v1_router.include_router(combat_router)
v1_router.include_router(locations_router)

```



### 24. `backend/app/config.py`

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



### 25. `backend/app/core/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 26. `backend/app/core/security.py`

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



### 27. `backend/app/core/vk_auth.py`

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



### 28. `backend/app/db/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python

```



### 29. `backend/app/db/base.py`

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



### 30. `backend/app/db/session.py`

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



### 31. `backend/app/main.py`

**Размер:** 1.8 KB

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
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan
)

# CORS Middleware (разрешаем VK и фронтенд)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "https://vk.com", "https://*.vk.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    print(f"{request.method} {request.url.path} -> {response.status_code}")
    return response

# Глобальный обработчик исключений
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# Подключение API роутеров (ЗДЕСЬ ОШИБКА БЫЛА РАНЕЕ: роутер не был подключен)
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



### 32. `backend/app/models/__init__.py`

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



### 33. `backend/app/models/character.py`

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



### 34. `backend/app/models/combat.py`

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



### 35. `backend/app/models/enums.py`

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



### 36. `backend/app/models/inventory.py`

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



### 37. `backend/app/models/item.py`

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



### 38. `backend/app/models/location.py`

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



### 39. `backend/app/models/memory.py`

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



### 40. `backend/app/models/quest.py`

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



### 41. `backend/app/models/shop.py`

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



### 42. `backend/app/models/system.py`

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



### 43. `backend/app/models/user.py`

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



### 44. `backend/app/schemas/__init__.py`

**Размер:** 0.0 KB

**Язык:** `python`



```python


```



### 45. `backend/app/schemas/auth.py`

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



### 46. `backend/app/schemas/character.py`

**Размер:** 2.1 KB

**Язык:** `python`



```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid
from app.schemas.enums import CharacterClass, CharacterStatus

class CharacterCreateRequest(BaseModel):
    """Запрос на создание персонажа."""
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$")
    character_class: CharacterClass

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v.lower() in ['admin', 'moderator', 'gm', 'god']:
            raise ValueError('Имя зарезервировано')
        return v.strip().title()

class CharacterStatsResponse(BaseModel):
    """Характеристики персонажа с модификаторами."""
    strength: int
    agility: int
    intelligence: int
    strength_mod: int
    agility_mod: int
    intelligence_mod: int
    strength_effective: int
    agility_effective: int
    intelligence_effective: int
    
    model_config = {"from_attributes": True}

class CharacterResourcesResponse(BaseModel):
    """Ресурсы персонажа."""
    hp_current: int
    hp_max: int
    mana_current: int
    mana_max: int
    stamina_current: int
    stamina_max: int
    fatigue: int
    gold: int
    inventory_slots: int
    inventory_slots_used: Optional[int] = None
    
    model_config = {"from_attributes": True}

class CharacterResponse(BaseModel):
    """Полное состояние персонажа."""
    id: uuid.UUID
    name: str
    character_class: CharacterClass
    level: int
    experience: int
    status: CharacterStatus
    current_location_id: uuid.UUID
    current_location_name: Optional[str] = None
    stats: CharacterStatsResponse
    resources: CharacterResourcesResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class LevelUpResponse(BaseModel):
    """Ответ на повышение уровня."""
    level: int
    new_experience: int
    stats_increased: dict
    resources_restored: bool
    message: str
    
    model_config = {"from_attributes": True}

```



### 47. `backend/app/schemas/combat.py`

**Размер:** 2.4 KB

**Язык:** `python`



```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import uuid
from app.schemas.enums import CharacterClass

class CombatActionRequest(BaseModel):
    """Запрос на действие в бою."""
    action: str = Field(..., pattern="^(attack|defend|use_item|flee|skill)$")
    target: Optional[str] = None  # Для навыков с выбором цели
    item_id: Optional[uuid.UUID] = None  # Для использования предметов
    skill_name: Optional[str] = None  # Для использования навыков
    
    @field_validator('action')
    @classmethod
    def validate_action(cls, v: str) -> str:
        if v not in ('attack', 'defend', 'use_item', 'flee', 'skill'):
            raise ValueError('Недопустимое действие')
        return v

class CombatLogEntry(BaseModel):
    """Запись в логе боя."""
    turn: int
    actor: str  # "player" или "enemy"
    action: str
    description: str
    damage: Optional[int] = None
    healing: Optional[int] = None
    is_critical: bool = False
    is_miss: bool = False
    
    model_config = {"from_attributes": True}

class CombatStateResponse(BaseModel):
    """Текущее состояние боя."""
    combat_session_id: uuid.UUID
    enemy_name: str
    enemy_level: int
    enemy_hp_current: int
    enemy_hp_max: int
    player_hp_current: int
    player_hp_max: int
    player_mana_current: int
    player_mana_max: int
    current_turn: int
    is_player_turn: bool
    combat_log: List[CombatLogEntry]
    
    model_config = {"from_attributes": True}

class CombatActionResult(BaseModel):
    """Результат действия в бою."""
    success: bool
    message: str
    player_damage_taken: int = 0
    enemy_damage_taken: int = 0
    player_healing_received: int = 0
    is_critical: bool = False
    is_miss: bool = False
    combat_state: Optional[CombatStateResponse] = None
    battle_ended: bool = False
    battle_result: Optional[str] = None  # "victory", "defeat", "fled"
    rewards: Optional[dict] = None
    
    model_config = {"from_attributes": True}

class CombatStartRequest(BaseModel):
    """Запрос на начало боя (для тестов)."""
    enemy_id: Optional[uuid.UUID] = None  # Если не указан, выбирается случайный по уровню

```



### 48. `backend/app/schemas/enums.py`

**Размер:** 1.2 KB

**Язык:** `python`



```python
"""Нативные Python Enum для Pydantic схем."""
import enum

class CharacterClass(str, enum.Enum):
    WARRIOR = "warrior"
    PRIEST = "priest"
    PALADIN = "paladin"
    MAGE = "mage"
    SUMMONER = "summoner"
    NECROMANCER = "necromancer"
    BARBARIAN = "barbarian"
    HUNTER = "hunter"
    DRUID = "druid"
    ROGUE = "rogue"
    WEREWOLF = "werewolf"

class CharacterStatus(str, enum.Enum):
    ALIVE = "alive"
    DEAD = "dead"
    RESTING = "resting"

class LocationType(str, enum.Enum):
    CITY = "city"
    FOREST = "forest"
    ROAD = "road"
    DUNGEON = "dungeon"
    CAVE = "cave"
    MOUNTAIN = "mountain"
    SWAMP = "swamp"

class ItemType(str, enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    QUEST_ITEM = "quest_item"
    BAG = "bag"

class ItemRarity(str, enum.Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class EquipmentSlot(str, enum.Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    HELMET = "helmet"
    GLOVES = "gloves"
    BOOTS = "boots"
    ACCESSORY = "accessory"
    RING1 = "ring1"
    RING2 = "ring2"

```



### 49. `backend/app/schemas/location.py`

**Размер:** 1.3 KB

**Язык:** `python`



```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid
from app.schemas.enums import LocationType

class LocationResponse(BaseModel):
    """Информация о локации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    region: str
    coord_x: int
    coord_y: int
    danger_level: int
    min_level: int
    description: Optional[str] = None
    ai_description_generated: bool
    is_safe: bool
    has_shop: bool
    has_tavern: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

class NeighborLocationResponse(BaseModel):
    """Соседняя локация для навигации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    distance: int
    travel_difficulty: int
    danger_level: int
    is_visited: bool = False
    
    model_config = {"from_attributes": True}

class MoveRequest(BaseModel):
    """Запрос на перемещение."""
    target_location_id: uuid.UUID = Field(..., description="ID целевой локации")

class MoveResponse(BaseModel):
    """Результат перемещения."""
    success: bool
    message: str
    new_location: LocationResponse
    fatigue_added: int
    encounter: Optional[dict] = None
    
    model_config = {"from_attributes": True}

```



### 50. `backend/app/services/character_service.py`

**Размер:** 6.5 KB

**Язык:** `python`



```python
"""Бизнес-логика операций с персонажем."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.character import Character
from app.models.location import Location
from app.models.enums import CHARACTER_CLASS, CHARACTER_STATUS
from app.utils.constants import CLASS_STARTING_STATS, STARTING_LOCATION_NAME, XP_THRESHOLDS, LEVEL_UP_BONUSES, MAX_FATIGUE, FATIGUE_ACTION_BLOCK
from app.utils.calculations import calculate_modifier, clamp_value, check_level_up, calculate_effective_stat
from app.schemas.character import CharacterCreateRequest, CharacterStatsResponse, CharacterResourcesResponse

async def validate_character_name(session: AsyncSession, name: str, exclude_id: str = None) -> bool:
    """Проверяет уникальность имени персонажа."""
    stmt = select(Character).where(Character.name == name)
    if exclude_id:
        stmt = stmt.where(Character.id != exclude_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none() is None

async def get_starting_location(session: AsyncSession) -> Location:
    """Получает стартовую локацию по имени."""
    result = await session.execute(
        select(Location).where(Location.name == STARTING_LOCATION_NAME)
    )
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=500, detail="Starting location not found")
    return location

def calculate_character_stats(character: Character) -> CharacterStatsResponse:
    """Рассчитывает характеристики с модификаторами."""
    # Базовые значения
    strength = character.strength
    agility = character.agility
    intelligence = character.intelligence
    
    # Модификаторы
    strength_mod = calculate_modifier(strength)
    agility_mod = calculate_modifier(agility)
    intelligence_mod = calculate_modifier(intelligence)
    
    # Эффективные (пока без экипировки - будет добавлено позже)
    strength_eff = calculate_effective_stat(strength)
    agility_eff = calculate_effective_stat(agility)
    intelligence_eff = calculate_effective_stat(intelligence)
    
    return CharacterStatsResponse(
        strength=strength,
        agility=agility,
        intelligence=intelligence,
        strength_mod=strength_mod,
        agility_mod=agility_mod,
        intelligence_mod=intelligence_mod,
        strength_effective=strength_eff,
        agility_effective=agility_eff,
        intelligence_effective=intelligence_eff,
    )

def calculate_character_resources(character: Character, inventory_used: int = None) -> CharacterResourcesResponse:
    """Рассчитывает ресурсы персонажа."""
    return CharacterResourcesResponse(
        hp_current=character.hp_current,
        hp_max=character.hp_max,
        mana_current=character.mana_current,
        mana_max=character.mana_max,
        stamina_current=character.stamina_current,
        stamina_max=character.stamina_max,
        fatigue=character.fatigue,
        gold=character.gold,
        inventory_slots=character.inventory_slots,
        inventory_slots_used=inventory_used,
    )

def check_action_allowed(character: Character) -> tuple[bool, str]:
    """Проверяет, может ли персонаж выполнять активные действия."""
    if character.fatigue >= FATIGUE_ACTION_BLOCK:
        return False, f"Слишком высокая усталость ({character.fatigue}%). Отдохните."
    if character.hp_current <= 0:
        return False, "Персонаж без сознания."
    return True, "OK"

async def create_character(
    session: AsyncSession,
    user_id: str,
    request: CharacterCreateRequest
) -> Character:
    """Создаёт нового персонажа."""
    # Проверка уникальности имени
    if not await validate_character_name(session, request.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Персонаж с таким именем уже существует"
        )
    
    # Получение стартовой локации
    starting_location = await get_starting_location(session)
    
    # Получение стартовых характеристик класса
    class_stats = CLASS_STARTING_STATS.get(request.character_class)
    if not class_stats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный класс персонажа"
        )
    
    # Создание персонажа
    character = Character(
        user_id=user_id,
        name=request.name,
        character_class=request.character_class,
        current_location_id=starting_location.id,
        # Характеристики класса
        strength=class_stats["strength"],
        agility=class_stats["agility"],
        intelligence=class_stats["intelligence"],
        # Ресурсы
        hp_current=class_stats["hp_max"],
        hp_max=class_stats["hp_max"],
        mana_current=class_stats["mana_max"],
        mana_max=class_stats["mana_max"],
        stamina_current=class_stats["stamina_max"],
        stamina_max=class_stats["stamina_max"],
        # Остальное
        level=1,
        experience=0,
        status='alive',
        fatigue=0,
        gold=0,
        inventory_slots=10,
    )
    
    session.add(character)
    await session.flush()
    await session.refresh(character)
    
    return character

async def apply_level_up(character: Character) -> dict:
    """Применяет повышение уровня персонажа."""
    from app.utils.constants import LEVEL_UP_BONUSES
    
    stats_increased = {}
    
    # Увеличение характеристик
    for stat, bonus in LEVEL_UP_BONUSES.items():
        if hasattr(character, stat):
            old_value = getattr(character, stat)
            new_value = old_value + bonus
            setattr(character, stat, new_value)
            stats_increased[stat] = {"old": old_value, "new": new_value}
    
    # Полное восстановление ресурсов
    character.hp_current = character.hp_max
    character.mana_current = character.mana_max
    character.stamina_current = character.stamina_max
    character.fatigue = 0
    
    return stats_increased

```



### 51. `backend/app/services/combat_service.py`

**Размер:** 17.0 KB

**Язык:** `python`



```python
"""Бизнес-логика боевой системы."""
import asyncio
import random
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import get_gpt_client, get_prompt_cache
from app.ai.prompts import COMBAT_NARRATIVE_PROMPT
from app.models.character import Character
from app.models.combat import Enemy, CombatSession
from app.models.location import Location
from app.schemas.combat import (
    CombatActionResult, CombatStateResponse, CombatLogEntry
)
from app.services.character_service import apply_level_up
from app.utils.calculations import calculate_modifier, clamp_value, check_level_up
from app.utils.dice import roll_d20, roll_damage, check_success, calculate_dc

# Константы боя
BASE_AC = 10  # Базовый класс брони
BASE_DC = 10  # Базовая сложность проверки
CRIT_MULTIPLIER = 2  # Множитель урона при крите
FLEE_DC_BASE = 15  # Базовая сложность побега


async def get_active_combat(session: AsyncSession, character_id: str) -> Optional[CombatSession]:
    """Получает активную боевую сессию персонажа."""
    result = await session.execute(
        select(CombatSession).where(
            CombatSession.character_id == character_id,
            CombatSession.is_active == True
        )
    )
    return result.scalar_one_or_none()


async def start_combat(
    session: AsyncSession,
    character_id: str,
    enemy_id: Optional[str] = None
) -> CombatSession:
    """Инициализирует новый бой."""
    # Проверяем, нет ли уже активного боя
    existing = await get_active_combat(session, character_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Бой уже активен"
        )
    
    # Получаем персонажа
    char_result = await session.execute(
        select(Character).where(Character.id == character_id)
    )
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    # Получаем или выбираем врага
    if enemy_id:
        enemy_result = await session.execute(
            select(Enemy).where(Enemy.id == enemy_id)
        )
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(status_code=404, detail="Enemy not found")
    else:
        # Выбираем случайного врага подходящего уровня
        enemy_result = await session.execute(
            select(Enemy)
            .where(
                and_(
                    Enemy.level >= max(1, character.level - 2),
                    Enemy.level <= character.level + 2
                )
            )
            .order_by(func.random())
            .limit(1)
        )
        enemy = enemy_result.scalar_one_or_none()
        if not enemy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No suitable enemies found"
            )
    
    # Создаём боевую сессию
    combat = CombatSession(
        character_id=character.id,
        enemy_id=enemy.id,
        enemy_name=enemy.name,
        enemy_hp_current=enemy.hp,
        enemy_hp_max=enemy.hp,
        enemy_stats={
            "strength": enemy.strength,
            "agility": enemy.agility,
            "intelligence": enemy.intelligence,
            "damage_min": enemy.damage_min,
            "damage_max": enemy.damage_max,
            "armor": enemy.armor,
            "dodge_chance": enemy.dodge_chance,
            "crit_chance": enemy.crit_chance,
        },
        is_active=True,
        current_turn=1,
        combat_log=[f"Бой начался! На вас напал {enemy.name}!"],
    )
    
    session.add(combat)
    await session.flush()
    await session.refresh(combat)
    
    return combat


def calculate_player_attack_dc(character: Character) -> int:
    """Рассчитывает сложность атаки игрока."""
    enemy_agi_mod = calculate_modifier(character.agility)
    return BASE_DC + enemy_agi_mod


def calculate_enemy_attack_dc(enemy_stats: dict) -> int:
    """Рассчитывает сложность атаки врага."""
    return BASE_DC + calculate_modifier(enemy_stats.get("agility", 10))


def calculate_player_armor(character: Character) -> int:
    """Рассчитывает броню игрока (упрощённо, без экипировки)."""
    return 0


def calculate_damage(
    attacker_str: int,
    defender_armor: int,
    min_dmg: int,
    max_dmg: int,
    is_critical: bool = False
) -> int:
    """Рассчитывает итоговый урон."""
    str_mod = calculate_modifier(attacker_str)
    base_dmg = roll_damage(min_dmg, max_dmg, str_mod, is_critical)
    return max(0, base_dmg - defender_armor)


async def generate_combat_narrative(
    character: Character,
    enemy_name: str,
    action_type: str,
    result_desc: str,
    damage: int,
    enemy_hp: int,
    enemy_max: int
) -> str:
    """Генерирует атмосферное описание хода через ИИ."""
    try:
        client = get_gpt_client()
        cache = get_prompt_cache()
        
        prompt_text = COMBAT_NARRATIVE_PROMPT.format(
            char_name=character.name,
            char_class=character.character_class,
            char_level=character.level,
            enemy_name=enemy_name,
            action_type=action_type,
            result_desc=result_desc,
            damage=damage if damage else 0,
            enemy_hp=enemy_hp,
            enemy_max=enemy_max,
            char_hp=character.hp_current,
            char_max=character.hp_max
        )
        
        messages = [{"role": "user", "text": prompt_text}]
        prompt_hash = cache.hash_prompt(messages)
        
        # Проверяем кэш
        cached_response = await cache.get(prompt_hash)
        if cached_response:
            return cached_response.strip()
        
        # Запрос к ИИ с таймаутом (чтобы не ждать долго)
        response = await asyncio.wait_for(
            client.generate(messages, temperature=0.8, max_tokens=100),
            timeout=3.0
        )
        
        # Кэшируем результат
        await cache.set(prompt_hash, response.strip())
        return response.strip()
        
    except Exception:
        # В случае ошибки возвращаем стандартное описание (fallback)
        return f"{result_desc} (Урон: {damage if damage else 0})"


async def process_player_attack(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatActionResult:
    """Обрабатывает атаку игрока."""
    enemy_stats = combat.enemy_stats
    
    # Бросок атаки
    attack_mod = calculate_modifier(character.strength)
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_enemy_attack_dc(enemy_stats)
    
    # Проверка попадания
    if attack_roll == 1:
        # Критический промах
        log_entry = f"Вы промахнулись критически!"
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="player_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="player",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(
            success=True,
            message=log_entry,
            is_miss=True,
            is_critical=False
        )
    
    if is_crit:
        log_entry = f"Критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = f"Вы попали! "
    else:
        log_entry = f"Вы промахнулись. "
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="player_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="player",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    # Расчёт урона
    damage = calculate_damage(
        attacker_str=character.strength,
        defender_armor=enemy_stats.get("armor", 0),
        min_dmg=character.strength // 2,
        max_dmg=character.strength,
        is_critical=is_crit
    )
    
    # Применение урона
    combat.enemy_hp_current = max(0, combat.enemy_hp_current - damage)
    
    log_entry += f"Урон: {damage}. HP врага: {combat.enemy_hp_current}/{combat.enemy_hp_max}"
    
    # Генерация ИИ описания
    ai_description = await generate_combat_narrative(
        character=character,
        enemy_name=combat.enemy_name,
        action_type="player_attack",
        result_desc=log_entry,
        damage=damage,
        enemy_hp=combat.enemy_hp_current,
        enemy_max=combat.enemy_hp_max
    )
    
    # Добавляем запись в лог с ИИ описанием
    combat.combat_log.append(CombatLogEntry(
        turn=combat.current_turn,
        actor="player",
        action="attack",
        description=ai_description,
        damage=damage,
        is_critical=is_crit
    ).model_dump())
    
    # Проверка победы
    if combat.enemy_hp_current <= 0:
        return await finish_combat(session, combat, character, victory=True)
    
    await session.flush()
    return CombatActionResult(
        success=True,
        message=log_entry,
        enemy_damage_taken=damage,
        is_critical=is_crit
    )


async def process_enemy_turn(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatActionResult:
    """Обрабатывает ход врага."""
    enemy_stats = combat.enemy_stats
    
    # Простая логика: враг всегда атакует
    attack_mod = calculate_modifier(enemy_stats.get("strength", 10))
    attack_roll, is_crit = roll_d20(attack_mod)
    attack_dc = calculate_player_attack_dc(character)
    
    if attack_roll == 1:
        log_entry = f"{combat.enemy_name} промахнулся критически!"
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="enemy_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="enemy",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    if is_crit:
        log_entry = f"{combat.enemy_name} наносит критический удар! "
    elif check_success(attack_roll, attack_dc):
        log_entry = f"{combat.enemy_name} атакует! "
    else:
        log_entry = f"{combat.enemy_name} промахнулся. "
        ai_description = await generate_combat_narrative(
            character=character,
            enemy_name=combat.enemy_name,
            action_type="enemy_attack",
            result_desc=log_entry,
            damage=0,
            enemy_hp=combat.enemy_hp_current,
            enemy_max=combat.enemy_hp_max
        )
        combat.combat_log.append(CombatLogEntry(
            turn=combat.current_turn,
            actor="enemy",
            action="attack",
            description=ai_description,
            is_miss=True
        ).model_dump())
        await session.flush()
        return CombatActionResult(success=True, message=log_entry, is_miss=True)
    
    # Расчёт урона
    damage = calculate_damage(
        attacker_str=enemy_stats.get("strength", 10),
        defender_armor=calculate_player_armor(character),
        min_dmg=enemy_stats.get("damage_min", 1),
        max_dmg=enemy_stats.get("damage_max", 5),
        is_critical=is_crit
    )
    
    # Применение урона персонажу
    character.hp_current = max(0, character.hp_current - damage)
    
    log_entry += f"Урон: {damage}. Ваше HP: {character.hp_current}/{character.hp_max}"
    
    # Генерация ИИ описания атаки врага
    ai_description = await generate_combat_narrative(
        character=character,
        enemy_name=combat.enemy_name,
        action_type="enemy_attack",
        result_desc=log_entry,
        damage=damage,
        enemy_hp=combat.enemy_hp_current,
        enemy_max=combat.enemy_hp_max
    )
    
    combat.combat_log.append(CombatLogEntry(
        turn=combat.current_turn,
        actor="enemy",
        action="attack",
        description=ai_description,
        damage=damage,
        is_critical=is_crit
    ).model_dump())
    
    # Проверка поражения
    if character.hp_current <= 0:
        return await finish_combat(session, combat, character, victory=False)
    
    # Следующий ход
    combat.current_turn += 1
    await session.flush()
    
    return CombatActionResult(
        success=True,
        message=log_entry,
        player_damage_taken=damage,
        is_critical=is_crit
    )


async def finish_combat(
    session: AsyncSession,
    combat: CombatSession,
    character: Character,
    victory: bool
) -> CombatActionResult:
    """Завершает бой и начисляет награды."""
    combat.is_active = False
    
    if victory:
        # Награды за победу
        xp_gain = 10
        gold_gain = random.randint(5, 15)
        
        character.experience += xp_gain
        character.gold += gold_gain
        
        # Проверка повышения уровня
        leveled_up, new_level = check_level_up(character.experience, character.level)
        if leveled_up:
            character.level = new_level
            await apply_level_up(character)
        
        combat.result = "victory"
        combat.rewards = {"xp": xp_gain, "gold": gold_gain}
        
        message = f"🎉 Победа! +{xp_gain} XP, +{gold_gain} золота"
        if leveled_up:
            message += f" | Уровень повышен до {new_level}!"
        
    else:
        # Штрафы за поражение
        character.gold = max(0, character.gold - 10)
        character.fatigue = clamp_value(character.fatigue + 20, 0, 100)
        
        combat.result = "defeat"
        message = "💀 Поражение... Вы потеряли 10 золота и устали."
    
    combat.ended_at = datetime.now()
    
    # Восстановление выносливости после боя
    character.stamina_current = clamp_value(
        character.stamina_current + 10,
        0,
        character.stamina_max
    )
    
    await session.flush()
    
    return CombatActionResult(
        success=True,
        message=message,
        battle_ended=True,
        battle_result=combat.result,
        rewards=combat.rewards if victory else None
    )


async def get_combat_state(
    session: AsyncSession,
    combat: CombatSession,
    character: Character
) -> CombatStateResponse:
    """Возвращает текущее состояние боя."""
    return CombatStateResponse(
        combat_session_id=combat.id,
        enemy_name=combat.enemy_name,
        enemy_level=combat.enemy_stats.get("level", 1),
        enemy_hp_current=combat.enemy_hp_current,
        enemy_hp_max=combat.enemy_hp_max,
        player_hp_current=character.hp_current,
        player_hp_max=character.hp_max,
        player_mana_current=character.mana_current,
        player_mana_max=character.mana_max,
        current_turn=combat.current_turn,
        is_player_turn=True,
        combat_log=[
            CombatLogEntry(**(entry if isinstance(entry, dict) else {
                "turn": 1,
                "actor": "system",
                "action": "log",
                "description": str(entry),
                "is_critical": False,
                "is_miss": False
            }))
            for entry in combat.combat_log
        ]
    )
```



### 52. `backend/app/services/location_service.py`

**Размер:** 7.3 KB

**Язык:** `python`



```python
from typing import Optional
import random
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.location import Location, LocationConnection
from app.models.character import Character
from app.models.combat import Enemy, CombatSession
from app.utils.constants import FATIGUE_WARNING, FATIGUE_ACTION_BLOCK
from app.utils.calculations import clamp_value
from app.schemas.location import LocationResponse, NeighborLocationResponse, MoveResponse

# Вероятности случайных встреч по типам локаций
ENCOUNTER_PROBABILITIES = {
    "city": 0.0,
    "forest": 0.3,
    "road": 0.1,
    "dungeon": 0.7,
    "cave": 0.5,
    "mountain": 0.4,
    "swamp": 0.6,
}

BASE_FATIGUE_COST = 5

async def get_location_by_id(session: AsyncSession, location_id: str) -> Location:
    result = await session.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location

async def get_current_location(session: AsyncSession, character_id: str) -> Location:
    result = await session.execute(
        select(Location)
        .join(Character, Character.current_location_id == Location.id)
        .where(Character.id == character_id)
    )
    location = result.scalar_one_or_none()
    if not location:
        raise HTTPException(status_code=404, detail="Current location not found")
    return location

async def get_neighbors(session: AsyncSession, location_id: str) -> list[Location]:
    result = await session.execute(
        select(Location)
        .join(LocationConnection, Location.id == LocationConnection.to_location_id)
        .where(LocationConnection.from_location_id == location_id)
    )
    return result.scalars().all()

async def validate_move(
    session: AsyncSession,
    character_id: str,
    target_location_id: str
) -> tuple[Character, Location, LocationConnection]:
    char_result = await session.execute(select(Character).where(Character.id == character_id))
    character = char_result.scalar_one_or_none()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    
    target = await get_location_by_id(session, target_location_id)
    
    conn_result = await session.execute(
        select(LocationConnection).where(
            and_(
                LocationConnection.from_location_id == character.current_location_id,
                LocationConnection.to_location_id == target_location_id
            )
        )
    )
    connection = conn_result.scalar_one_or_none()
    if not connection:
        raise HTTPException(status_code=400, detail="Cannot move to this location directly")
    
    if character.fatigue >= FATIGUE_ACTION_BLOCK:
        raise HTTPException(status_code=400, detail=f"Too fatigued ({character.fatigue}%). Rest first.")
    
    return character, target, connection

def calculate_fatigue_cost(connection: LocationConnection, character: Character) -> int:
    base = BASE_FATIGUE_COST
    difficulty_bonus = connection.travel_difficulty * 2
    level_penalty = max(0, connection.travel_difficulty - character.level) * 3
    total = base + difficulty_bonus + level_penalty
    return clamp_value(total, 1, 50)

async def check_random_encounter(
    session: AsyncSession,
    location: Location,
    character: Character
) -> Optional[dict]:
    probability = ENCOUNTER_PROBABILITIES.get(location.location_type, 0.1)
    
    if random.random() > probability:
        return None
    
    enemy_result = await session.execute(
        select(Enemy)
        .where(
            and_(
                Enemy.level >= max(1, character.level - 2),
                Enemy.level <= character.level + 2
            )
        )
        .order_by(Enemy.level)
        .limit(1)
    )
    enemy = enemy_result.scalar_one_or_none()
    
    if not enemy:
        return None
    
    combat = CombatSession(
        character_id=character.id,
        enemy_id=enemy.id,
        enemy_name=enemy.name,
        enemy_hp_current=enemy.hp,
        enemy_hp_max=enemy.hp,
        enemy_stats={
            "strength": enemy.strength,
            "agility": enemy.agility,
            "intelligence": enemy.intelligence,
            "damage_min": enemy.damage_min,
            "damage_max": enemy.damage_max,
            "armor": enemy.armor,
        },
        is_active=True,
        current_turn=1,
        combat_log=[f"Внезапная встреча с {enemy.name}!"],
    )
    session.add(combat)
    await session.flush()
    
    return {
        "type": "combat",
        "enemy_name": enemy.name,
        "enemy_level": enemy.level,
        "combat_session_id": str(combat.id),
        "message": f"На вас напал {enemy.name}!"
    }

async def generate_location_description(
    location: Location,
    character_class: str,
    character_level: int
) -> str:
    templates = {
        "city": f"Город {location.name} встречает вас шумом и суетой. Здесь можно найти торговцев и таверну.",
        "forest": f"Лес {location.name} окутан таинственной тишиной. Тени шевелятся между древними деревьями.",
        "road": f"Пыльная дорога {location.name} ведёт через {location.region}. Вдали виднеются силуэты путников.",
        "dungeon": f"Мрачный вход в {location.name} зияет темнотой. Оттуда доносится эхо чьих-то шагов.",
        "cave": f"Пещера {location.name} хранит секреты древних времён. Сталактиты сверкают в тусклом свете.",
        "mountain": f"Горы {location.name} возвышаются над облаками. Ветер свистит в ущельях.",
        "swamp": f"Болото {location.name} окутано туманом. Где-то вдалеке квакают невидимые лягушки.",
    }
    return templates.get(location.location_type, f"Вы находитесь в {location.name}.")

async def move_character(
    session: AsyncSession,
    character_id: str,
    target_location_id: str
) -> MoveResponse:
    character, target, connection = await validate_move(session, character_id, target_location_id)
    
    fatigue_cost = calculate_fatigue_cost(connection, character)
    character.fatigue = clamp_value(character.fatigue + fatigue_cost, 0, 100)
    
    character.current_location_id = target_location_id
    
    encounter = await check_random_encounter(session, target, character)
    
    if not target.ai_description_generated:
        target.description = await generate_location_description(target, character.character_class, character.level)
        target.ai_description_generated = True
    
    await session.flush()
    
    message = f"Вы прибыли в {target.name}."
    if character.fatigue >= FATIGUE_WARNING:
        message += f" Вы очень устали ({character.fatigue}%)."
    
    return MoveResponse(
        success=True,
        message=message,
        new_location=LocationResponse.model_validate(target),
        fatigue_added=fatigue_cost,
        encounter=encounter
    )

```



### 53. `backend/app/utils/calculations.py`

**Размер:** 1.7 KB

**Язык:** `python`



```python
"""Формулы игровых расчётов."""

def calculate_modifier(stat_value: int) -> int:
    """
    Рассчитывает модификатор характеристики.
    Формула: (stat - 10) // 2
    """
    return (stat_value - 10) // 2

def clamp_value(value: int, min_val: int, max_val: int) -> int:
    """Ограничивает значение в заданных границах."""
    return max(min_val, min(value, max_val))

def get_xp_for_level(level: int) -> int:
    """Возвращает порог опыта для заданного уровня."""
    from app.utils.constants import XP_THRESHOLDS
    return XP_THRESHOLDS.get(level, 0)

def get_next_level_xp(level: int) -> int:
    """Возвращает опыт, необходимый для следующего уровня."""
    from app.utils.constants import XP_THRESHOLDS
    if level >= 15:
        return 0
    return XP_THRESHOLDS.get(level + 1, 0) - XP_THRESHOLDS.get(level, 0)

def check_level_up(current_xp: int, current_level: int) -> tuple[bool, int]:
    """
    Проверяет, достиг ли персонаж следующего уровня.
    Возвращает: (уровень_повышен, новый_уровень)
    """
    from app.utils.constants import XP_THRESHOLDS
    for level in range(current_level + 1, 16):
        if current_xp >= XP_THRESHOLDS.get(level, float('inf')):
            return True, level
    return False, current_level

def calculate_effective_stat(base_stat: int, equipment_bonus: int = 0, buff_bonus: int = 0) -> int:
    """Рассчитывает эффективное значение характеристики."""
    return base_stat + equipment_bonus + buff_bonus

```



### 54. `backend/app/utils/constants.py`

**Размер:** 2.2 KB

**Язык:** `python`



```python
"""Константы игровых механик."""

# Стартовые характеристики для 11 классов
CLASS_STARTING_STATS = {
    "warrior": {"strength": 14, "agility": 10, "intelligence": 8, "hp_max": 120, "mana_max": 40, "stamina_max": 100},
    "priest": {"strength": 8, "agility": 10, "intelligence": 14, "hp_max": 80, "mana_max": 120, "stamina_max": 90},
    "paladin": {"strength": 12, "agility": 10, "intelligence": 10, "hp_max": 100, "mana_max": 80, "stamina_max": 95},
    "mage": {"strength": 6, "agility": 10, "intelligence": 16, "hp_max": 60, "mana_max": 150, "stamina_max": 70},
    "summoner": {"strength": 8, "agility": 12, "intelligence": 14, "hp_max": 70, "mana_max": 130, "stamina_max": 80},
    "necromancer": {"strength": 8, "agility": 10, "intelligence": 15, "hp_max": 75, "mana_max": 140, "stamina_max": 75},
    "barbarian": {"strength": 16, "agility": 12, "intelligence": 6, "hp_max": 140, "mana_max": 30, "stamina_max": 110},
    "hunter": {"strength": 10, "agility": 14, "intelligence": 10, "hp_max": 90, "mana_max": 60, "stamina_max": 100},
    "druid": {"strength": 10, "agility": 10, "intelligence": 12, "hp_max": 85, "mana_max": 100, "stamina_max": 95},
    "rogue": {"strength": 10, "agility": 16, "intelligence": 8, "hp_max": 80, "mana_max": 50, "stamina_max": 105},
    "werewolf": {"strength": 13, "agility": 13, "intelligence": 7, "hp_max": 110, "mana_max": 45, "stamina_max": 100},
}

# Стартовая локация для всех классов
STARTING_LOCATION_NAME = "Деревня Элдарион"

# Пороги опыта для уровней 1-15
XP_THRESHOLDS = {
    1: 0,
    2: 100,
    3: 250,
    4: 450,
    5: 700,
    6: 1000,
    7: 1400,
    8: 1900,
    9: 2500,
    10: 3200,
    11: 4000,
    12: 5000,
    13: 6200,
    14: 7600,
    15: 9200,
}

# Бонусы характеристик при повышении уровня
LEVEL_UP_BONUSES = {
    "strength": 2,
    "agility": 2,
    "intelligence": 2,
    "hp_max": 10,
    "mana_max": 8,
    "stamina_max": 5,
}

# Лимиты ресурсов
MAX_FATIGUE = 100
FATIGUE_ACTION_BLOCK = 80
FATIGUE_WARNING = 60

# Восстановление при отдыхе
REST_CAMP_RECOVERY = 0.3  # 30%
REST_TAVERN_RECOVERY = 1.0  # 100%

```



### 55. `backend/app/utils/dice.py`

**Размер:** 1.4 KB

**Язык:** `python`



```python
"""Утилиты для бросков кубиков и расчётов d20."""
import random
from typing import Optional

def roll_d20(modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> tuple[int, bool]:
    """
    Бросает 1d20 с модификатором.
    
    Возвращает: (результат_броска, был_ли_крит)
    """
    if advantage and disadvantage:
        # Взаимная отмена
        roll = random.randint(1, 20)
    elif advantage:
        roll = max(random.randint(1, 20), random.randint(1, 20))
    elif disadvantage:
        roll = min(random.randint(1, 20), random.randint(1, 20))
    else:
        roll = random.randint(1, 20)
    
    is_critical = roll in (1, 20)
    return roll + modifier, is_critical

def roll_damage(min_dmg: int, max_dmg: int, modifier: int = 0, is_critical: bool = False) -> int:
    """
    Рассчитывает урон.
    
    При критическом успехе урон удваивается.
    """
    base = random.randint(min_dmg, max_dmg) + modifier
    if is_critical and base > 0:
        base *= 2
    return max(0, base)

def calculate_dc(base: int, modifier: int = 0) -> int:
    """Рассчитывает сложность проверки (DC)."""
    return base + modifier

def check_success(roll: int, dc: int) -> bool:
    """Проверяет успех проверки."""
    return roll >= dc

```



### 56. `backend/seeds/load_seeds.py`

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



### 57. `frontend/public/index.html`

**Размер:** 1.6 KB

**Язык:** `html`



```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Легенды Элары</title>
    <script src="https://unpkg.com/@vkontakte/vk-bridge/dist/browser.min.js"></script>
</head>
<body>
    <div id="root">
        <h1>🐉 Легенды Элары</h1>
        <p>Приложение загружается...</p>
        <div id="user-info"></div>
    </div>
    
    <script>
        // Инициализация VK Bridge
        vkBridge.send('VKWebAppInit')
            .then(() => {
                console.log('VK Bridge инициализирован');
                document.getElementById('user-info').innerHTML = '<p>✅ VK Bridge работает!</p>';
                
                // Получаем данные пользователя
                return vkBridge.send('VKWebAppGetUserInfo');
            })
            .then(data => {
                console.log('User info:', data);
                if (data.id) {
                    document.getElementById('user-info').innerHTML += 
                        `<p>Привет, ${data.first_name}!</p>
                         <p>User ID: ${data.id}</p>`;
                }
            })
            .catch(error => {
                console.error('Ошибка VK Bridge:', error);
                document.getElementById('user-info').innerHTML += 
                    '<p style="color: red">⚠️ Ошибка инициализации VK Bridge</p>';
            });
    </script>
</body>
</html>

```



### 58. `nginx/conf.d/api.conf`

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



### 59. `nginx/conf.d/app.conf`

**Размер:** 0.0 KB

**Язык:** `ini`



```ini

```



### 60. `nginx/nginx.conf`

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



### 61. `scan_project.py`

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

*Всего файлов кода: 61*
