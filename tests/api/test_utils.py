import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_complete_cpu_from_name_detail():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/name_to_cpu?cpu_name=i7-8565U")

        assert res.json() == {
            "core_units": 4,
            "die_size": 123.0,
            "die_size_per_core": None,
            "family": "Whiskey Lake-U",
            "manufacturer": "Intel",
            "model_range": "Core i7",
            "name": "Intel Core i7-8565U",
            "tdp": 28,
            "units": None,
            "usage": {
                "avg_power": None,
                "elec_factors": {
                    "adp": None,
                    "adpe": None,
                    "adpf": None,
                    "ap": None,
                    "ctue": None,
                    "ctuh_c": None,
                    "ctuh_nc": None,
                    "epf": None,
                    "epm": None,
                    "ept": None,
                    "gwp": None,
                    "gwppb": None,
                    "gwppf": None,
                    "gwpplu": None,
                    "ir": None,
                    "lu": None,
                    "mips": None,
                    "odp": None,
                    "pe": None,
                    "pm": None,
                    "pocp": None,
                    "wu": None,
                },
                "hours_life_time": None,
                "time_workload": None,
                "usage_location": None,
                "use_time_ratio": None,
            },
        }


@pytest.mark.asyncio
async def test_complete_cpu_from_name():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/name_to_cpu?cpu_name=deijeijdiejdzij")
        assert res.json() == "CPU name deijeijdiejdzij is not found in our database"


@pytest.mark.asyncio
async def test_get_api_version_is_not_empty_string():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/version")
        assert res.json()


# @pytest.mark.asyncio
# async def test_get_api_version_is_semver():
#     transport = ASGITransport(app=app)
#     async with AsyncClient(transport=transport, base_url="http://test") as ac:
#         res = await ac.get('/v1/utils/version')
#         # Check returned version matches semver regex
#         # See https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string
#         assert re.match("^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$", res.json())


@pytest.mark.asyncio
async def test_get_cloud_regions_all():
    """Test getting all cloud regions without filter"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/cloud_regions")

        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Check structure of response
        for region in data:
            assert "provider" in region
            assert "region" in region
            assert isinstance(region["provider"], str)
            assert isinstance(region["region"], str)

        # Check that we have multiple providers
        providers = set(region["provider"] for region in data)
        assert "aws" in providers
        assert "azure" in providers
        assert "gcp" in providers


@pytest.mark.asyncio
async def test_get_cloud_regions_aws_filter():
    """Test getting AWS cloud regions only"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/cloud_regions?provider=aws")

        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Check that all results are AWS
        for region in data:
            assert region["provider"] == "aws"
            assert "region" in region

        # Check specific AWS regions exist
        regions = [region["region"] for region in data]
        assert "us-east-1" in regions
        assert "eu-west-3" in regions


@pytest.mark.asyncio
async def test_complete_gpu_from_name_detail():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/name_to_gpu?gpu_name=H100+SXM+80GB")

        assert res.status_code == 200
        assert res.json() == {
            "units": None,
            "usage": {
                "use_time_ratio": None,
                "hours_life_time": None,
                "avg_power": None,
                "time_workload": None,
                "usage_location": None,
                "elec_factors": {
                    "gwp": None,
                    "adp": None,
                    "pe": None,
                    "gwppb": None,
                    "gwppf": None,
                    "gwpplu": None,
                    "ir": None,
                    "lu": None,
                    "odp": None,
                    "pm": None,
                    "pocp": None,
                    "wu": None,
                    "mips": None,
                    "adpe": None,
                    "adpf": None,
                    "ap": None,
                    "ctue": None,
                    "ctuh_c": None,
                    "ctuh_nc": None,
                    "epf": None,
                    "epm": None,
                    "ept": None,
                },
            },
            "name": "NVIDIA H100 SXM 80GB",
            "manufacturer": "NVIDIA",
            "weight": 1.69,
            "heatsink_weight": 0.90077,
            "pwb_surface": 296.37,
            "pwb_weight": None,
            "casing_weight": 0.78923,
            "gpu_surface": 2810.4,
            "vram": 80,
            "vram_dies": 6,
            "vram_surface": None,
            "transport_boat": 19000.0,
            "transport_truck": 1000.0,
            "transport_plane": 0.0,
        }


@pytest.mark.asyncio
async def test_complete_gpu_from_name_not_found():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/name_to_gpu?gpu_name=xyznotgpu123")
        assert res.json() == "GPU name xyznotgpu123 is not found in our database"


@pytest.mark.asyncio
async def test_get_all_gpu_names():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/gpu_name")
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        assert "NVIDIA H100 SXM 80GB" in res.json()
