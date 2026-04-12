from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, List
import uuid
from app.schemas.enums import CharacterClass

class CombatActionRequest(BaseModel):
    """Запрос на действие в бою."""
    action: str = Field(..., pattern="^(attack|defend|use_item|flee|skill)$")
    target: Optional[str] = None  # Для навыков с выбором цели
    item_id: Optional[uuid.UUID] = None  # Для использования предметов
    skill_name: Optional[str] = None  # Для использования навыков
    
    @field_validator('action')
    @classmethod
    def validate_action(cls, v: str) -> str:
        if v not in ('attack', 'defend', 'use_item', 'flee', 'skill'):
            raise ValueError('Недопустимое действие')
        return v

class CombatLogEntry(BaseModel):
    """Запись в логе боя."""
    turn: int
    actor: str  # "player" или "enemy"
    action: str
    description: str
    damage: Optional[int] = None
    healing: Optional[int] = None
    is_critical: bool = False
    is_miss: bool = False
    
    model_config = {"from_attributes": True}

class CombatStateResponse(BaseModel):
    """Текущее состояние боя."""
    combat_session_id: uuid.UUID
    enemy_name: str
    enemy_level: int
    enemy_hp_current: int
    enemy_hp_max: int
    player_hp_current: int
    player_hp_max: int
    player_mana_current: int
    player_mana_max: int
    current_turn: int
    is_player_turn: bool
    combat_log: List[CombatLogEntry]
    
    model_config = {"from_attributes": True}

class CombatActionResult(BaseModel):
    """Результат действия в бою."""
    success: bool
    message: str
    player_damage_taken: int = 0
    enemy_damage_taken: int = 0
    player_healing_received: int = 0
    is_critical: bool = False
    is_miss: bool = False
    combat_state: Optional[CombatStateResponse] = None
    battle_ended: bool = False
    battle_result: Optional[str] = None  # "victory", "defeat", "fled"
    rewards: Optional[dict] = None
    
    model_config = {"from_attributes": True}

class CombatStartRequest(BaseModel):
    """Запрос на начало боя (для тестов)."""
    enemy_id: Optional[uuid.UUID] = None  # Если не указан, выбирается случайный по уровню
