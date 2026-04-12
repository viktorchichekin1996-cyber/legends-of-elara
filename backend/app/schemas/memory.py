"""Схемы для памяти персонажа."""
from typing import List, Dict, Any
import uuid
from pydantic import BaseModel, Field
from datetime import datetime

class MemoryResponse(BaseModel):
    id: uuid.UUID
    memory_type: str
    title: str
    description: str
    importance: int
    tags: List[str]
    data: Dict[str, Any]
    created_at: datetime
    model_config = {"from_attributes": True}