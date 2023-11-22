import abc
from enum import IntEnum
from functools import wraps
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.model import Base, Factory
from db.postgres import get_session
from models.model import FactoryCreate


class Status(IntEnum):
    OK = 0
    ALREADY_EXISTS = 1
    NOT_EXIST = 2
    DB_ERROR = 3
    SERVER_ERROR = 4


class Result:
    def __init__(self, status: Status, data: Base = None) -> None:
        self.status = status
        self.data = data


class AbstractStorage(abc.ABC):
    @abc.abstractmethod
    async def create_factory(self, *args, **kwargs):
        ...

    # @abc.abstractmethod
    # async def create_review_for_factory(self, *args, **kwargs):
    #    ...

    @abc.abstractmethod
    async def get_factories(self, *args, **kwargs):
        ...

    @abc.abstractmethod
    async def get_factory(self, *args, **kwargs):
        ...


class PostgresStorage(AbstractStorage):

    def __init__(self, session) -> None:
        self.session = session

    def error_handler(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                res = await func(self, *args, **kwargs)
                return res
            except DatabaseError as e:
                print(e)
                await self.session.rollback()
                return Result(status=Status.DB_ERROR)
            except Exception as e:
                print(e)
                await self.session.rollback()
                return Result(Status.SERVER_ERROR)

        return wrapper

    async def create_factory(self, factory: FactoryCreate, session=None) -> dict:
        factory = Factory(**factory.dict())
        self.session.add(factory)
        await self.session.commit()
        await self.session.refresh(factory)
        print(factory)
        return dict(
            status=HTTPStatus.CREATED,
            message="Factory create",
            data=factory,
            state=Status.OK,
        )

    async def get_factories(self):
        query = select(Factory)
        data = await self.session.execute(query)
        return Result(status=Status.OK, data=data.all())

    async def get_factory(self, factory_id: UUID):
        query = select(Factory).where(Factory.id == factory_id)
        data = await self.session.execute(query)
        return Result(status=Status.OK, data=data.one_or_none())


async def get_storage(session: AsyncSession = Depends(get_session)) -> AbstractStorage:
    return PostgresStorage(session)
