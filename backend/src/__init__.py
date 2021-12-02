from fastapi import FastAPI
from passlib.context import CryptContext

from .clients import AzureClient
from .routers import router


def setup_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    app.azure_client = AzureClient()
    return app


app = setup_app()
