import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import factory
from src.core.config import settings

app = FastAPI(
    title=settings.service_name,
    docs_url="/api/factories/openapi",
    openapi_url="/api/factories/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(factory.router, prefix="/api/v1/factory", tags=["factory"])


def main():
    import asyncio
    import platform

    windows_platform = platform.system() == "Windows"
    if windows_platform:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    main()
