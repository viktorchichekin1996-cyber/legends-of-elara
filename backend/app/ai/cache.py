import hashlib
import json
import logging
import redis.asyncio as aioredis
from app.config import settings

logger = logging.getLogger(__name__)

class PromptCache:
    """Redis-кэш для промптов и ответов YandexGPT."""
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self.client = aioredis.from_url(self.redis_url, decode_responses=True)
        self.ttl = 3600  # 1 час

    async def get(self, prompt_hash: str) -> str | None:
        try:
            return await self.client.get(f"ai:prompt:{prompt_hash}")
        except Exception as e:
            logger.error(f"Redis cache GET error: {e}")
            return None

    async def set(self, prompt_hash: str, response: str) -> None:
        try:
            await self.client.set(f"ai:prompt:{prompt_hash}", response, ex=self.ttl)
        except Exception as e:
            logger.error(f"Redis cache SET error: {e}")

    def hash_prompt(self, prompt_data: list[dict]) -> str:
        content = json.dumps(prompt_data, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def close(self):
        await self.client.close()
