from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends, Request, status as fastapi_status
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.model import FactoryCreate, Factory
from services.factory import FactoryService, get_factory_service

router = APIRouter()


@router.post(
    "/",
    summary="Создание factory",
    description="Создание factory",
    response_model=FactoryCreate,
    status_code=fastapi_status.HTTP_201_CREATED,
)
async def create_role(
        request: Request,
        factory: FactoryCreate,
        factory_service: FactoryService = Depends(get_factory_service),
        session: AsyncSession = Depends(get_session),
):
    res = await factory_service.create_factory(factory=factory, session=session)
    if res["status"] != HTTPStatus.CREATED:
        raise HTTPException(status_code=res["status"], detail=res["message"])
    return res
