#!/usr/bin/env bash
set -euo pipefail

echo "🏗️ Подэтап 2.3-2.6: Создание моделей SQLAlchemy"
echo "=================================================="

cd ~/legends-of-elara/backend
mkdir -p app/models

# 1. Enums
echo "📝 Создание models/enums.py..."
cat > app/models/enums.py <<'PYEOF'
from sqlalchemy import Enum as SAEnum
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
PYEOF

# 2. User & Character
echo "📝 Создание models/user.py..."
cat > app/models/user.py <<'PYEOF'
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
    vk_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    characters: Mapped[List["Character"]] = relationship("Character", back_populates="user", cascade="all, delete-orphan")
PYEOF

echo "📝 Создание models/character.py..."
cat > app/models/character.py <<'PYEOF'
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin
from app.models.enums import CHARACTER_CLASS, CHARACTER_STATUS

class Character(Base, TimestampMixin):
    __tablename__ = "characters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    character_class: Mapped[str] = mapped_column(CHARACTER_CLASS, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(CHARACTER_STATUS, default="alive", nullable=False)
    
    strength: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    hp_current: Mapped[int] = mapped_column(Integer, nullable=False)
    hp_max: Mapped[int] = mapped_column(Integer, nullable=False)
    mana_current: Mapped[int] = mapped_column(Integer, nullable=False)
    mana_max: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_current: Mapped[int] = mapped_column(Integer, nullable=False)
    stamina_max: Mapped[int] = mapped_column(Integer, nullable=False)
    fatigue: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    gold: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    inventory_slots: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    
    current_location_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("locations.id"), index=True, nullable=False)
    
    user: Mapped["User"] = relationship("User", back_populates="characters")
    inventory: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="character", cascade="all, delete-orphan")
    
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
PYEOF

# 3. Items, Inventory, Equipment
echo "📝 Создание models/item.py..."
cat > app/models/item.py <<'PYEOF'
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
PYEOF

echo "📝 Создание models/inventory.py..."
cat > app/models/inventory.py <<'PYEOF'
import uuid
from datetime import datetime
from typing import List
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
PYEOF

# 4. Locations & Connections
echo "📝 Создание models/location.py..."
cat > app/models/location.py <<'PYEOF'
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
PYEOF

# 5. Quests & Memory
echo "📝 Создание models/quest.py..."
cat > app/models/quest.py <<'PYEOF'
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
        CheckConstraint("(SELECT COUNT(*) FROM character_quests WHERE character_id = character_quests.character_id AND status = 'active') <= 3", name="character_active_quests_limit"),
        Index("idx_character_quests_status", "status"),
    )
PYEOF

echo "📝 Создание models/memory.py..."
cat > app/models/memory.py <<'PYEOF'
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
PYEOF

# 6. Combat & Economy & System
echo "📝 Создание models/combat.py..."
cat > app/models/combat.py <<'PYEOF'
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
PYEOF

echo "📝 Создание models/shop.py..."
cat > app/models/shop.py <<'PYEOF'
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
PYEOF

echo "📝 Создание models/system.py..."
cat > app/models/system.py <<'PYEOF'
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
PYEOF

# 7. Init для Alembic discovery
echo "📦 Создание models/__init__.py..."
cat > app/models/__init__.py <<'PYEOF'
from app.db.base import Base
from app.models import user, character, item, inventory, location, quest, memory, combat, shop, system

__all__ = [
    "Base", "User", "Character", "Item", "Inventory", "Equipment",
    "Location", "LocationConnection", "Quest", "CharacterQuest",
    "CharacterMemory", "Enemy", "CombatSession", "ShopItem", "Transaction",
    "AiPrompt", "GameLog"
]
PYEOF
# Fix: import models correctly in __init__
cat > app/models/__init__.py <<'PYEOF'
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
PYEOF

echo "=================================================="
echo "✅ Подэтап 2.3-2.6 успешно выполнен!"