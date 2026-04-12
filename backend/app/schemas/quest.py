"""Схемы для квестов."""
from typing import List, Optional, Dict, Any
import uuid
from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.enums import QuestStatus

class QuestGoalAI(BaseModel):
    """Структура цели квеста для AI генерации."""
    type: str = Field(..., description="kill, collect, visit")
    target: str = Field(..., description="Имя врага, предмета или локации")
    count: int = Field(..., ge=1, le=50)

class QuestRewardAI(BaseModel):
    xp: int = Field(..., ge=10, le=5000)
    gold: int = Field(..., ge=5, le=2000)

class QuestAIResponse(BaseModel):
    """Строгий ответ от ИИ для валидации."""
    name: str = Field(..., min_length=5, max_length=150)
    description: str = Field(..., min_length=10, max_length=1000)
    goals: List[QuestGoalAI] = Field(..., min_items=1, max_items=3)
    rewards: QuestRewardAI
    min_level: int = Field(..., ge=1, le=15)

class QuestResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    min_level: int
    goals: List[Dict[str, Any]]
    rewards: Dict[str, Any]
    ai_generated: bool
    model_config = {"from_attributes": True}

class CharacterQuestResponse(BaseModel):
    id: uuid.UUID
    quest_id: uuid.UUID
    quest_name: str
    status: QuestStatus
    progress: List[Dict[str, Any]]
    accepted_at: datetime
    model_config = {"from_attributes": True}

class QuestGenerateRequest(BaseModel):
    quest_type: Optional[str] = Field(None, description="kill, collect, visit или None для случайного")