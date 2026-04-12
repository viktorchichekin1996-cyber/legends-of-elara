"""Шаблоны промптов для YandexGPT."""
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.character import Character
from app.models.location import Location
from app.models.quest import CharacterQuest, Quest
from app.models.memory import CharacterMemory

logger = logging.getLogger(__name__)

# Экранируем фигурные скобки в примере схемы: {{ вместо {
SYSTEM_PROMPT = """
Ты — нейросетевой движок событий для текстовой RPG "Легенды Элары".
Правила вывода:
1. Ответ СТРОГО в формате JSON. Никакого markdown, никаких пояснений вне JSON.
2. Схема: {{ "description": "атмосферное описание события", "choices": [{{"text": "вариант", "action": "тип_действия"}}]}}
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

# === НОВЫЙ ПРОМПТ ДЛЯ ГЕНЕРАЦИИ КВЕСТОВ ===
# Все фигурные скобки в примере схемы экранированы: {{ вместо {
QUEST_GENERATION_PROMPT = """
Ты — геймдизайнер тёмного фэнтези RPG "Легенды Элары".
Создай уникальный квест на основе контекста персонажа.

Контекст:
- Класс: {char_class}, Уровень: {char_level}
- Локация: {location_name} (Тип: {location_type}, Опасность: {danger_level})
- Активные квесты: {quests}

Требования:
1. Ответ СТРОГО в формате чистого JSON без markdown, без пояснений.
2. Схема ответа (экранирована для Python .format()):
{{
  "name": "Название квеста",
  "description": "Описание задания в 2-3 предложениях",
  "goals": [
    {{"type": "kill|collect|visit", "target": "имя_цели", "count": число}}
  ],
  "rewards": {{"xp": число, "gold": число}},
  "min_level": число
}}
3. Цели должны соответствовать типу локации (в лесу = волки/грибы, в городе = NPC/торговля).
4. Награды сбалансированы по уровню персонажа (ур. {char_level}).
5. Не дублируй активные квесты: {quests}.
6. Язык ответа: русский.

Сгенерируй квест и верни ТОЛЬКО валидный JSON.
"""

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
