from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=32)
    username: str = Field(max_length=128, unique=True)
    password: str = Field(max_length=128)
