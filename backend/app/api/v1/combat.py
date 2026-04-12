"""Эндпоинты боевой системы."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db, get_current_user
from app.models.character import Character
from app.models.combat import CombatSession
from app.schemas.combat import (
    CombatActionRequest,
    CombatActionResult,
    CombatStateResponse,
    CombatStartRequest,
)
from app.services.combat_service import (
    start_combat,
    get_active_combat,
    get_combat_state,
    process_player_attack,
    process_enemy_turn,
)

router = APIRouter(prefix="/combat", tags=["Combat"])

@router.post("/start", response_model=CombatStateResponse)
async def start_combat_endpoint(
    request: CombatStartRequest = CombatStartRequest(),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatStateResponse:
    """Начало боя с врагом."""
    # Получаем персонажа
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    # Проверяем, нет ли уже активного боя
    existing = await get_active_combat(db, str(character.id))
    if existing:
        return await get_combat_state(db, existing, character)
    
    # Начинаем бой
    combat = await start_combat(db, str(character.id), request.enemy_id)
    await db.commit()
    
    return await get_combat_state(db, combat, character)

@router.get("/state", response_model=CombatStateResponse)
async def get_combat_state_endpoint(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatStateResponse:
    """Получение текущего состояния боя."""
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    combat = await get_active_combat(db, str(character.id))
    if not combat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active combat session"
        )
    
    return await get_combat_state(db, combat, character)

@router.post("/action", response_model=CombatActionResult)
async def combat_action_endpoint(
    request: CombatActionRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CombatActionResult:
    """Выполнение действия в бою."""
    char_result = await db.execute(
        select(Character).where(Character.user_id == current_user.id)
    )
    character = char_result.scalar_one_or_none()
    
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Character not found"
        )
    
    combat = await get_active_combat(db, str(character.id))
    if not combat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active combat session"
        )
    
    # Обработка действий
    if request.action == "attack":
        result = await process_player_attack(db, combat, character)
    elif request.action == "defend":
        # Упрощённая защита: снижение урона на 50% в следующем ходе врага
        result = CombatActionResult(
            success=True,
            message="Вы заняли оборонительную позицию. Следующая атака врага будет слабее."
        )
    elif request.action == "use_item":
        # Упрощённо: использование зелья
        if request.item_id:
            result = CombatActionResult(
                success=True,
                message="Вы использовали предмет. (Реализация предметов — Этап 8)"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="item_id required for use_item action"
            )
    elif request.action == "flee":
        # Упрощённый побег: 50% шанс
        import random
        if random.random() > 0.5:
            result = await process_enemy_turn(db, combat, character)
            if not result.battle_ended:
                result.message += " | Побег не удался!"
        else:
            combat.is_active = False
            combat.result = "fled"
            await db.flush()
            result = CombatActionResult(
                success=True,
                message="Вы успешно сбежали из боя!",
                battle_ended=True,
                battle_result="fled"
            )
    elif request.action == "skill":
        result = CombatActionResult(
            success=True,
            message="Навыки будут реализованы на следующем этапе."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown action"
        )
    
    # Если бой не закончен — ход врага
    if not result.battle_ended and request.action == "attack":
        enemy_result = await process_enemy_turn(db, combat, character)
        result.player_damage_taken = enemy_result.player_damage_taken
        result.message += f" | {enemy_result.message}"
        if enemy_result.battle_ended:
            result.battle_ended = True
            result.battle_result = enemy_result.battle_result
    
    await db.commit()
    
    # Обновляем состояние боя в ответе
    if not result.battle_ended:
        updated_combat = await get_active_combat(db, str(character.id))
        if updated_combat:
            result.combat_state = await get_combat_state(db, updated_combat, character)
    
    return result
