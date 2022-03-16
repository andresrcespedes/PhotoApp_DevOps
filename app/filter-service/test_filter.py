import pytest
from filter_service import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_available_filters():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/filters')
        assert isinstance(response.json(), list)
        assert isinstance(response.json()[0], str)
        assert response.status_code == 200
