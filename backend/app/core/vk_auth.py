import hmac
import hashlib
import json
from urllib.parse import parse_qsl, unquote
from fastapi import HTTPException, status

def validate_vk_init_data(init_data: str, secret: str) -> dict:
    parsed = dict(parse_qsl(init_data))
    if "hash" not in parsed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing hash in initData")

    check_hash = parsed.pop("hash")
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    
    # Спецификация VK требует использования "VK Web App Verify" как ключа для HMAC
    secret_key = hmac.new(b"VK Web App Verify", secret.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated_hash, check_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid VK signature")

    if "user" in parsed:
        try:
            parsed["user"] = json.loads(unquote(parsed["user"]))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user data in initData")
            
    return parsed
