import pytest
from httpx import AsyncClient, ASGITransport
from jsonschema import validate

from boaviztapi.main import app
from tests.json_schemas.electricity import available_countries_schema

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_available_countries():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/electricity/available_countries')
        assert res.status_code == 200
        assert res.json()
        validate(res.json(), available_countries_schema)
