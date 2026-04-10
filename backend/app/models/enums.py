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
