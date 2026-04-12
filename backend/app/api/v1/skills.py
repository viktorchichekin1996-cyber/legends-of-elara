"""Эндпоинты обучения навыкам."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.schemas.shop import EconomyOperationResponse
from app.services.economy_service import record_transaction, get_character_gold

router = APIRouter(prefix="/skills", tags=["Skills & Training"])

@router.post("/train", response_model=EconomyOperationResponse)
async def train_skill(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Обучение навыку (симуляция за золото)."""
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    cost = 100 * char.level  # Формула стоимости
    gold_before = await get_character_gold(db, char.id)
    
    if gold_before < cost:
        raise HTTPException(status_code=400, detail=f"Недостаточно золота (нужно {cost})")
        
    # Просто списываем золото и даем немного опыта для примера
    await record_transaction(db, char.id, 'training', -cost, f"Обучение навыку (ур. {char.level})")
    char.experience += 50  # Бонус опыта за тренировку
    
    await db.commit()
    
    return EconomyOperationResponse(
        success=True, 
        message=f"Вы потренировались и получили +50 опыта. Потрачено {cost} золота.",
        gold_before=gold_before,
        gold_after=await get_character_gold(db, char.id)
    )
