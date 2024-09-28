from pydantic import BaseModel, ConfigDict


class UserMeRequestData(BaseModel):
    access_token: str


class UserMeData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    username: str
