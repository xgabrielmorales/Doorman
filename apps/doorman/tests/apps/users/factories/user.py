from polyfactory.factories.pydantic_factory import ModelFactory

from src.apps.users.schemas import CreateUserData


class CreateUserDataFactory(ModelFactory[CreateUserData]):
    __model__ = CreateUserData
