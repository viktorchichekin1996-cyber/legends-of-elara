"""Нативные Python Enum для Pydantic схем."""
import enum

class CharacterClass(str, enum.Enum):
    WARRIOR = "воин"
    PRIEST = "жрец"
    PALADIN = "паладин"
    MAGE = "маг"
    SUMMONER = "призыватель"
    NECROMANCER = "некромант"
    BARBARIAN = "варвар"
    HUNTER = "охотник"
    DRUID = "друид"
    ROGUE = "вор"
    WEREWOLF = "оборотень"

class CharacterStatus(str, enum.Enum):
    ALIVE = "жив"
    DEAD = "мёртв"
    RESTING = "отдых"

class LocationType(str, enum.Enum):
    CITY = "город"
    FOREST = "лес"
    ROAD = "дорога"
    DUNGEON = "подземелье"
    CAVE = "пещера"
    MOUNTAIN = "горы"
    SWAMP = "болото"

class ItemType(str, enum.Enum):
    WEAPON = "оружие"
    ARMOR = "броня"
    ACCESSORY = "аксессуар"
    CONSUMABLE = "расходник"
    QUEST_ITEM = "квестовый"
    BAG = "сумка"

class ItemRarity(str, enum.Enum):
    COMMON = "обычный"
    UNCOMMON = "необычный"
    RARE = "редкий"
    EPIC = "эпический"
    LEGENDARY = "легендарный"

class EquipmentSlot(str, enum.Enum):
    WEAPON = "оружие"
    ARMOR = "броня"
    HELMET = "шлем"
    GLOVES = "перчатки"
    BOOTS = "ботинки"
    ACCESSORY = "аксессуар"
    RING1 = "кольцо1"
    RING2 = "кольцо2"

class QuestStatus(str, enum.Enum):
    ACTIVE = "активен"
    COMPLETED = "завершён"
    FAILED = "провален"
    CANCELLED = "отменён"

class MemoryType(str, enum.Enum):
    BOSS_DEFEAT = "победа_над_боссом"
    ALLY_DEATH = "смерть_союзника"
    IMPORTANT_CHOICE = "важный_выбор"
    DISCOVERY = "открытие"
    QUEST_COMPLETE = "квест_завершён"
    LEVEL_UP = "повышение_уровня"
    UNIQUE_EVENT = "уникальное_событие"