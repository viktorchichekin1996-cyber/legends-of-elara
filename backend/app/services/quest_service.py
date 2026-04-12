"""Бизнес-логика квестов и прогресса."""
import uuid
import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from uuid import UUID

from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from fastapi import HTTPException, status

from app.models.quest import Quest, CharacterQuest
from app.models.character import Character
from app.models.location import Location
from app.models.enums import QUEST_STATUS
from app.schemas.quest import QuestAIResponse, QuestGenerateRequest
from app.ai import get_gpt_client, get_prompt_cache
from app.ai.prompts import QUEST_GENERATION_PROMPT
from app.services.memory_service import add_memory
from app.utils.calculations import clamp_value

logger = logging.getLogger(__name__)
MAX_ACTIVE_QUESTS = 3

def extract_json_from_response(raw_text: str) -> str:
    """Извлекает чистый JSON из ответа ИИ, удаляя markdown-обёртки."""
    if not raw_text:
        return ""
    
    # Удаляем маркдаун код-блоки: ```json ... ``` или ``` ... ```
    cleaned = re.sub(r'^```(?:json)?\s*', '', raw_text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r'\s*```$', '', cleaned, flags=re.MULTILINE)
    
    # Находим первый валидный JSON объект (на случай лишнего текста)
    # Ищем по первой { и последней }
    start = cleaned.find('{')
    end = cleaned.rfind('}') + 1
    if start >= 0 and end > start:
        return cleaned[start:end].strip()
    
    return cleaned.strip()

async def generate_quest(
    session: AsyncSession, 
    character_id: str | UUID,
    quest_type: Optional[str] = None
) -> Tuple[CharacterQuest, Quest]:
    """9.1 Генерация квеста через ИИ с валидацией."""
    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    
    # Проверка лимита активных квестов
    active_count_stmt = select(CharacterQuest).where(
        and_(CharacterQuest.character_id == char_uuid, CharacterQuest.status == "active")
    )
    active_count = len((await session.execute(active_count_stmt)).scalars().all())
    if active_count >= MAX_ACTIVE_QUESTS:
        raise HTTPException(status_code=400, detail=f"Максимум {MAX_ACTIVE_QUESTS} активных квестов")
    
    # Загружаем контекст персонажа
    char = (await session.execute(select(Character).where(Character.id == char_uuid))).scalar_one()
    loc = (await session.execute(select(Location).where(Location.id == char.current_location_id))).scalar_one()
    
    # Получаем список активных квестов для исключения дублей
    active_quests_stmt = select(Quest.name).join(CharacterQuest).where(
        and_(CharacterQuest.character_id == char_uuid, CharacterQuest.status == "active")
    )
    active_quests = [q[0] for q in (await session.execute(active_quests_stmt)).all()]
    
    # Формируем промпт
    prompt = QUEST_GENERATION_PROMPT.format(
        char_class=char.character_class,
        char_level=char.level,
        location_name=loc.name,
        location_type=loc.location_type,
        danger_level=loc.danger_level,
        quests=", ".join(active_quests) or "Нет активных"
    )
    
    # Запрос к ИИ
    client = get_gpt_client()
    cache = get_prompt_cache()
    messages = [{"role": "user", "text": prompt}]
    prompt_hash = cache.hash_prompt(messages)
    
    raw_response = await cache.get(prompt_hash)
    if not raw_response:
        raw_response = await client.generate(messages, temperature=0.8, max_tokens=1000)
        await cache.set(prompt_hash, raw_response)
    
    logger.debug(f"Raw AI response: {raw_response[:200]}...")
    
    # Извлекаем чистый JSON из ответа
    json_str = extract_json_from_response(raw_response)
    logger.debug(f"Extracted JSON: {json_str[:200]}...")
    
    # Парсинг и валидация
    try:
        quest_data = QuestAIResponse.model_validate_json(json_str)
    except Exception as e:
        logger.error(f"AI quest parse failed: {e}")
        logger.error(f"Raw response: {raw_response}")
        logger.error(f"Extracted JSON: {json_str}")
        raise HTTPException(status_code=502, detail="Ошибка генерации квеста ИИ")
    
    # Сохранение шаблона квеста в БД
    quest_db = Quest(
        id=uuid.uuid4(),
        name=quest_data.name,
        description=quest_data.description,
        goals=[g.model_dump() for g in quest_data.goals],
        rewards=quest_data.rewards.model_dump(),
        min_level=quest_data.min_level,
        ai_generated=True
    )
    session.add(quest_db)
    await session.flush()
    
    # Создание записи квеста у персонажа
    progress = [
        {"type": g.type, "target": g.target, "count": g.count, "current": 0} 
        for g in quest_data.goals
    ]
    
    char_quest = CharacterQuest(
        id=uuid.uuid4(),
        character_id=char_uuid,
        quest_id=quest_db.id,
        status="active",
        progress=progress
    )
    session.add(char_quest)
    await session.flush()
    
    logger.info(f"Quest generated: {quest_data.name} for char {char.name}")
    return char_quest, quest_db

