import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_cloud_wu_with_known_location():
    """wu use-phase should return values when usage_location has wu data."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=wu",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )

    assert res.status_code == 200
    data = res.json()
    wu = data["impacts"]["wu"]

    assert wu["unit"] == "m3 eq."

    # Use phase should have numeric values (not "not implemented")
    assert isinstance(wu["use"], dict)
    assert wu["use"]["value"] == 6.7
    assert wu["use"]["min"] > 0
    assert wu["use"]["max"] > wu["use"]["value"]


@pytest.mark.asyncio
async def test_cloud_wu_without_wu_location():
    """wu use-phase should be 'not implemented' when location has no wu data (e.g. WOR)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get(
            "/v1/cloud/instance?verbose=false&criteria=wu"
            "&instance_type=a1.4xlarge&provider=aws",
        )

    assert res.status_code == 200
    data = res.json()
    wu = data["impacts"]["wu"]

    assert wu["use"] == "not implemented"


@pytest.mark.asyncio
async def test_cloud_wu_combined_with_gwp():
    """wu and gwp can be requested together."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=wu&criteria=gwp",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )

    assert res.status_code == 200
    data = res.json()

    assert "wu" in data["impacts"]
    assert "gwp" in data["impacts"]

    # Both should have use-phase values
    assert isinstance(data["impacts"]["wu"]["use"], dict)
    assert isinstance(data["impacts"]["gwp"]["use"], dict)


@pytest.mark.asyncio
async def test_server_wu_with_known_location():
    """Server wu use-phase should work with a location that has wu data."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false&criteria=wu",
            json={"usage": {"usage_location": "DEU"}},
        )

    assert res.status_code == 200
    data = res.json()
    wu = data["impacts"]["wu"]

    assert isinstance(wu["use"], dict)
    assert wu["use"]["value"] == 50.0
    assert wu["use"]["min"] > 0
    assert wu["use"]["max"] > wu["use"]["value"]


@pytest.mark.asyncio
async def test_cpu_wu_with_known_location():
    """CPU wu use-phase should work with a location that has wu data."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=false&criteria=wu",
            json={"usage": {"usage_location": "FRA"}},
        )

    assert res.status_code == 200
    data = res.json()
    wu = data["impacts"]["wu"]

    assert isinstance(wu["use"], dict)
    assert wu["use"]["value"] == 18.0
    assert wu["use"]["min"] == 3.435
    assert wu["use"]["max"] > wu["use"]["value"]
