import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_cloud_fe_with_known_location():
    """FE use-phase should return values for any location (factor is always 1)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=fe",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )

    assert res.status_code == 200
    data = res.json()
    fe = data["impacts"]["fe"]

    assert fe["unit"] == "MJ"
    assert fe["description"] == "Final energy consumption"

    # Use phase should have numeric values
    assert isinstance(fe["use"], dict)
    assert fe["use"]["value"] > 0

    # Embedded phase should not be implemented for FE
    assert fe["embedded"] == "not implemented"


@pytest.mark.asyncio
async def test_cloud_fe_same_across_countries():
    """FE use-phase should return the same value regardless of country,
    since the factor is always 1."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res_fra = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=fe",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )
        res_nor = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=fe",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "NOR"},
            },
        )

    fra_fe = res_fra.json()["impacts"]["fe"]["use"]["value"]
    nor_fe = res_nor.json()["impacts"]["fe"]["use"]["value"]

    # FE should be identical regardless of country
    assert fra_fe == nor_fe


@pytest.mark.asyncio
async def test_cloud_fe_combined_with_gwp():
    """FE and GWP can be requested together."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=false&criteria=fe&criteria=gwp",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )

    assert res.status_code == 200
    data = res.json()

    assert "fe" in data["impacts"]
    assert "gwp" in data["impacts"]

    # Both should have use-phase values
    assert isinstance(data["impacts"]["fe"]["use"], dict)
    assert isinstance(data["impacts"]["gwp"]["use"], dict)


@pytest.mark.asyncio
async def test_server_fe():
    """Server FE use-phase should work."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false&criteria=fe",
            json={"usage": {"usage_location": "DEU"}},
        )

    assert res.status_code == 200
    data = res.json()
    fe = data["impacts"]["fe"]

    assert isinstance(fe["use"], dict)
    assert fe["use"]["value"] > 0
    assert fe["embedded"] == "not implemented"


@pytest.mark.asyncio
async def test_component_cpu_fe():
    """CPU component FE use-phase should work."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=false&criteria=fe",
            json={"usage": {"usage_location": "FRA"}},
        )

    assert res.status_code == 200
    data = res.json()
    fe = data["impacts"]["fe"]

    assert isinstance(fe["use"], dict)
    assert fe["use"]["value"] > 0
    assert fe["embedded"] == "not implemented"


@pytest.mark.asyncio
async def test_cloud_fe_verbose():
    """Verbose output should include fe_factor with value 1."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/cloud/instance?verbose=true&criteria=fe",
            json={
                "provider": "aws",
                "instance_type": "a1.4xlarge",
                "usage": {"usage_location": "FRA"},
            },
        )

    assert res.status_code == 200
    data = res.json()

    # Verbose should expose the fe_factor
    assert "fe_factor" in data["verbose"]
    assert data["verbose"]["fe_factor"]["value"] == 1
