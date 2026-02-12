import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_complete_cpu():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=false",
            json={"core_units": 12, "die_size_per_core": 24.5},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.0204,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 14.93,
                    "min": 14.93,
                    "value": 14.93,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 233.9,
                    "min": 233.9,
                    "value": 233.9,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_complete_cpu_verbose():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=true",
            json={"core_units": 12, "die_size_per_core": 24.5},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.0204,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 14.93,
                    "min": 14.93,
                    "value": 14.93,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 233.9,
                    "min": 233.9,
                    "value": 233.9,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        },
        "verbose": {
            "adp_factor": {
                "max": 2.656e-07,
                "min": 1.32e-08,
                "source": "ADEME Base IMPACTS ®",
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "value": 6.42e-08,
            },
            "avg_power": {
                "max": 182.22,
                "min": 182.22,
                "status": "COMPLETED",
                "unit": "W",
                "value": 182.22,
            },
            "core_units": {"status": "INPUT", "value": 12},
            "die_size": {
                "max": 294.0,
                "min": 294.0,
                "source": "die_size_per_core*core_units",
                "status": "COMPLETED",
                "unit": "mm2",
                "value": 294.0,
            },
            "die_size_per_core": {"status": "INPUT", "unit": "mm2", "value": 24.5},
            "duration": {"unit": "hours", "value": 26280.0},
            "gwp_factor": {
                "max": 0.9,
                "min": 0.023,
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                "Average of 27 european countries",
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "value": 0.38,
            },
            "hours_life_time": {
                "max": 26280.0,
                "min": 26280.0,
                "status": "ARCHETYPE",
                "unit": "hours",
                "value": 26280.0,
            },
            "impacts": {
                "adp": {
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "max": 0.0204,
                        "min": 0.0204,
                        "value": 0.0204,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgSbeq",
                    "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
                },
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {
                        "max": 14.93,
                        "min": 14.93,
                        "value": 14.93,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgCO2eq",
                    "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
                },
                "pe": {
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "max": 233.9,
                        "min": 233.9,
                        "value": 233.9,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "MJ",
                    "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
                },
            },
            "model_range": {"status": "ARCHETYPE", "value": "Xeon Platinum"},
            "params": {
                "source": "From CPU model range",
                "status": "COMPLETED",
                "value": {"a": 171.1813, "b": 0.0354, "c": 36.8953, "d": -10.1336},
            },
            "pe_factor": {
                "max": 468.15,
                "min": 0.013,
                "source": "ADPf / (1-%renewable_energy)",
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "value": 12.874,
            },
            "time_workload": {
                "max": 100.0,
                "min": 0.0,
                "status": "ARCHETYPE",
                "unit": "%",
                "value": 50.0,
            },
            "units": {"max": 1.0, "min": 1.0, "status": "ARCHETYPE", "value": 1.0},
            "usage_location": {
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO",
                "value": "EEE",
            },
            "use_time_ratio": {
                "max": 1.0,
                "min": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "value": 1.0,
            },
        },
    }


@pytest.mark.asyncio
async def test_complete_cpu_with_low_precision():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=false",
            json={"core_units": 12, "die_size_per_core": 20},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.0204,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 13.87,
                    "min": 13.87,
                    "value": 13.87,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 219.6,
                    "min": 219.6,
                    "value": 219.6,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_cpu():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/component/cpu?verbose=false", json={})

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.02042,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 80.85,
                    "min": 9.652,
                    "value": 14.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 1121.0,
                    "min": 162.9,
                    "value": 220.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_multiple_cpu():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=false",
            json={"units": 3, "core_units": 12, "die_size_per_core": 24.5},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.06121,
                    "min": 0.06121,
                    "value": 0.06121,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.003816, "min": 0.0001896, "value": 0.0009},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 44.8,
                    "min": 44.8,
                    "value": 44.8,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 12930.0, "min": 330.4, "value": 5000.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 701.7,
                    "min": 701.7,
                    "value": 701.7,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 6726000.0, "min": 186.8, "value": 200000.0},
            },
        }
    }


