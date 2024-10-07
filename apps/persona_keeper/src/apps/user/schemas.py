from pydantic import BaseModel, ConfigDict


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


class UserMeRequestData(BaseModel):
    access_token: str


class UserMeData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    username: str
