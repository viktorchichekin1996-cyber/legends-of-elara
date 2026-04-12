"""Эндпоинты квестов."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.quest import CharacterQuest, Quest
from app.schemas.quest import QuestResponse, CharacterQuestResponse, QuestGenerateRequest
from app.services.quest_service import generate_quest, complete_quest, cancel_quest

router = APIRouter(prefix="/quests", tags=["Quests"])

@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_new_quest(
    request: QuestGenerateRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    
    cq, quest = await generate_quest(db, str(char.id), request.quest_type)
    await db.commit()
    
    return {"character_quest_id": str(cq.id), "quest": QuestResponse.model_validate(quest)}

@router.get("/", response_model=list[CharacterQuestResponse])
async def get_quests(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    # FIX: Используем правильный join с relationship
    result = await db.execute(
        select(CharacterQuest, Quest)
        .join(Quest, CharacterQuest.quest_id == Quest.id)
        .where(CharacterQuest.character_id == char.id)
        .order_by(CharacterQuest.accepted_at.desc())
    )
    rows = result.all()
    
    return [
        CharacterQuestResponse(
            id=cq.id, 
            quest_id=cq.quest_id, 
            quest_name=q.name if q else "Unknown",
            status=cq.status, 
            progress=cq.progress, 
            accepted_at=cq.accepted_at
        ) for cq, q in rows
    ]

@router.post("/{quest_id}/complete")
async def complete_active_quest(
    quest_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    res = await complete_quest(db, str(char.id), quest_id)
    await db.commit()
    return res

@router.post("/{quest_id}/cancel")
async def cancel_active_quest(
    quest_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    char = (await db.execute(select(Character).where(Character.user_id == current_user.id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
        
    res = await cancel_quest(db, str(char.id), quest_id)
    await db.commit()
    return res
