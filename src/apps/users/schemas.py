from pydantic import BaseModel


class UserMeRequestData(BaseModel):
    access_token: str
