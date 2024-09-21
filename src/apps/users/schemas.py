from pydantic import BaseModel


class UserMeRequestData(BaseModel):
    access_token: str


class UserMeData(BaseModel):
    first_name: str
    last_name: str
    username: str

    class Config:
        from_attributes = True
        orm_mode = True
