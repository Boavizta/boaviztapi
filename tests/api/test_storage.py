import copy

import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)

URL = "/v1/storage/"

ISSUE_BODY = {
    "configuration": {
        "capacity": 1000,
        "type": "SSD",
        "manufacturer": "Samsung",
        "replication": 1,
    },
    "usage": {
        "hours_electrical_consumption": 12,
        "usage_location": "FRA",
        "storage": 2000,
    },
}


async def post(body, params="?verbose=false"):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        return await ac.post(URL + params, json=body)


def body_with(**configuration):
    body = copy.deepcopy(ISSUE_BODY)
    body["configuration"].update(configuration)
    return body


def gwp(res):
    impacts = res.json()["impacts"]["gwp"]
    return impacts["embedded"]["value"], impacts["use"]["value"]


@pytest.mark.asyncio
@pytest.mark.parametrize("disk_type", ["SSD", "hdd"])
async def test_issue_body(disk_type):
    res = await post(body_with(type=disk_type))

    assert res.status_code == 200
    assert set(res.json()) == {"impacts"}
    assert set(res.json()["impacts"]) == {"gwp", "adp", "pe"}
    embedded, use = gwp(res)
    assert embedded > 0
    assert use > 0


@pytest.mark.asyncio
async def test_replication_doubles_impacts():
    embedded, use = gwp(await post(ISSUE_BODY))
    embedded_2, use_2 = gwp(await post(body_with(replication=2)))

    # Outputs are rounded to significant figures
    assert embedded_2 == pytest.approx(2 * embedded, rel=0.05)
    assert use_2 == pytest.approx(2 * use, rel=0.05)


@pytest.mark.asyncio
async def test_hours_electrical_consumption_is_use_time_ratio():
    body = copy.deepcopy(ISSUE_BODY)
    del body["usage"]["hours_electrical_consumption"]
    body["usage"]["use_time_ratio"] = 0.5

    assert gwp(await post(body)) == gwp(await post(ISSUE_BODY))


@pytest.mark.asyncio
async def test_default_configuration():
    res = await post({"usage": {"storage": 100}}, params="")

    assert res.status_code == 200
    verbose = res.json()["verbose"]
    assert verbose["storage_type"]["value"] == "SSD"
    assert verbose["capacity"]["status"] == "ARCHETYPE"
    assert verbose["replication"]["value"] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        body_with(type="NVMe"),
        body_with(capacity=0),
        body_with(replication=0),
        {"usage": {"storage": -1}},
        {"usage": {"usage_location": "FRA"}},
        {"configuration": {"type": "SSD"}},
    ],
)
async def test_invalid_body(body):
    res = await post(body)

    assert res.status_code == 422
