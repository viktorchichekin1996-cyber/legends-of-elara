"""Утилиты для бросков кубиков и расчётов d20."""
import random
from typing import Optional

def roll_d20(modifier: int = 0, advantage: bool = False, disadvantage: bool = False) -> tuple[int, bool]:
    """
    Бросает 1d20 с модификатором.
    
    Возвращает: (результат_броска, был_ли_крит)
    """
    if advantage and disadvantage:
        # Взаимная отмена
        roll = random.randint(1, 20)
    elif advantage:
        roll = max(random.randint(1, 20), random.randint(1, 20))
    elif disadvantage:
        roll = min(random.randint(1, 20), random.randint(1, 20))
    else:
        roll = random.randint(1, 20)
    
    is_critical = roll in (1, 20)
    return roll + modifier, is_critical

def roll_damage(min_dmg: int, max_dmg: int, modifier: int = 0, is_critical: bool = False) -> int:
    """
    Рассчитывает урон.
    
    При критическом успехе урон удваивается.
    """
    base = random.randint(min_dmg, max_dmg) + modifier
    if is_critical and base > 0:
        base *= 2
    return max(0, base)

def calculate_dc(base: int, modifier: int = 0) -> int:
    """Рассчитывает сложность проверки (DC)."""
    return base + modifier

def check_success(roll: int, dc: int) -> bool:
    """Проверяет успех проверки."""
    return roll >= dc
