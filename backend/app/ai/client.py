import logging
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

class YandexGPTClient:
    """Асинхронный клиент для YandexGPT (yandexgpt-lite/latest)."""
    def __init__(self):
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Authorization": f"Api-Key {settings.YANDEX_API_KEY}",
            "Content-Type": "application/json"
        }
        self.model_uri = f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite/latest"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def generate(self, messages: list[dict[str, str]], temperature: float = 0.7, max_tokens: int = 1500) -> str:
        payload = {
            "model_uri": self.model_uri,
            "completion_options": {"temperature": temperature, "max_tokens": max_tokens},
            "messages": messages
        }
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.post(self.base_url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data["result"]["alternatives"][0]["message"]["text"]
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    wait = 2 ** attempt
                    logger.warning(f"YandexGPT rate limit (429). Retry {attempt+1}/{max_retries} after {wait}s")
                    import asyncio
                    await asyncio.sleep(wait)
                    continue
                logger.error(f"YandexGPT HTTP Error {e.response.status_code}: {e.response.text}")
                raise
            except httpx.RequestError as e:
                logger.error(f"YandexGPT Network Error: {e}")
                if attempt == max_retries - 1:
                    raise
                import asyncio
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"YandexGPT Unexpected Error: {e}")
                raise
        raise RuntimeError("YandexGPT generation failed after retries")

    async def close(self):
        await self.client.aclose()
