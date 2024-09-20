from datetime import datetime

from pydantic import BaseModel


class EncodedTokenData(BaseModel):
    exp: datetime
    iat: datetime
    sub: str


class CreateUser(BaseModel):
    name: str
    username: str
    password: str


class CreatedUserData(BaseModel):
    name: str
    username: str


class AuthData(BaseModel):
    username: str
    password: str


class AuthGrantedData(BaseModel):
    access_token: str
    refresh_token: str


class UserMeRequestData(BaseModel):
    access_token: str
