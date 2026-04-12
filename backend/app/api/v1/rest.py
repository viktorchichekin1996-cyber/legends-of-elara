"""Эндпоинты отдыха и таверны."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.schemas.shop import TavernRequest, EconomyOperationResponse
from app.services.shop_service import rest_in_tavern

router = APIRouter(prefix="/rest", tags=["Rest & Tavern"])

@router.post("/tavern", response_model=EconomyOperationResponse)
async def rest_in_tavern_endpoint(
    request: TavernRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    result = await rest_in_tavern(db, char.id)
    await db.commit()
    return result
