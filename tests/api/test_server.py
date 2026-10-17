import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_complete_config_server():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false",
            json={
                "model": {},
                "configuration": {
                    "cpu": {"units": 2, "core_units": 24, "die_size_per_core": 24.5},
                    "ram": [
                        {"units": 4, "capacity": 32, "density": 1.79},
                        {"units": 4, "capacity": 16, "density": 1.79},
                    ],
                    "disk": [
                        {"units": 2, "type": "ssd", "capacity": 400, "density": 50.6},
                        {"units": 2, "type": "hdd"},
                    ],
                    "gpu": {"units": 2, "vram": 40},
                    "power_supply": {"units": 2, "unit_weight": 10},
                },
            },
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.2727,
                    "min": 0.2652,
                    "value": 0.2652,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.01032, "min": 4.409e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 1791.0,
                    "min": 1727.0,
                    "value": 1791.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 34980.0, "min": 76.82, "value": 7000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 24620.0,
                    "min": 23640.0,
                    "value": 24620.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 18200000.0,
                    "min": 43.42,
                    "value": 200000.0,
                    "warnings": [
                        "Uncertainty from technical characteristics is very important. "
                        "Results should be interpreted with caution (see "
                        "min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_config_server():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/server/?verbose=false", json={})
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 87.57,
                    "min": 0.05434,
                    "value": 0.2,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.08879, "min": 1.799e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 3034000.0,
                    "min": 200.1,
                    "value": 3000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgCO2eq",
                "use": {"max": 300900.0, "min": 31.35, "value": 8000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 37660000.0,
                    "min": 2750.0,
                    "value": 40000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "MJ",
                "use": {
                    "max": 156500000.0,
                    "min": 17.72,
                    "value": 300000.0,
                    "warnings": [
                        "Uncertainty from technical "
                        "characteristics is very important. "
                        "Results should be interpreted with "
                        "caution (see min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_dell_r740_server():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false",
            json={
                "model": {"name": "R740", "type": "rack", "year": 2020},
                "configuration": {
                    "cpu": {"units": 2, "core_units": 24, "die_size_per_core": 24.5},
                    "ram": [{"units": 12, "capacity": 32, "density": 1.79}],
                    "disk": [
                        {"units": 1, "type": "ssd", "capacity": 400, "density": 50.6}
                    ],
                    "power_supply": {"units": 2, "unit_weight": 2.99},
                },
                "usage": {},
            },
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.1492,
                    "min": 0.1492,
                    "value": 0.1492,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.01074, "min": 5.139e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 967.9,
                    "min": 967.9,
                    "value": 967.9,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 36410.0, "min": 89.55, "value": 7000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 12870.0,
                    "min": 12870.0,
                    "value": 12870.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 18940000.0,
                    "min": 50.61,
                    "value": 200000.0,
                    "warnings": [
                        "Uncertainty from technical characteristics is very important. "
                        "Results should be interpreted with caution (see "
                        "min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_partial_server_1():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false",
            json={
                "model": {},
                "configuration": {
                    "cpu": {"units": 2},
                    "ram": [{"units": 4, "capacity": 32}, {"units": 4, "capacity": 16}],
                    "disk": [{"units": 2, "type": "ssd"}, {"units": 2, "type": "hdd"}],
                },
            },
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 6.674,
                    "min": 0.1128,
                    "value": 0.2,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.01032, "min": 4.409e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 225200.0,
                    "min": 1181.0,
                    "value": 1000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical characteristics is very "
                        "important. Results should be interpreted "
                        "with caution (see min and max values)",
                    ],
                },
                "unit": "kgCO2eq",
                "use": {"max": 34980.0, "min": 76.82, "value": 7000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 2796000.0,
                    "min": 14800.0,
                    "value": 20000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical characteristics is very "
                        "important. Results should be interpreted "
                        "with caution (see min and max values)",
                    ],
                },
                "unit": "MJ",
                "use": {
                    "max": 18200000.0,
                    "min": 43.42,
                    "value": 200000.0,
                    "warnings": [
                        "Uncertainty from technical characteristics is very important. "
                        "Results should be interpreted with caution (see "
                        "min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_partial_server_2():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false",
            json={
                "model": {},
                "configuration": {
                    "cpu": {"units": 2, "die_size": 24.5},
                    "ram": [
                        {"units": 4},
                        {"units": 4, "capacity": 16, "density": 1.79},
                    ],
                    "disk": [
                        {"units": 2, "capacity": 400, "density": 50.6, "type": "ssd"},
                        {"units": 2, "type": "hdd"},
                    ],
                    "power_supply": {"units": 2, "unit_weight": 10},
                },
            },
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.5086,
                    "min": 0.2493,
                    "value": 0.26,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.01032, "min": 4.409e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 9758.0,
                    "min": 902.8,
                    "value": 1400.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 34980.0, "min": 76.82, "value": 7000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 122400.0,
                    "min": 12310.0,
                    "value": 20000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 18200000.0,
                    "min": 43.42,
                    "value": 200000.0,
                    "warnings": [
                        "Uncertainty from technical characteristics is very important. "
                        "Results should be interpreted with caution (see "
                        "min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_partial_server_3():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false",
            json={
                "model": {},
                "configuration": {
                    "ram": [{"units": 4, "capacity": 16, "density": 1.79}],
                    "power_supply": {"units": 2, "unit_weight": 10},
                },
            },
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 79.3,
                    "min": 0.2193,
                    "value": 0.2,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.07773, "min": 2.147e-05, "value": 0.001},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 2752000.0,
                    "min": 753.9,
                    "value": 900.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgCO2eq",
                "use": {"max": 263400.0, "min": 37.42, "value": 7000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 34160000.0,
                    "min": 10610.0,
                    "value": 10000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "MJ",
                "use": {
                    "max": 137000000.0,
                    "min": 21.15,
                    "value": 200000.0,
                    "warnings": [
                        "Uncertainty from technical "
                        "characteristics is very important. "
                        "Results should be interpreted with "
                        "caution (see min and max values)"
                    ],
                },
            },
        }
    }


@pytest.mark.asyncio
async def test_custom_usage_1():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?verbose=false&duration=8785",
            json={"usage": {"avg_power": 1, "usage_location": "FRA"}},
        )
    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 21.95,
                    "min": 0.01362,
                    "value": 0.06,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgSbeq",
                "use": {"max": 4.268e-07, "min": 4.268e-07, "value": 4.268e-07},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 760800.0,
                    "min": 50.16,
                    "value": 800.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "kgCO2eq",
                "use": {"max": 0.8609, "min": 0.8609, "value": 0.8609},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 9442000.0,
                    "min": 689.3,
                    "value": 10000.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical "
                        "characteristics is very "
                        "important. Results should be "
                        "interpreted with caution (see "
                        "min and max values)",
                    ],
                },
                "unit": "MJ",
                "use": {"max": 99.17, "min": 99.17, "value": 99.17},
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_config_server_generic_criteria():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/server/?verbose=false&criteria=adpf", json={})
    assert res.json() == {
        "impacts": {
            "adpf": {
                "description": "Use of fossil resources (including nuclear)",
                "embedded": {
                    "max": 51500.0,
                    "min": 51500.0,
                    "value": 51500.0,
                    "warnings": ["Generic data used for impact calculation."],
                },
                "unit": "MJ",
                "use": {"max": 7789000.0, "min": 17.42, "value": 200000.0},
            }
        }
    }


@pytest.mark.asyncio
async def test_apple_m1_server():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?archetype=mac2.metal&verbose=false&criteria=gwp", json={}
        )

        assert res.json() == {
            "impacts": {
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {
                        "max": 608.2,
                        "min": 237.0,
                        "value": 420.0,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgCO2eq",
                    "use": {"max": 13320.0, "min": 37.02, "value": 3000.0},
                }
            }
        }


@pytest.mark.asyncio
async def test_dellR740_server():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/server/?archetype=dellR740&verbose=false&criteria=gwp", json={}
        )

        assert res.json() == {
            "impacts": {
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {
                        "max": 1186.0,
                        "min": 760.6,
                        "value": 950.0,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgCO2eq",
                    "use": {"max": 18160.0, "min": 89.32, "value": 5000.0},
                }
            }
        }


@pytest.mark.asyncio
async def test_utils_version():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get("/v1/utils/version")
        assert res.status_code == 200