@pytest.mark.asyncio
async def test_incomplete_cpu_verbose():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=true",
            json={"core_units": 24, "family": "Skylake"},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.0204,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 17.95,
                    "min": 17.95,
                    "value": 17.95,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 274.5,
                    "min": 274.5,
                    "value": 274.5,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        },
        "verbose": {
            "adp_factor": {
                "max": 2.656e-07,
                "min": 1.32e-08,
                "source": "ADEME Base IMPACTS ®",
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "value": 6.42e-08,
            },
            "avg_power": {
                "max": 182.22,
                "min": 182.22,
                "status": "COMPLETED",
                "unit": "W",
                "value": 182.22,
            },
            "core_units": {"status": "INPUT", "value": 24},
            "die_size": {
                "max": 447.0,
                "min": 447.0,
                "source": "Linear regression on Skylake",
                "status": "COMPLETED",
                "unit": "mm2",
                "value": 447.0,
            },
            "duration": {"unit": "hours", "value": 26280.0},
            "family": {"status": "INPUT", "value": "Skylake"},
            "gwp_factor": {
                "max": 0.9,
                "min": 0.023,
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                "Average of 27 european countries",
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "value": 0.38,
            },
            "hours_life_time": {
                "max": 26280.0,
                "min": 26280.0,
                "status": "ARCHETYPE",
                "unit": "hours",
                "value": 26280.0,
            },
            "impacts": {
                "adp": {
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "max": 0.0204,
                        "min": 0.0204,
                        "value": 0.0204,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgSbeq",
                    "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
                },
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {
                        "max": 17.95,
                        "min": 17.95,
                        "value": 17.95,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgCO2eq",
                    "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
                },
                "pe": {
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "max": 274.5,
                        "min": 274.5,
                        "value": 274.5,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "MJ",
                    "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
                },
            },
            "model_range": {"status": "ARCHETYPE", "value": "Xeon Platinum"},
            "params": {
                "source": "From CPU model range",
                "status": "COMPLETED",
                "value": {"a": 171.1813, "b": 0.0354, "c": 36.8953, "d": -10.1336},
            },
            "pe_factor": {
                "max": 468.15,
                "min": 0.013,
                "source": "ADPf / (1-%renewable_energy)",
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "value": 12.874,
            },
            "time_workload": {
                "max": 100.0,
                "min": 0.0,
                "status": "ARCHETYPE",
                "unit": "%",
                "value": 50.0,
            },
            "units": {"max": 1.0, "min": 1.0, "status": "ARCHETYPE", "value": 1.0},
            "usage_location": {
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO",
                "value": "EEE",
            },
            "use_time_ratio": {
                "max": 1.0,
                "min": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "value": 1.0,
            },
        },
    }


@pytest.mark.asyncio
async def test_incomplete_cpu_verbose_2():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/cpu?verbose=true",
            json={"core_units": 24, "family": "skylak"},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.02041,
                    "min": 0.0204,
                    "value": 0.0204,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 46.77,
                    "min": 10.6,
                    "value": 19.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 662.2,
                    "min": 175.6,
                    "value": 280.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
            },
        },
        "verbose": {
            "adp_factor": {
                "max": 2.656e-07,
                "min": 1.32e-08,
                "source": "ADEME Base IMPACTS ®",
                "status": "DEFAULT",
                "unit": "kg Sbeq/kWh",
                "value": 6.42e-08,
            },
            "avg_power": {
                "max": 182.22,
                "min": 182.22,
                "status": "COMPLETED",
                "unit": "W",
                "value": 182.22,
            },
            "core_units": {"status": "INPUT", "value": 24},
            "die_size": {
                "max": 1910.0,
                "min": 74.0,
                "source": "Average value of all families with 24 cores",
                "status": "COMPLETED",
                "unit": "mm2",
                "value": 485.0,
            },
            "duration": {"unit": "hours", "value": 26280.0},
            "family": {"status": "INPUT", "value": "skylak"},
            "gwp_factor": {
                "max": 0.9,
                "min": 0.023,
                "source": "https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n"
                "Average of 27 european countries",
                "status": "DEFAULT",
                "unit": "kg CO2eq/kWh",
                "value": 0.38,
            },
            "hours_life_time": {
                "max": 26280.0,
                "min": 26280.0,
                "status": "ARCHETYPE",
                "unit": "hours",
                "value": 26280.0,
            },
            "impacts": {
                "adp": {
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {
                        "max": 0.02041,
                        "min": 0.0204,
                        "value": 0.0204,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgSbeq",
                    "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
                },
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {
                        "max": 46.77,
                        "min": 10.6,
                        "value": 19.0,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "kgCO2eq",
                    "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
                },
                "pe": {
                    "description": "Consumption of primary energy",
                    "embedded": {
                        "max": 662.2,
                        "min": 175.6,
                        "value": 280.0,
                        "warnings": ["End of life is not included in the calculation"],
                    },
                    "unit": "MJ",
                    "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
                },
            },
            "model_range": {"status": "ARCHETYPE", "value": "Xeon Platinum"},
            "params": {
                "source": "From CPU model range",
                "status": "COMPLETED",
                "value": {"a": 171.1813, "b": 0.0354, "c": 36.8953, "d": -10.1336},
            },
            "pe_factor": {
                "max": 468.15,
                "min": 0.013,
                "source": "ADPf / (1-%renewable_energy)",
                "status": "DEFAULT",
                "unit": "MJ/kWh",
                "value": 12.874,
            },
            "time_workload": {
                "max": 100.0,
                "min": 0.0,
                "status": "ARCHETYPE",
                "unit": "%",
                "value": 50.0,
            },
            "units": {"max": 1.0, "min": 1.0, "status": "ARCHETYPE", "value": 1.0},
            "usage_location": {
                "status": "DEFAULT",
                "unit": "CodSP3 - NCS Country Codes - NATO",
                "value": "EEE",
            },
            "use_time_ratio": {
                "max": 1.0,
                "min": 1.0,
                "status": "ARCHETYPE",
                "unit": "/1",
                "value": 1.0,
            },
        },
    }


