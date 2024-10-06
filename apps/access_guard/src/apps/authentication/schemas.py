from pydantic import BaseModel


class TokenData(BaseModel):
    exp: int | None = None
    iat: int
    jti: str
    sub: str | int
    type: str


class AuthData(BaseModel):
    username: str
    password: str


class AuthGrantedData(BaseModel):
    access_token: str
    refresh_token: str
