"""Бизнес-логика памяти персонажа."""
import uuid
import logging
from typing import Dict, Any, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.memory import CharacterMemory
from app.utils.calculations import clamp_value

logger = logging.getLogger(__name__)

async def add_memory(
    session: AsyncSession,
    character_id: str | UUID,
    memory_type: str,
    title: str,
    description: str,
    importance: int,
    tags: List[str],
    data: Optional[Dict[str, Any]] = None
) -> CharacterMemory:
    """Сохраняет воспоминание. Автоматически игнорирует важность < 4."""
    if importance < 4:
        logger.debug(f"Memory ignored (importance={importance} < 4)")
        return None

    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    memory = CharacterMemory(
        id=uuid.uuid4(),
        character_id=char_uuid,
        memory_type=memory_type,
        title=title,
        description=description,
        importance=clamp_value(importance, 1, 5),
        tags=tags or [],
        data=data or {}
    )
    session.add(memory)
    await session.flush()
    await session.refresh(memory)
    logger.info(f"Memory added: {title} (imp={importance})")
    return memory

async def get_character_memories(
    session: AsyncSession, 
    character_id: str | UUID, 
    limit: int = 20
) -> List[CharacterMemory]:
    """Получает последние важные воспоминания персонажа."""
    char_uuid = UUID(character_id) if isinstance(character_id, str) else character_id
    stmt = (
        select(CharacterMemory)
        .where(CharacterMemory.character_id == char_uuid)
        .order_by(CharacterMemory.created_at.desc())
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())