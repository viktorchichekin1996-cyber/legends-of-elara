from sqlalchemy.dialects.postgresql import ENUM

def pg_enum(name: str, *values: str) -> ENUM:
    return ENUM(*values, name=name, create_type=True)

CHARACTER_CLASS = pg_enum('character_class',
    'воин', 'жрец', 'паладин', 'маг', 'призыватель',
    'некромант', 'варвар', 'охотник', 'друид', 'вор', 'оборотень'
)

ITEM_TYPE = pg_enum('item_type',
    'оружие', 'броня', 'аксессуар', 'расходник', 'квестовый', 'сумка'
)

ITEM_RARITY = pg_enum('item_rarity',
    'обычный', 'необычный', 'редкий', 'эпический', 'легендарный'
)

EQUIPMENT_SLOT = pg_enum('equipment_slot',
    'оружие', 'броня', 'шлем', 'перчатки', 'ботинки',
    'аксессуар', 'кольцо1', 'кольцо2'
)

LOCATION_TYPE = pg_enum('location_type',
    'город', 'лес', 'дорога', 'подземелье', 'пещера', 'горы', 'болото'
)

QUEST_STATUS = pg_enum('quest_status',
    'активен', 'завершён', 'провален', 'отменён'
)

TRANSACTION_TYPE = pg_enum('transaction_type',
    'награда_квест', 'награда_бой', 'покупка', 'продажа',
    'отдых', 'ремонт', 'обучение', 'штраф'
)

MEMORY_TYPE = pg_enum('memory_type',
    'победа_над_боссом', 'смерть_союзника', 'важный_выбор', 'открытие',
    'квест_завершён', 'повышение_уровня', 'уникальное_событие'
)

CHARACTER_STATUS = pg_enum('character_status',
    'жив', 'мёртв', 'отдых'
)