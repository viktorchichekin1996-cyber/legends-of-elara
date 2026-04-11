import re
import json
import logging
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class Choice(BaseModel):
    text: str
    action: str

class AiEventResponse(BaseModel):
    type: str = "event"
    description: str
    choices: list[Choice]
    mood: str | None = None

async def parse_ai_response(raw_text: str, max_retries: int = 2) -> AiEventResponse:
    """Извлекает и валидирует JSON из ответа ИИ."""
    # Попытка найти JSON внутри markdown блоков ```json ... ```
    json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_text, re.DOTALL)
    json_str = json_match.group(1) if json_match else raw_text

    for attempt in range(max_retries + 1):
        try:
            data = json.loads(json_str)
            return AiEventResponse(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"AI parse attempt {attempt+1} failed: {e}")
            if attempt == max_retries:
                raise ValueError(f"Failed to parse AI response: {e}")
            # В реальном сценарии здесь можно отправить запрос на исправление,
            # но для оптимизации переходим к fallback на уровне сервиса.
            raise