@pytest.mark.asyncio
async def test_empty_gpu():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/component/gpu?verbose=false", json={})

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {"max": 0.005826, "min": 0.005826, "value": 0.005826},
                "unit": "kgSbeq",
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {"max": 575.1, "min": 575.1, "value": 575.1},
                "unit": "kgCO2eq",
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {"max": 7912.0, "min": 7912.0, "value": 7912.0},
                "unit": "MJ",
                "use": "not implemented",
            },
        }
    }


@pytest.mark.asyncio
async def test_complete_gpu_verbose():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/gpu?verbose=true",
            json={"units": 2, "weight": 2.2, "vram": 24, "vram_dies": 12},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {"max": 0.005819, "min": 0.005819, "value": 0.005819},
                "unit": "kgSbeq",
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {"max": 238.6, "min": 238.6, "value": 238.6},
                "unit": "kgCO2eq",
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {"max": 3424.0, "min": 3424.0, "value": 3424.0},
                "unit": "MJ",
                "use": "not implemented",
            },
        },
        "verbose": {
            "casing_weight": {
                "max": 0.79,
                "min": 0.79,
                "status": "ARCHETYPE",
                "unit": "kg",
                "value": 0.79,
            },
            "duration": {"unit": "hours", "value": 26280.0},
            "gpu_surface": {
                "max": 2808.445102929598,
                "min": 2808.445102929598,
                "status": "ARCHETYPE",
                "unit": "mm2",
                "value": 2808.445102929598,
            },
            "heatsink_weight": {
                "max": 0.9,
                "min": 0.9,
                "status": "ARCHETYPE",
                "unit": "kg",
                "value": 0.9,
            },
            "impacts": {
                "adp": {
                    "description": "Use of minerals and fossil ressources",
                    "embedded": {"max": 0.005819, "min": 0.005819, "value": 0.005819},
                    "unit": "kgSbeq",
                    "use": "not implemented",
                },
                "gwp": {
                    "description": "Total climate change",
                    "embedded": {"max": 238.6, "min": 238.6, "value": 238.6},
                    "unit": "kgCO2eq",
                    "use": "not implemented",
                },
                "pe": {
                    "description": "Consumption of primary energy",
                    "embedded": {"max": 3424.0, "min": 3424.0, "value": 3424.0},
                    "unit": "MJ",
                    "use": "not implemented",
                },
            },
            "pwb_surface": {
                "max": 296.0,
                "min": 296.0,
                "status": "ARCHETYPE",
                "unit": "cm2",
                "value": 296.0,
            },
            "transport_boat": {
                "max": 19000.0,
                "min": 19000.0,
                "status": "ARCHETYPE",
                "unit": "km",
                "value": 19000.0,
            },
            "transport_plane": {
                "max": 0.0,
                "min": 0.0,
                "status": "ARCHETYPE",
                "unit": "km",
                "value": 0.0,
            },
            "transport_truck": {
                "max": 1000.0,
                "min": 1000.0,
                "status": "ARCHETYPE",
                "unit": "km",
                "value": 1000.0,
            },
            "units": {"status": "INPUT", "value": 2},
            "vram": {"status": "INPUT", "unit": "gb", "value": 24},
            "vram_dies": {"status": "INPUT", "value": 12},
            "vram_surface": {
                "max": 506.6304769903343,
                "min": 506.6304769903343,
                "status": "COMPLETED",
                "unit": "mm2",
                "value": 506.6304769903343,
            },
            "weight": {"status": "INPUT", "unit": "kg", "value": 2.2},
        },
    }


