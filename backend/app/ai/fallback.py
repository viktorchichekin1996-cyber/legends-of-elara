import random
import logging
from app.ai.parser import AiEventResponse, Choice

logger = logging.getLogger(__name__)

FALLBACK_EVENTS = [
    AiEventResponse(
        description="Тропа петляет среди древних деревьев. Ветер доносит запах сырости и далёкий гул.",
        choices=[
            Choice(text="Идти на звук", action="move"),
            Choice(text="Осмотреть тропу", action="interact"),
            Choice(text="Свернуть в чащу", action="travel")
        ]
    ),
    AiEventResponse(
        description="Старый указатель раскачивается на ветру. Надпись почти стёрлась, но читается слово 'Осторожно'.",
        choices=[
            Choice(text="Обойти стороной", action="travel"),
            Choice(text="Проверить экипировку", action="interact"),
            Choice(text="Устроить привал", action="rest")
        ]
    )
]

def get_fallback_event(character_class: str, location_type: str) -> AiEventResponse:
    """Возвращает безопасное событие при сбое ИИ."""
    logger.warning("AI generation failed. Using fallback event.")
    return random.choice(FALLBACK_EVENTS)
