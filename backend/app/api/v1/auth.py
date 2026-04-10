from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user, security
from app.core.security import create_access_token, create_refresh_token
from app.core.vk_auth import validate_vk_init_data
from app.config import settings
from app.models.user import User
from app.schemas.auth import VKAuthRequest, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/vk", response_model=Token)
async def auth_vk(data: VKAuthRequest, db: AsyncSession = Depends(get_db)):
    """Авторизация через VK initData. Валидирует подпись, создаёт/находит пользователя, возвращает JWT."""
    vk_data = validate_vk_init_data(data.initData, settings.VK_APP_SECRET)
    vk_user_id = vk_data.get("user", {}).get("id")
    
    if not vk_user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="vk_user_id not found in initData")

    vk_user_id_int = int(vk_user_id)

    stmt = select(User).where(User.vk_user_id == vk_user_id_int)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        # SQLAlchemy 2.0 без MappedAsDataclass: создаём объект и устанавливаем поля
        user = User()
        user.vk_user_id = vk_user_id_int
        user.is_active = True
        db.add(user)
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token(user.id, user.vk_user_id)
    refresh_token = create_refresh_token(user.id, user.vk_user_id)
    return Token(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Получение данных текущего авторизованного пользователя."""
    return user

@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user)
):
    """Обновление пары access/refresh токенов."""
    # В продакшене здесь можно добавить проверку revocation списка или типа токена
    access_token = create_access_token(user.id, user.vk_user_id)
    refresh_token = create_refresh_token(user.id, user.vk_user_id)
    return Token(access_token=access_token, refresh_token=refresh_token)
