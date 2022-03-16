import pytest
# from starlette.testclient import TestClient
import json
from bson import json_util
import logging
# from fastapi.testclient import TestClient
from filter_service import app
from beanie import Document, init_beanie
from httpx import AsyncClient, Request
#logging.basicConfig(level=logging.DEBUG)

@pytest.mark.asyncio
async def test_get_available_filters():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post('/filters')
        assert isinstance(response.json(), list)
        assert isinstance(response.json()[0], str)
        assert response.status_code == 200
