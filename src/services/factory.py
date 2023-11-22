from fastapi import Depends

from db.storage import AbstractStorage, get_storage
from models.model import FactoryCreate, Factory


class FactoryService:
    def __init__(self, storage: AbstractStorage):
        self.storage = storage

    async def create_factory(self, factory: FactoryCreate, session) -> Factory:
        result = await self.storage.create_factory(factory, session)
        return result


def get_factory_service(storage: AbstractStorage = Depends(get_storage)) -> FactoryService:
    return FactoryService(storage)