from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class VKAuthRequest(BaseModel):
    initData: str = Field(..., min_length=10, description="VK initData строка с подписью")

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

class TokenPayload(BaseModel):
    sub: uuid.UUID
    exp: datetime
    iat: datetime
    vk_user_id: int
    type: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    vk_user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