async def update_quest_progress(
    session: AsyncSession,
    character_id: str | UUID,
    event_type: str,  # "kill", "collect", "visit"
    target: str,      # enemy_name, item_name, location_name
    amount: int = 1
) -> bool:
    """9.2 Авто-обновление прогресса квестов."""
    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    target_lower = target.lower().strip()
    
    active_stmt = select(CharacterQuest).where(
        and_(CharacterQuest.character_id == char_uuid, CharacterQuest.status == "active")
    )
    result = await session.execute(active_stmt)
    active_quests = result.scalars().all()
    
    updated = False
    for cq in active_quests:
        progress = cq.progress or []
        for goal in progress:
            if goal.get("type") == event_type and goal.get("target", "").lower().strip() == target_lower:
                if goal["current"] < goal["count"]:
                    goal["current"] = min(goal["current"] + amount, goal["count"])
                    updated = True
                    logger.debug(f"Quest progress: {goal['target']} {goal['current']}/{goal['count']}")
        
        if updated:
            cq.progress = progress
            await session.flush()
            break
            
    return updated

async def complete_quest(
    session: AsyncSession,
    character_id: str | UUID,
    character_quest_id: str | UUID
) -> dict:
    """9.3 Завершение квеста с проверкой прогресса и начислением наград."""
    cq_uuid = UUID(character_quest_id) if isinstance(character_quest_id, str) else character_quest_id
    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    
    cq = (await session.execute(
        select(CharacterQuest).options(selectinload(CharacterQuest.quest))
        .where(CharacterQuest.id == cq_uuid, CharacterQuest.character_id == char_uuid)
    )).scalar_one_or_none()
    
    if not cq:
        raise HTTPException(status_code=404, detail="Квест не найден")
    if cq.status != "active":
        raise HTTPException(status_code=400, detail="Квест не активен")
    
    # Проверка выполнения всех целей
    all_done = all(g["current"] >= g["count"] for g in (cq.progress or []))
    if not all_done:
        incomplete = [g["target"] for g in (cq.progress or []) if g["current"] < g["count"]]
        raise HTTPException(status_code=400, detail=f"Цели не выполнены: {', '.join(incomplete)}")
    
    # Начисление наград
    char = (await session.execute(select(Character).where(Character.id == char_uuid))).scalar_one()
    rewards = cq.quest.rewards or {"xp": 0, "gold": 0}
    
    char.experience += rewards.get("xp", 0)
    char.gold += rewards.get("gold", 0)
    
    cq.status = "completed"
    cq.completed_at = None  # SQLAlchemy server default
    
    # Сохранение в память (важность 4)
    await add_memory(
        session, char_uuid, "quest_complete", cq.quest.name,
        f"Выполнен квест: {cq.quest.name}. Награда: {rewards.get('xp', 0)} XP, {rewards.get('gold', 0)} золота.",
        4, ["quest", "completed"], {"quest_id": str(cq.id)}
    )
    
    await session.flush()
    return {"message": f"Квест '{cq.quest.name}' выполнен!", "rewards": rewards}

async def cancel_quest(
    session: AsyncSession,
    character_id: str | UUID,
    character_quest_id: str | UUID
) -> dict:
    """9.3 Отмена квеста."""
    cq_uuid = UUID(character_quest_id) if isinstance(character_quest_id, str) else character_quest_id
    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    
    cq = (await session.execute(
        select(CharacterQuest).where(CharacterQuest.id == cq_uuid, CharacterQuest.character_id == char_uuid)
    )).scalar_one_or_none()
    
    if not cq or cq.status != "active":
        raise HTTPException(status_code=404, detail="Активный квест не найден")
    
    cq.status = "cancelled"
    await session.flush()
    return {"message": "Квест отменён"}
