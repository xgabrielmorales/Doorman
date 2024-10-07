import uuid
from datetime import datetime, timedelta

import jwt

from src.core.settings import settings


def generate_mock_token(subject: str | int, token_type: str) -> str:
    now = datetime.utcnow()

    if token_type == "access":
        exp_time = now + timedelta(minutes=15)
    else:
        exp_time = now + timedelta(days=30)

    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(exp_time.timestamp()),
        "type": token_type,
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
