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

class QuestStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MemoryType(str, enum.Enum):
    BOSS_DEFEAT = "boss_defeat"
    ALLY_DEATH = "ally_death"
    IMPORTANT_CHOICE = "important_choice"
    DISCOVERY = "discovery"
    QUEST_COMPLETE = "quest_complete"
    LEVEL_UP = "level_up"
    UNIQUE_EVENT = "unique_event"