"""Константы игровых механик."""

# Стартовые характеристики для 11 классов
# Ключи должны совпадать с русскими значениями Enum CharacterClass
CLASS_STARTING_STATS = {
    "воин": {
        "strength": 14,
        "agility": 10,
        "intelligence": 8,
        "hp_max": 120,
        "mana_max": 40,
        "stamina_max": 100,
    },
    "жрец": {
        "strength": 8,
        "agility": 10,
        "intelligence": 14,
        "hp_max": 80,
        "mana_max": 120,
        "stamina_max": 90,
    },
    "паладин": {
        "strength": 12,
        "agility": 10,
        "intelligence": 10,
        "hp_max": 100,
        "mana_max": 80,
        "stamina_max": 95,
    },
    "маг": {
        "strength": 6,
        "agility": 10,
        "intelligence": 16,
        "hp_max": 60,
        "mana_max": 150,
        "stamina_max": 70,
    },
    "призыватель": {
        "strength": 8,
        "agility": 12,
        "intelligence": 14,
        "hp_max": 70,
        "mana_max": 130,
        "stamina_max": 80,
    },
    "некромант": {
        "strength": 8,
        "agility": 10,
        "intelligence": 15,
        "hp_max": 75,
        "mana_max": 140,
        "stamina_max": 75,
    },
    "варвар": {
        "strength": 16,
        "agility": 12,
        "intelligence": 6,
        "hp_max": 140,
        "mana_max": 30,
        "stamina_max": 110,
    },
    "охотник": {
        "strength": 10,
        "agility": 14,
        "intelligence": 10,
        "hp_max": 90,
        "mana_max": 60,
        "stamina_max": 100,
    },
    "друид": {
        "strength": 10,
        "agility": 10,
        "intelligence": 12,
        "hp_max": 85,
        "mana_max": 100,
        "stamina_max": 95,
    },
    "вор": {
        "strength": 10,
        "agility": 16,
        "intelligence": 8,
        "hp_max": 80,
        "mana_max": 50,
        "stamina_max": 105,
    },
    "оборотень": {
        "strength": 13,
        "agility": 13,
        "intelligence": 7,
        "hp_max": 110,
        "mana_max": 45,
        "stamina_max": 100,
    },
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
# Ключи должны совпадать с именами атрибутов модели Character
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