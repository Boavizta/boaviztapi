import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_config_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model": {
            },
            "configuration": {
                "cpu": {
                    "units": 2,
                    "core_units": 24,
                    "die_size": 0.245
                },
                "ram": [
                    {
                        "units": 4,
                        "capacity": 32,
                        "density": 1.79
                    },
                    {
                        "units": 4,
                        "capacity": 16,
                        "density": 1.79
                    }
                ],
                "disk": [
                    {
                        "units": 2,
                        "type": "ssd",
                        "capacity": 400,
                        "density": 50.6
                    },
                    {
                        "units": 2,
                        "type": "hdd"
                    }
                ],
                "power_supply": {
                    "units": 2,
                    "unit_weight": 10
                }
            }
        })
    assert res.json() == {'adp': {'manufacture': 0.25, 'unit': 'kgSbeq', 'use': 0.000313},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 1900.0},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 62850.0}}


@pytest.mark.asyncio
async def test_empty_config_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={})
    assert res.json() == {'adp': {'manufacture': 0.23, 'unit': 'kgSbeq', 'use': 0.000436},
                          'gwp': {'manufacture': 3300.0, 'unit': 'kgCO2eq', 'use': 2600.0},
                          'pe': {'manufacture': 42000.0, 'unit': 'MJ', 'use': 87380.0}}


@pytest.mark.asyncio
async def test_dell_r740_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model":
                {
                    "manufacturer": "Dell",
                    "name": "R740",
                    "type": "rack",
                    "year": 2020
                },
            "configuration":
                {
                    "cpu":
                        {
                            "units": 2,
                            "core_units": 24,
                            "die_size_per_core": 0.245
                        },
                    "ram":
                        [
                            {
                                "units": 12,
                                "capacity": 32,
                                "density": 1.79
                            }
                        ],
                    "disk":
                        [
                            {
                                "units": 1,
                                "type": "ssd",
                                "capacity": 400,
                                "density": 50.6
                            }
                        ],
                    "power_supply":
                        {
                            "units": 2,
                            "unit_weight": 2.99
                        }
                },
            "usage": {
                "100": {
                    "time": 0.15,
                    "power": 1.0
                },
                "50": {
                    "time": 0.55,
                    "power": 0.7235
                },
                "10": {
                    "time": 0.2,
                    "power": 0.5118
                },
                "idle": {
                    "time": 0.1,
                    "power": 0.3941
                }
            }
        }
                            )
    assert res.json() == {'adp': {'manufacture': 0.15, 'unit': 'kgSbeq', 'use': 0.000354},
                          'gwp': {'manufacture': 970.0, 'unit': 'kgCO2eq', 'use': 2100.0},
                          'pe': {'manufacture': 13000.0, 'unit': 'MJ', 'use': 71020.0}}


@pytest.mark.asyncio
async def test_partial_server_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model": {
            },
            "configuration": {
                "cpu": {
                    "units": 2
                },
                "ram": [
                    {
                        "units": 4,
                        "capacity": 32
                    },
                    {
                        "units": 4,
                        "capacity": 16
                    }
                ],
                "disk": [
                    {
                        "units": 2,
                        "type": "ssd"
                    },
                    {
                        "units": 2,
                        "type": "hdd"
                    }
                ]
            }
        })
    assert {'adp': {'manufacture': 0.15, 'unit': 'kgSbeq', 'use': 0.000313},
            'gwp': {'manufacture': 1300.0, 'unit': 'kgCO2eq', 'use': 1900.0},
            'pe': {'manufacture': 17000.0, 'unit': 'MJ', 'use': 62850.0}}


@pytest.mark.asyncio
async def test_partial_server_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model": {
            },
            "configuration": {
                "cpu": {
                    "units": 2,
                    "die_size": 0.245
                },
                "ram": [
                    {
                        "units": 4
                    },
                    {
                        "units": 4,
                        "capacity": 16,
                        "density": 1.79
                    }
                ],
                "disk": [
                    {
                        "units": 2,
                        "capacity": 400,
                        "density": 50.6,
                        "type": "ssd"
                    },
                    {
                        "units": 2,
                        "type": "hdd"
                    }
                ],
                "power_supply": {
                    "units": 2,
                    "unit_weight": 10
                }
            }
        })
    assert res.json() == {'adp': {'manufacture': 0.26, 'unit': 'kgSbeq', 'use': 0.000313},
                          'gwp': {'manufacture': 1400.0, 'unit': 'kgCO2eq', 'use': 1900.0},
                          'pe': {'manufacture': 19000.0, 'unit': 'MJ', 'use': 62850.0}}


@pytest.mark.asyncio
async def test_partial_server_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model": {
            },
            "configuration": {

                "ram": [
                    {
                        "units": 4,
                        "capacity": 16,
                        "density": 1.79

                    }
                ],
                "power_supply": {
                    "units": 2,
                    "unit_weight": 10
                }
            }
        })
    assert res.json() == {'adp': {'manufacture': 0.24, 'unit': 'kgSbeq', 'use': 0.000286},
                          'gwp': {'manufacture': 900.0, 'unit': 'kgCO2eq', 'use': 1700.0},
                          'pe': {'manufacture': 13000.0, 'unit': 'MJ', 'use': 57390.0}}


@pytest.mark.asyncio
async def test_custom_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "usage": {
                "years_use_time": 1,
                "days_use_time": 1,
                "hours_use_time": 1,
                "hours_electrical_consumption": 1,
                "usage_location": "FRA"
            }
        })
    assert res.json() == {'adp': {'manufacture': 0.23, 'unit': 'kgSbeq', 'use': 4e-07},
                          'gwp': {'manufacture': 3300.0, 'unit': 'kgCO2eq', 'use': 0.9},
                          'pe': {'manufacture': 42000.0, 'unit': 'MJ', 'use': 100.0}}
