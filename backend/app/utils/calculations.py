"""Формулы игровых расчётов."""

def calculate_modifier(stat_value: int) -> int:
    """
    Рассчитывает модификатор характеристики.
    Формула: (stat - 10) // 2
    """
    return (stat_value - 10) // 2

def clamp_value(value: int, min_val: int, max_val: int) -> int:
    """Ограничивает значение в заданных границах."""
    return max(min_val, min(value, max_val))

def get_xp_for_level(level: int) -> int:
    """Возвращает порог опыта для заданного уровня."""
    from app.utils.constants import XP_THRESHOLDS
    return XP_THRESHOLDS.get(level, 0)

def get_next_level_xp(level: int) -> int:
    """Возвращает опыт, необходимый для следующего уровня."""
    from app.utils.constants import XP_THRESHOLDS
    if level >= 15:
        return 0
    return XP_THRESHOLDS.get(level + 1, 0) - XP_THRESHOLDS.get(level, 0)

def check_level_up(current_xp: int, current_level: int) -> tuple[bool, int]:
    """
    Проверяет, достиг ли персонаж следующего уровня.
    Возвращает: (уровень_повышен, новый_уровень)
    """
    from app.utils.constants import XP_THRESHOLDS
    for level in range(current_level + 1, 16):
        if current_xp >= XP_THRESHOLDS.get(level, float('inf')):
            return True, level
    return False, current_level

def calculate_effective_stat(base_stat: int, equipment_bonus: int = 0, buff_bonus: int = 0) -> int:
    """Рассчитывает эффективное значение характеристики."""
    return base_stat + equipment_bonus + buff_bonus
