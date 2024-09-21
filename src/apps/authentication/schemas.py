from datetime import datetime

from pydantic import BaseModel


class EncodedTokenData(BaseModel):
    exp: datetime
    iat: datetime
    sub: str


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
        orm_mode = True
