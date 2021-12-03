from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext

from .clients import AzureClient
from .routers import router
from .settings import settings


def setup_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.add_middleware(CORSMiddleware, **settings.CORS_SETTINGS)
    app.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    app.azure_client = AzureClient()
    return app


app = setup_app()
