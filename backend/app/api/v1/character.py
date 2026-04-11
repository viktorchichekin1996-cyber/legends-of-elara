"""Эндпоинты управления персонажем."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location
from app.models.enums import CHARACTER_CLASS as DB_CHARACTER_CLASS
from app.schemas.character import (
    CharacterCreateRequest,
    CharacterResponse,
    CharacterStatsResponse,
    LevelUpResponse,
)
from app.schemas.enums import CharacterClass
from app.services.character_service import (
    create_character,
    calculate_character_stats,
    calculate_character_resources,
    check_action_allowed,
    apply_level_up,
)
from app.utils.calculations import get_xp_for_level, get_next_level_xp, check_level_up

router = APIRouter(prefix="/character", tags=["Character"])

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_character_endpoint(
    request: CharacterCreateRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterResponse:
    """Создание нового персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У вас уже есть персонаж"
        )
    
    character = await create_character(db, str(current_user.id), request)
    await db.commit()
    await db.refresh(character)
    
    location_result = await db.execute(
        select(Location).where(Location.id == character.current_location_id)
    )
    location = location_result.scalar_one_or_none()
    
    return CharacterResponse(
        id=character.id,
        name=character.name,
        character_class=CharacterClass(character.character_class),
        level=character.level,
        experience=character.experience,
        status=character.status,
        current_location_id=character.current_location_id,
        current_location_name=location.name if location else None,
        stats=calculate_character_stats(character),
        resources=calculate_character_resources(character),
        created_at=character.created_at,
        updated_at=character.updated_at,
    )

@router.get("/", response_model=CharacterResponse)
async def get_character(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterResponse:
    """Получение полного состояния персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден. Создайте персонажа."
        )
    
    location_result = await db.execute(
        select(Location).where(Location.id == character.current_location_id)
    )
    location = location_result.scalar_one_or_none()
    
    return CharacterResponse(
        id=character.id,
        name=character.name,
        character_class=CharacterClass(character.character_class),
        level=character.level,
        experience=character.experience,
        status=character.status,
        current_location_id=character.current_location_id,
        current_location_name=location.name if location else None,
        stats=calculate_character_stats(character),
        resources=calculate_character_resources(character),
        created_at=character.created_at,
        updated_at=character.updated_at,
    )

@router.get("/stats", response_model=CharacterStatsResponse)
async def get_character_stats(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CharacterStatsResponse:
    """Получение характеристик персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )
    
    return calculate_character_stats(character)

@router.post("/levelup", response_model=LevelUpResponse)
async def level_up_character(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LevelUpResponse:
    """Обработка повышения уровня персонажа."""
    result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Персонаж не найден"
        )
    
    leveled_up, new_level = check_level_up(character.experience, character.level)
    
    if not leveled_up:
        next_xp = get_next_level_xp(character.level)
        current_xp_for_level = character.experience - get_xp_for_level(character.level)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недостаточно опыта. Нужно ещё {next_xp - current_xp_for_level} XP"
        )
    
    old_level = character.level
    character.level = new_level
    stats_increased = await apply_level_up(character)
    
    await db.commit()
    
    return LevelUpResponse(
        level=new_level,
        new_experience=character.experience,
        stats_increased=stats_increased,
        resources_restored=True,
        message=f"Поздравляем! Вы достигли {new_level} уровня!"
    )
