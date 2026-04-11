"""Модуль интеграции с YandexGPT."""
from .client import YandexGPTClient
from .cache import PromptCache
from .parser import AiEventResponse, parse_ai_response
from .prompts import build_character_context, format_prompt
from .fallback import get_fallback_event

_gpt_client = None
_prompt_cache = None

def get_gpt_client() -> YandexGPTClient:
    global _gpt_client
    if _gpt_client is None:
        _gpt_client = YandexGPTClient()
    return _gpt_client

def get_prompt_cache() -> PromptCache:
    global _prompt_cache
    if _prompt_cache is None:
        _prompt_cache = PromptCache()
    return _prompt_cache

__all__ = [
    "get_gpt_client", "get_prompt_cache",
    "build_character_context", "format_prompt",
    "parse_ai_response", "AiEventResponse",
    "get_fallback_event"
]
