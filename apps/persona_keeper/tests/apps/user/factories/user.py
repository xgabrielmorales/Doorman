from polyfactory.factories.pydantic_factory import ModelFactory

from src.apps.user.schemas import CreateUserData


class CreateUserDataFactory(ModelFactory[CreateUserData]):
    __model__ = CreateUserData
