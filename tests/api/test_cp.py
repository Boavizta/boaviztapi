import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/consumption_profile/cpu', json={"cpu": {"name": "intel xeon gold 6134", "tdp": 130}})

    assert res.json() == {'a': 35.5688, 'b': 0.2438, 'c': 9.6694, 'd': -0.6087}