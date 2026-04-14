import hmac
import hashlib
import base64
from urllib.parse import parse_qsl, urlencode
from fastapi import HTTPException, status

def validate_vk_init_data(init_data: str, secret: str) -> dict:
    """
    Валидирует подпись VK initData согласно официальной спецификации.
    Источник: https://dev.vk.com/mini-apps/development/launch-params-sign
    """
    # ✅ Сохраняем пустые параметры (например, vk_access_token_settings=)
    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    
    # Извлекаем подпись (поддерживаем sign и hash)
    sign = parsed.pop("sign", None) or parsed.pop("hash", None)
    
    if not sign:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing sign/hash in initData"
        )
    
    # ✅ Фильтруем только параметры с префиксом vk_
    vk_params = {k: v for k, v in parsed.items() if k.startswith("vk_")}
    
    if not vk_params:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No vk_ parameters found"
        )
    
    # ✅ Сортируем параметры по ключу
    sorted_params = dict(sorted(vk_params.items()))
    
    # ✅ Формируем строку в формате key=value&key=value
    data_check_string = urlencode(sorted_params)
    
    # ✅ Вычисляем HMAC-SHA256 с секретным ключом (без VKWebAppVerify!)
    hmac_hash = hmac.new(
        secret.encode("utf-8"),
        data_check_string.encode("utf-8"),
        hashlib.sha256
    ).digest()
    
    # ✅ Кодируем в Base64 URL-safe формат
    calculated_sign = base64.b64encode(hmac_hash).decode("utf-8")
    calculated_sign = calculated_sign.rstrip("=").replace("+", "-").replace("/", "_")
    
    # Сравниваем подписи
    if not hmac.compare_digest(calculated_sign, sign):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid VK signature"
        )
    
    return parsed