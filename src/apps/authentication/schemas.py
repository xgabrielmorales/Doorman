from pydantic import BaseModel


class Token(BaseModel):
    exp: int
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
    first_name: str
    last_name: str
    username: str

    class Config:
        from_attributes = True
        from_attributes = True
