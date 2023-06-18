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
                    "die_size_per_core": 24.5
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
                                               'value': 0.25,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0078,
                                          'min': 0.000194,
                                          'significant_figures': 3,
                                          'value': 0.00125}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1100.0,
                                               'min': 1100.0,
                                               'significant_figures': 2,
                                               'value': 1100.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 26000.0,
                                          'min': 340.0,
                                          'significant_figures': 2,
                                          'value': 7400.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 15000.0,
                                              'min': 14000.0,
                                              'significant_figures': 2,
                                              'value': 15000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 13746000.0,
                                         'min': 190.86,
                                         'significant_figures': 5,
                                         'value': 251380.0}}}


@pytest.mark.asyncio
async def test_empty_config_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 88.0,
                                               'min': 0.054,
                                               'significant_figures': 2,
                                               'value': 0.23,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0759,
                                          'min': 8.85e-05,
                                          'significant_figures': 3,
                                          'value': 0.00174}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 3000000.0,
                                               'min': 200.0,
                                               'significant_figures': 2,
                                               'value': 3300.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 260000.0,
                                          'min': 150.0,
                                          'significant_figures': 2,
                                          'value': 10000.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 38000000.0,
                                              'min': 2800.0,
                                              'significant_figures': 2,
                                              'value': 42000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 133820000.0,
                                         'min': 87.149,
                                         'significant_figures': 5,
                                         'value': 349530.0}}}


@pytest.mark.asyncio
async def test_dell_r740_server():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model":
                {
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
                            "die_size_per_core": 24.5
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
                                                'value': 0.15,
                                                'warnings': ['End of life is not included in the '
                                                             'calculation']},
                                   'unit': 'kgSbeq',
                                   'use': {'max': 0.00881,
                                           'min': 0.000219,
                                           'significant_figures': 3,
                                           'value': 0.00142}},
                           'gwp': {'description': 'Total climate change',
                                   'embedded': {'max': 970.0,
                                                'min': 970.0,
                                                'significant_figures': 2,
                                                'value': 970.0,
                                                'warnings': ['End of life is not included in the '
                                                             'calculation']},
                                   'unit': 'kgCO2eq',
                                   'use': {'max': 30000.0,
                                           'min': 380.0,
                                           'significant_figures': 2,
                                           'value': 8400.0}},
                           'pe': {'description': 'Consumption of primary energy',
                                  'embedded': {'max': 13000.0,
                                               'min': 13000.0,
                                               'significant_figures': 2,
                                               'value': 13000.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'MJ',
                                  'use': {'max': 15535000.0,
                                          'min': 215.7,
                                          'significant_figures': 5,
                                          'value': 284100.0}}}


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
                                  'embedded': {'max': 6.7,
                                               'min': 0.11,
                                               'significant_figures': 2,
                                               'value': 0.15,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0078,
                                          'min': 0.000194,
                                          'significant_figures': 3,
                                          'value': 0.00125}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 230000.0,
                                               'min': 1200.0,
                                               'significant_figures': 2,
                                               'value': 1300.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 26000.0,
                                          'min': 340.0,
                                          'significant_figures': 2,
                                          'value': 7400.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 2800000.0,
                                              'min': 15000.0,
                                              'significant_figures': 2,
                                              'value': 17000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 13746000.0,
                                         'min': 190.86,
                                         'significant_figures': 5,
                                         'value': 251380.0}}}


@pytest.mark.asyncio
async def test_partial_server_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/server/?verbose=false', json={
            "model": {
            },
            "configuration": {
                "cpu": {
                    "units": 2,
                    "die_size": 24.5
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
                                  'embedded': {'max': 0.51,
                                               'min': 0.25,
                                               'significant_figures': 2,
                                               'value': 0.26,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0078,
                                          'min': 0.000194,
                                          'significant_figures': 3,
                                          'value': 0.00125}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 9800.0,
                                               'min': 910.0,
                                               'significant_figures': 2,
                                               'value': 1400.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 26000.0,
                                          'min': 340.0,
                                          'significant_figures': 2,
                                          'value': 7400.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 120000.0,
                                              'min': 12000.0,
                                              'significant_figures': 2,
                                              'value': 19000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 13746000.0,
                                         'min': 190.86,
                                         'significant_figures': 5,
                                         'value': 251380.0}}}


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
                                  'embedded': {'max': 79.0,
                                               'min': 0.22,
                                               'significant_figures': 2,
                                               'value': 0.24,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0546,
                                          'min': 9.27e-05,
                                          'significant_figures': 3,
                                          'value': 0.00114}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 2800000.0,
                                               'min': 760.0,
                                               'significant_figures': 2,
                                               'value': 900.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 190000.0,
                                          'min': 160.0,
                                          'significant_figures': 2,
                                          'value': 6800.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 34000000.0,
                                              'min': 11000.0,
                                              'significant_figures': 2,
                                              'value': 13000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 96254000.0,
                                         'min': 91.289,
                                         'significant_figures': 5,
                                         'value': 229570.0}}}


@pytest.mark.asyncio
async def test_custom_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post("/v1/server/?verbose=false&duration=8785", json={
            "usage": {
                "avg_power": 1,
                "usage_location": "FRA"
            }
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 22.0,
                                               'min': 0.014,
                                               'significant_figures': 2,
                                               'value': 0.059,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4.3e-07,
                                          'min': 4.3e-07,
                                          'significant_figures': 2,
                                          'value': 4.3e-07}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 760000.0,
                                               'min': 51.0,
                                               'significant_figures': 2,
                                               'value': 830.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.86,
                                          'min': 0.86,
                                          'significant_figures': 2,
                                          'value': 0.86}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 9400000.0,
                                              'min': 690.0,
                                              'significant_figures': 2,
                                              'value': 10000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 99.0,
                                         'min': 99.0,
                                         'significant_figures': 2,
                                         'value': 99.0}}}
