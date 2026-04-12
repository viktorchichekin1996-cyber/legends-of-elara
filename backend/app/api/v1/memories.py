"""Эндпоинты памяти персонажа."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.schemas.memory import MemoryResponse
from app.services.memory_service import get_character_memories

router = APIRouter(prefix="/memories", tags=["Memories"])

@router.get("/", response_model=list[MemoryResponse])
async def get_memories(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    memories = await get_character_memories(db, str(char.id))
    return [MemoryResponse.model_validate(m) for m in memories]