from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.character import router as character_router
from app.api.v1.combat import router as combat_router
from app.api.v1.locations import router as locations_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.quests import router as quests_router
from app.api.v1.memories import router as memories_router

v1_router = APIRouter()
v1_router.include_router(auth_router)
v1_router.include_router(character_router)
v1_router.include_router(combat_router)
v1_router.include_router(locations_router)
v1_router.include_router(inventory_router)
v1_router.include_router(quests_router)
v1_router.include_router(memories_router)
