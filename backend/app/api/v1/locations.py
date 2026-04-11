from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.location import Location, LocationConnection
from app.schemas.location import (
    LocationResponse,
    NeighborLocationResponse,
    MoveRequest,
    MoveResponse,
)
from app.services.location_service import (
    get_neighbors,
    move_character,
)

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/current", response_model=LocationResponse)
async def get_current_location_endpoint(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LocationResponse:
    result = await db.execute(
        select(Location)
        .join(Character, Character.current_location_id == Location.id)
        .where(Character.user_id == current_user.id)
    )
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character or location not found")
    
    return LocationResponse.model_validate(location)

@router.get("/neighbors", response_model=list[NeighborLocationResponse])
async def get_neighbor_locations(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[NeighborLocationResponse]:
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    neighbors = await get_neighbors(db, str(character.current_location_id))
    
    return [
        NeighborLocationResponse(
            id=n.id,
            name=n.name,
            location_type=n.location_type,
            distance=1,
            travel_difficulty=1,
            danger_level=n.danger_level,
            is_visited=False,
        )
        for n in neighbors
    ]

@router.post("/move", response_model=MoveResponse)
async def move_to_location(
    request: MoveRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MoveResponse:
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    
    result = await move_character(
        db,
        str(character.id),
        str(request.target_location_id)
    )
    
    await db.commit()
    
    return result
