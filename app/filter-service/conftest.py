import pytest
import pytest_asyncio

import motor
from fastapi.testclient import TestClient
from beanie import Document, init_beanie
from models import Filter
from pydantic import BaseModel,BaseSettings

@pytest_asyncio.fixture
async def clearFilters():
    await Filter.find().delete()

@pytest_asyncio.fixture
async def initDB():
    class Settings(BaseSettings):
        mongo_host: str = "localhost"
        mongo_port: str = "27017"
        mongo_user: str = ""
        mongo_password: str = ""
        database_name: str = "filters_test"

    settings = Settings()

    conn = f"mongodb://"
    if settings.mongo_user:
        conn += f"{settings.mongo_user}:{settings.mongo_password}@"
    conn += f"{settings.mongo_host}:{settings.mongo_port}"
    client = motor.motor_asyncio.AsyncIOMotorClient(conn)  # type: ignore
    await init_beanie(database=client["filter-test"], document_models=[Filter])
    yield

