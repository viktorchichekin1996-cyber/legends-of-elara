from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid
from app.schemas.enums import CharacterClass, CharacterStatus

class CharacterCreateRequest(BaseModel):
    """Запрос на создание персонажа."""
    name: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$")
    character_class: CharacterClass

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if v.lower() in ['admin', 'moderator', 'gm', 'god']:
            raise ValueError('Имя зарезервировано')
        return v.strip().title()

class CharacterStatsResponse(BaseModel):
    """Характеристики персонажа с модификаторами."""
    strength: int
    agility: int
    intelligence: int
    strength_mod: int
    agility_mod: int
    intelligence_mod: int
    strength_effective: int
    agility_effective: int
    intelligence_effective: int
    
    model_config = {"from_attributes": True}

class CharacterResourcesResponse(BaseModel):
    """Ресурсы персонажа."""
    hp_current: int
    hp_max: int
    mana_current: int
    mana_max: int
    stamina_current: int
    stamina_max: int
    fatigue: int
    gold: int
    inventory_slots: int
    inventory_slots_used: Optional[int] = None
    
    model_config = {"from_attributes": True}

class CharacterResponse(BaseModel):
    """Полное состояние персонажа."""
    id: uuid.UUID
    name: str
    character_class: CharacterClass
    level: int
    experience: int
    status: CharacterStatus
    current_location_id: uuid.UUID
    current_location_name: Optional[str] = None
    stats: CharacterStatsResponse
    resources: CharacterResourcesResponse
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class LevelUpResponse(BaseModel):
    """Ответ на повышение уровня."""
    level: int
    new_experience: int
    stats_increased: dict
    resources_restored: bool
    message: str
    
    model_config = {"from_attributes": True}
