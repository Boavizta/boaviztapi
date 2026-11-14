import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app
from boaviztapi.models.impact import IMPACT_CRITERIAS

pytest_plugins = ("pytest_asyncio",)

ROUTES = [
    ("post", "/v1/component/cpu", {}),
    ("post", "/v1/component/ram", {}),
    ("post", "/v1/component/gpu", {}),
    ("post", "/v1/server/", {}),
    ("post", "/v1/cloud/instance", {"provider": "aws", "instance_type": "a1.4xlarge"}),
    ("post", "/v1/terminal/laptop", {}),
    ("post", "/v1/iot/iot_device?archetype=smart_watch", {}),
]


async def call(method, url, body):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        if method == "get":
            return await ac.get(url)
        return await ac.post(url, json=body)


def with_query(url, query):
    return f"{url}{'&' if '?' in url else '?'}{query}"


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "url", "body"), ROUTES)
async def test_unknown_criterion_is_a_422(method, url, body):
    res = await call(
        method, with_query(url, "verbose=false&criteria=gwp&criteria=bogus"), body
    )

    assert res.status_code == 422
    (error,) = res.json()["detail"]
    assert error["loc"] == ["query", "criteria"]
    assert "Unknown impact criteria: bogus" in error["msg"]
    assert "gwp" in error["msg"]


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "url", "body"), ROUTES)
async def test_criteria_all_returns_every_criterion(method, url, body):
    res = await call(method, with_query(url, "verbose=false&criteria=all"), body)

    assert res.status_code == 200
    assert list(res.json()["impacts"]) == list(IMPACT_CRITERIAS)


@pytest.mark.asyncio
async def test_criteria_all_with_verbose():
    res = await call("post", "/v1/server/?verbose=true&criteria=all", {})

    assert res.status_code == 200
    assert list(res.json()["impacts"]) == list(IMPACT_CRITERIAS)
    assert list(res.json()["verbose"]["CPU-1"]["impacts"]) == list(IMPACT_CRITERIAS)


@pytest.mark.asyncio
async def test_get_route_with_unknown_criterion():
    res = await call("get", "/v1/component/cpu?verbose=false&criteria=bogus", None)

    assert res.status_code == 422
