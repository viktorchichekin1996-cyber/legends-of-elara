"""Централизованный сервис операций с золотом. Этап 10.1"""
import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.models.character import Character
from app.models.shop import Transaction

async def record_transaction(
    session: AsyncSession,
    character_id: uuid.UUID,
    transaction_type: str,
    amount: int,
    description: Optional[str] = None,
    reference_id: Optional[uuid.UUID] = None
) -> Transaction:
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    new_balance = char.gold + amount
    if new_balance < 0:
        raise HTTPException(status_code=400, detail=f"Недостаточно золота. Нужно: {abs(amount)}, есть: {char.gold}")
    char.gold = new_balance
    txn = Transaction(
        id=uuid.uuid4(),
        character_id=character_id,
        transaction_type=transaction_type,
        amount=amount,
        description=description,
        reference_id=reference_id,
        balance_after=new_balance
    )
    session.add(txn)
    await session.flush()
    return txn

async def can_afford(session: AsyncSession, character_id: uuid.UUID, cost: int) -> bool:
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    return char is not None and char.gold >= cost

async def get_character_gold(session: AsyncSession, character_id: uuid.UUID) -> int:
    char = (await session.execute(select(Character).where(Character.id == character_id))).scalar_one_or_none()
    if not char:
        raise HTTPException(status_code=404, detail="Персонаж не найден")
    return char.gold