@pytest.mark.asyncio
async def test_complete_ram():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/ram?verbose=false",
            json={"units": 12, "capacity": 32, "density": 1.79},
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.0338,
                    "min": 0.0338,
                    "value": 0.0338,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 0.0007612, "min": 3.783e-05, "value": 0.00018},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 534.6,
                    "min": 534.6,
                    "value": 534.6,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 2579.0, "min": 65.92, "value": 1100.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 6745.0,
                    "min": 6745.0,
                    "value": 6745.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 1342000.0,
                    "min": 37.26,
                    "value": 40000.0,
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
async def test_empty_ram():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/component/ram?verbose=false", json={})

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.06469,
                    "min": 0.001753,
                    "value": 0.005,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 6.343e-05, "min": 3.153e-06, "value": 1.5e-05},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 2205.0,
                    "min": 7.42,
                    "value": 100.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 214.9, "min": 5.493, "value": 90.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 27370.0,
                    "min": 101.3,
                    "value": 1000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 111800.0,
                    "min": 3.105,
                    "value": 3000.0,
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
async def test_wrong_manuf_ram():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/ram?verbose=false", json={"manufacturer": "oieoiudhehz"}
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.06469,
                    "min": 0.001753,
                    "value": 0.005,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": {"max": 6.343e-05, "min": 3.153e-06, "value": 1.5e-05},
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 2205.0,
                    "min": 7.42,
                    "value": 100.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": {"max": 214.9, "min": 5.493, "value": 90.0},
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 27370.0,
                    "min": 101.3,
                    "value": 1000.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": {
                    "max": 111800.0,
                    "min": 3.105,
                    "value": 3000.0,
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
async def test_wrong_manuf_ssd():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/ssd?verbose=false", json={"manufacturer": "oieoiudhehz"}
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 3.151,
                    "min": 0.006863,
                    "value": 0.002,
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
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 110000.0,
                    "min": 226.3,
                    "value": 50.0,
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
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 1365000.0,
                    "min": 2804.0,
                    "value": 600.0,
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
                "use": "not implemented",
            },
        }
    }


@pytest.mark.asyncio
async def test_complete_ssd():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/ssd?verbose=false", json={"capacity": 400, "density": 50.6}
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.001061,
                    "min": 0.001061,
                    "value": 0.001061,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 23.73,
                    "min": 23.73,
                    "value": 23.73,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 289.8,
                    "min": 289.8,
                    "value": 289.8,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": "not implemented",
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_ssd():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post("/v1/component/ssd?verbose=false", json={})

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 3.151,
                    "min": 0.006863,
                    "value": 0.002,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical characteristics is very "
                        "important. Results should be interpreted "
                        "with caution (see min and max values)",
                    ],
                },
                "unit": "kgSbeq",
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 110000.0,
                    "min": 226.3,
                    "value": 50.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical characteristics is very "
                        "important. Results should be interpreted "
                        "with caution (see min and max values)",
                    ],
                },
                "unit": "kgCO2eq",
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 1365000.0,
                    "min": 2804.0,
                    "value": 600.0,
                    "warnings": [
                        "End of life is not included in the calculation",
                        "Uncertainty from technical characteristics is very "
                        "important. Results should be interpreted "
                        "with caution (see min and max values)",
                    ],
                },
                "unit": "MJ",
                "use": "not implemented",
            },
        }
    }


@pytest.mark.asyncio
async def test_empty_blade():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post(
            "/v1/component/case?verbose=false", json={"case_type": "blade"}
        )

    assert res.json() == {
        "impacts": {
            "adp": {
                "description": "Use of minerals and fossil ressources",
                "embedded": {
                    "max": 0.02767,
                    "min": 0.02767,
                    "value": 0.02767,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgSbeq",
                "use": "not implemented",
            },
            "gwp": {
                "description": "Total climate change",
                "embedded": {
                    "max": 85.9,
                    "min": 85.9,
                    "value": 85.9,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "kgCO2eq",
                "use": "not implemented",
            },
            "pe": {
                "description": "Consumption of primary energy",
                "embedded": {
                    "max": 1229.0,
                    "min": 1229.0,
                    "value": 1229.0,
                    "warnings": ["End of life is not included in the calculation"],
                },
                "unit": "MJ",
                "use": "not implemented",
            },
        }
    }
