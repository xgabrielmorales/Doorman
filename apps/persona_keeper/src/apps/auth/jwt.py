import jwt

from src.apps.auth.schemas import TokenData
from src.core.settings import settings


class AuthJWT:
    def decode_token(self, encoded_token: str | bytes | None = None) -> TokenData:
        raw_jwt = jwt.decode(
            jwt=encoded_token,  # type: ignore[arg-type]
            key=settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        return TokenData(**raw_jwt)
