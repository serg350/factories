from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, Request, status as fastapi_status
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from db.storage import Status, Result
from models.model import FactoryCreate, Factory
from services.factory import FactoryService, get_factory_service

router = APIRouter()


@router.post(
    "/factories",
    summary="Создание factory",
    description="Создание factory",
    status_code=fastapi_status.HTTP_201_CREATED,
)
async def create_factory(
        factory: FactoryCreate,
        factory_service: FactoryService = Depends(get_factory_service),
        session: AsyncSession = Depends(get_session),
):
    res = await factory_service.create_factory(factory=factory, session=session)
    if res["status"] != HTTPStatus.CREATED:
        raise HTTPException(status_code=res["status"], detail=res["message"])
    return res


@router.get(
    "/factories",
    summary="Получение списка фабрик",
    description="Получение списка фабрик",
    status_code=fastapi_status.HTTP_200_OK,
)
async def get_factory(
    request: Request,
    factory_service: FactoryService = Depends(get_factory_service),
):
    result: Result = await factory_service.get_factories()

    if result.status != Status.OK:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="Select error.")

    return [row[0] for row in result.data]


@router.get(
    "/factory/{factory_id}",
    summary="Получение информации по фабрике по id",
    description="Получение информации по фабрике по id",
    status_code=fastapi_status.HTTP_200_OK,
)
async def get_factory(
    request: Request,
    factory_id: UUID,
    factory_service: FactoryService = Depends(get_factory_service),
):
    result: Result = await factory_service.get_factory(factory_id=factory_id)

    if result.status != Status.OK:
        raise HTTPException(status_code=fastapi_status.HTTP_404_NOT_FOUND, detail="Select error.")

    return result
