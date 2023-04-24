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
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.26,
                                            'min': 0.25,
                                            'significant_figures': 2,
                                            'value': 0.25},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0195,
                                          'min': 5.53e-09,
                                          'significant_figures': 3,
                                          'value': 0.000313}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 1100.0,
                                            'min': 1100.0,
                                            'significant_figures': 2,
                                            'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 66000.0,
                                          'min': 0.0096,
                                          'significant_figures': 2,
                                          'value': 1900.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 15000.0,
                                           'min': 14000.0,
                                           'significant_figures': 2,
                                           'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 34370000.0,
                                         'min': 0.005447,
                                         'significant_figures': 4,
                                         'value': 62850.0}}}


@pytest.mark.asyncio
async def test_empty_config_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 9.4,
                                            'min': 0.055,
                                            'significant_figures': 2,
                                            'value': 0.23},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.19,
                                          'min': 2.53e-09,
                                          'significant_figures': 3,
                                          'value': 0.000436}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 310000.0,
                                            'min': 220.0,
                                            'significant_figures': 2,
                                            'value': 3300.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 640000.0,
                                          'min': 0.0044,
                                          'significant_figures': 2,
                                          'value': 2600.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 3800000.0,
                                           'min': 3000.0,
                                           'significant_figures': 2,
                                           'value': 42000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 334600000.0,
                                         'min': 0.002487,
                                         'significant_figures': 4,
                                         'value': 87380.0}}}


@pytest.mark.asyncio
async def test_dell_r740_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model":
                {
                    "embeddedr": "Dell",
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
            }
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.15,
                                            'min': 0.15,
                                            'significant_figures': 2,
                                            'value': 0.15},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.022,
                                          'min': 6.25e-09,
                                          'significant_figures': 3,
                                          'value': 0.000354}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 970.0,
                                            'min': 970.0,
                                            'significant_figures': 2,
                                            'value': 970.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 75000.0,
                                          'min': 0.011,
                                          'significant_figures': 2,
                                          'value': 2100.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 13000.0,
                                           'min': 13000.0,
                                           'significant_figures': 2,
                                           'value': 13000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 38840000.0,
                                         'min': 0.006156,
                                         'significant_figures': 4,
                                         'value': 71020.0}}}


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
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.9,
                                            'min': 0.34,
                                            'significant_figures': 2,
                                            'value': 0.15},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0195,
                                          'min': 5.53e-09,
                                          'significant_figures': 3,
                                          'value': 0.000313}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 23000.0,
                                            'min': 8900.0,
                                            'significant_figures': 2,
                                            'value': 1300.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 66000.0,
                                          'min': 0.0096,
                                          'significant_figures': 2,
                                          'value': 1900.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 290000.0,
                                           'min': 110000.0,
                                           'significant_figures': 2,
                                           'value': 17000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 34370000.0,
                                         'min': 0.005447,
                                         'significant_figures': 4,
                                         'value': 62850.0}}}


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
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.28,
                                            'min': 0.25,
                                            'significant_figures': 2,
                                            'value': 0.26},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0195,
                                          'min': 5.53e-09,
                                          'significant_figures': 3,
                                          'value': 0.000313}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 1900.0,
                                            'min': 980.0,
                                            'significant_figures': 2,
                                            'value': 1400.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 66000.0,
                                          'min': 0.0096,
                                          'significant_figures': 2,
                                          'value': 1900.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 24000.0,
                                           'min': 13000.0,
                                           'significant_figures': 2,
                                           'value': 19000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 34370000.0,
                                         'min': 0.005447,
                                         'significant_figures': 4,
                                         'value': 62850.0}}}


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
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 8.4,
                                            'min': 0.22,
                                            'significant_figures': 2,
                                            'value': 0.24},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.137,
                                          'min': 2.65e-09,
                                          'significant_figures': 3,
                                          'value': 0.000286}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 280000.0,
                                            'min': 760.0,
                                            'significant_figures': 2,
                                            'value': 900.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 460000.0,
                                          'min': 0.0046,
                                          'significant_figures': 2,
                                          'value': 1700.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 3400000.0,
                                           'min': 11000.0,
                                           'significant_figures': 2,
                                           'value': 13000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 240600000.0,
                                         'min': 0.002605,
                                         'significant_figures': 4,
                                         'value': 57390.0}}}


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
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 9.4,
                                            'min': 0.055,
                                            'significant_figures': 2,
                                            'value': 0.23},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4e-07,
                                          'min': 4e-07,
                                          'significant_figures': 1,
                                          'value': 4e-07}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 310000.0,
                                            'min': 220.0,
                                            'significant_figures': 2,
                                            'value': 3300.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.9,
                                          'min': 0.9,
                                          'significant_figures': 1,
                                          'value': 0.9}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 3800000.0,
                                           'min': 3000.0,
                                           'significant_figures': 2,
                                           'value': 42000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 100.0,
                                         'min': 100.0,
                                         'significant_figures': 1,
                                         'value': 100.0}}}
