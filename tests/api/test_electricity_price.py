import pytest
import pytest_asyncio

from jsonschema import validate
from starlette.testclient import TestClient

from boaviztapi.main import app
from tests.json_schemas.electricity import available_countries_schema, electricity_prices_elecmaps_latest_schema, \
    electricity_carbon_intensity_elecmaps_latest_schema

pytest_plugins = ('pytest_asyncio',)

@pytest_asyncio.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.mark.asyncio
async def test_available_countries(client):
    res = client.get('/v1/electricity/available_countries')
    assert res.status_code == 200
    assert res.json()
    validate(res.json(), available_countries_schema)

@pytest.mark.asyncio
async def test_get_electricity_price(client):
    res = client.get('/v1/electricity/price?zone=AT&temporalGranularity=hourly')
    assert res.status_code == 200
    assert res.json()
    validate(res.json(), electricity_prices_elecmaps_latest_schema)

@pytest.mark.asyncio
async def test_get_electricity_price_with_wrong_zone(client):
    res = client.get('/v1/electricity/price?zone=WRONGZONE&temporalGranularity=hourly')
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_get_carbon_intensity(client):
    res = client.get('/v1/electricity/carbon_intensity?zone=AT&temporalGranularity=hourly')
    assert res.status_code == 200
    assert res.json()
    validate(res.json(), electricity_carbon_intensity_elecmaps_latest_schema)

@pytest.mark.asyncio
async def test_get_carbon_intensity_with_wrong_zone(client):
    res = client.get('/v1/electricity/carbon_intensity?zone=WRONGZONE&temporalGranularity=hourly')
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_get_power_breakdown(client):
    res = client.get('/v1/electricity/power_breakdown?zone=AT&temporalGranularity=hourly')
    assert res.status_code == 200
    assert res.json()
    # we don't validate the schema because it varies a lot between zones