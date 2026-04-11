from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid
from app.schemas.enums import LocationType

class LocationResponse(BaseModel):
    """Информация о локации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    region: str
    coord_x: int
    coord_y: int
    danger_level: int
    min_level: int
    description: Optional[str] = None
    ai_description_generated: bool
    is_safe: bool
    has_shop: bool
    has_tavern: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

class NeighborLocationResponse(BaseModel):
    """Соседняя локация для навигации."""
    id: uuid.UUID
    name: str
    location_type: LocationType
    distance: int
    travel_difficulty: int
    danger_level: int
    is_visited: bool = False
    
    model_config = {"from_attributes": True}

class MoveRequest(BaseModel):
    """Запрос на перемещение."""
    target_location_id: uuid.UUID = Field(..., description="ID целевой локации")

class MoveResponse(BaseModel):
    """Результат перемещения."""
    success: bool
    message: str
    new_location: LocationResponse
    fatigue_added: int
    encounter: Optional[dict] = None
    
    model_config = {"from_attributes": True}
