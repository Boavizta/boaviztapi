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
    assert res.json() == {
        "gwp": {
            "manufacture": 1100.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 15000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.25,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_empty_config_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={})
    assert res.json() == {
        "gwp": {
            "manufacture": 3300.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 42000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.23,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }


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
    assert res.json() == {
        "gwp": {
            "manufacture": 970.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 13000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.15,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }


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
    assert res.json() == {
        "gwp": {
            "manufacture": 1300.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 17000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.15,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }


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
                        "density": 50.6
                    },
                    {
                        "units": 2
                    }
                ],
                "power_supply": {
                    "units": 2,
                    "unit_weight": 10
                }
            }
        })
    assert res.json() == {
        "gwp": {
            "manufacture": 1400.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 19000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.26,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }


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
    assert res.json() == {
        "gwp": {
            "manufacture": 900.0,
            "use": 696.0,
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 13000.0,
            "use": "Not Implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.24,
            "use": "Not Implemented",
            "unit": "kgSbeq"
        }
    }
