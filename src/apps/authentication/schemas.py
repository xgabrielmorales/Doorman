from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
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


class CreateUserData(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class CreatedUserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    username: str
