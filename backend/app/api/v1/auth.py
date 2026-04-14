from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime, timedelta, timezone
import jwt

from app.api.deps import get_db
from app.models.user import User
from app.core.vk_auth import validate_vk_init_data
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# === СХЕМЫ ===
class VKAuthRequest(BaseModel):
    initData: str = Field(..., min_length=10, description="VK initData строка")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: uuid.UUID
    vk_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# === УТИЛИТЫ JWT ===
def create_access_token(subject: uuid.UUID, vk_user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.JWT_EXPIRE_DAYS)
    to_encode = {
        "sub": str(subject),
        "vk_user_id": vk_user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(subject: uuid.UUID, vk_user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode = {
        "sub": str(subject),
        "vk_user_id": vk_user_id,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# === ЭНДПОИНТЫ ===
@router.post("/vk", response_model=Token)
async def auth_vk(data: VKAuthRequest, db: AsyncSession = Depends(get_db)):
    """Авторизация через VK initData"""
    # Валидируем подпись
    vk_data = validate_vk_init_data(data.initData, settings.VK_APP_SECRET)
    
    # Получаем vk_user_id
    user_info = vk_data.get("user", {})
    vk_user_id = user_info.get("id") or vk_data.get("vk_user_id")
    
    if not vk_user_id:
        raise HTTPException(status_code=400, detail="vk_user_id not found")
    
    vk_user_id_int = int(vk_user_id)
    
    # Ищем пользователя
    stmt = select(User).where(User.vk_user_id == vk_user_id_int)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    # Создаём нового, если нет
    if not user:
        user = User(vk_user_id=vk_user_id_int, is_active=True)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    
    # Генерируем токены
    access_token = create_access_token(user.id, user.vk_user_id)
    refresh_token = create_refresh_token(user.id, user.vk_user_id)
    
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(lambda: None)):  # Заглушка для зависимостей
    """Получение данных текущего пользователя"""
    return user

