import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_empty_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            'provider': 'aws',
            'instance_type': 'a1.4xlarge',
            'usage': {}
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.14,
                                               'min': 0.065,
                                               'significant_figures': 2,
                                               'value': 0.099,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000822,
                                          'min': 2.88e-05,
                                          'significant_figures': 3,
                                          'value': 0.000155}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 630.0,
                                               'min': 260.0,
                                               'significant_figures': 2,
                                               'value': 460.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 2800.0,
                                          'min': 50.0,
                                          'significant_figures': 2,
                                          'value': 920.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8800.0,
                                              'min': 3600.0,
                                              'significant_figures': 2,
                                              'value': 6400.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 1448500.0,
                                         'min': 28.392,
                                         'significant_figures': 5,
                                         'value': 31163.0}}}


@pytest.mark.asyncio
async def test_empty_usage_m6gxlarge():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            'provider': 'aws',
            'instance_type': "m6g.xlarge",
            'usage': {}
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.17,
                                               'min': 0.081,
                                               'significant_figures': 2,
                                               'value': 0.0075,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00242,
                                          'min': 0.000102,
                                          'significant_figures': 3,
                                          'value': 3.44e-05}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1400.0,
                                               'min': 510.0,
                                               'significant_figures': 2,
                                               'value': 55.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 8200.0,
                                          'min': 180.0,
                                          'significant_figures': 2,
                                          'value': 200.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 19000.0,
                                              'min': 6700.0,
                                              'significant_figures': 2,
                                              'value': 730.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 4264300.0,
                                         'min': 100.49,
                                         'significant_figures': 5,
                                         'value': 6893.8}}}


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/instance?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.14,
                                               'min': 0.065,
                                               'significant_figures': 2,
                                               'value': 0.049,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000773,
                                          'min': 2.88e-05,
                                          'significant_figures': 3,
                                          'value': 7.77e-05}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 630.0,
                                               'min': 260.0,
                                               'significant_figures': 2,
                                               'value': 230.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 2600.0,
                                          'min': 50.0,
                                          'significant_figures': 2,
                                          'value': 460.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8800.0,
                                              'min': 3600.0,
                                              'significant_figures': 2,
                                              'value': 3200.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 1363300.0,
                                         'min': 28.392,
                                         'significant_figures': 5,
                                         'value': 15582.0}}}


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/instance?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.28,
                                               'min': 0.15,
                                               'significant_figures': 2,
                                               'value': 0.099,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00716,
                                          'min': 0.000287,
                                          'significant_figures': 3,
                                          'value': 0.000774}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 3500.0,
                                               'min': 1200.0,
                                               'significant_figures': 2,
                                               'value': 1000.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 24000.0,
                                          'min': 500.0,
                                          'significant_figures': 2,
                                          'value': 4600.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 45000.0,
                                              'min': 15000.0,
                                              'significant_figures': 2,
                                              'value': 13000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 12621000.0,
                                         'min': 282.82,
                                         'significant_figures': 5,
                                         'value': 155210.0}}}


@pytest.mark.asyncio
async def test_wrong_input():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            "provider": "test",
            "instance_type": "a1.4xlarge",
            "usage": {}
        })
    assert res.json() == {'detail': 'a1.4xlarge at test not found'}


@pytest.mark.asyncio
async def test_wrong_input_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            "provider": "aws",
            "instance_type": "test",
            "usage": {}
        })
    assert res.json() == {'detail': 'test at aws not found'}


@pytest.mark.asyncio
async def test_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {
                "time_workload": [
                    {
                        "time_percentage": 50,
                        "load_percentage": 0
                    },
                    {
                        "time_percentage": 25,
                        "load_percentage": 60
                    },
                    {
                        "time_percentage": 25,
                        "load_percentage": 100
                    }
                ]
            }})

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.17,
                                               'min': 0.086,
                                               'significant_figures': 2,
                                               'value': 0.12,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00271,
                                          'min': 0.000111,
                                          'significant_figures': 3,
                                          'value': 0.000598}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1300.0,
                                               'min': 470.0,
                                               'significant_figures': 2,
                                               'value': 830.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 9200.0,
                                          'min': 190.0,
                                          'significant_figures': 2,
                                          'value': 3500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 17000.0,
                                              'min': 6300.0,
                                              'significant_figures': 2,
                                              'value': 11000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 4784900.0,
                                         'min': 109.21,
                                         'significant_figures': 5,
                                         'value': 119870.0}}}


@pytest.mark.asyncio
async def test_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {
                "time_workload": 100
            }})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.17,
                                               'min': 0.086,
                                               'significant_figures': 2,
                                               'value': 0.12,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00462,
                                          'min': 0.000189,
                                          'significant_figures': 3,
                                          'value': 0.00102}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1300.0,
                                               'min': 470.0,
                                               'significant_figures': 2,
                                               'value': 830.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 16000.0,
                                          'min': 330.0,
                                          'significant_figures': 2,
                                          'value': 6000.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 17000.0,
                                              'min': 6300.0,
                                              'significant_figures': 2,
                                              'value': 11000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 8152000.0,
                                         'min': 186.06,
                                         'significant_figures': 5,
                                         'value': 204220.0}}}


@pytest.mark.asyncio
async def test_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false&duration=1', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {}
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 5e-06,
                                               'min': 2.5e-06,
                                               'significant_figures': 2,
                                               'value': 3.5e-06,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 1.02e-07,
                                          'min': 4.18e-09,
                                          'significant_figures': 3,
                                          'value': 2.25e-08}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 0.037,
                                               'min': 0.013,
                                               'significant_figures': 2,
                                               'value': 0.024,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.35,
                                          'min': 0.0073,
                                          'significant_figures': 2,
                                          'value': 0.13}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 0.5,
                                              'min': 0.18,
                                              'significant_figures': 2,
                                              'value': 0.32,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 180.46,
                                         'min': 0.0041187,
                                         'significant_figures': 5,
                                         'value': 4.5206}}}


@pytest.mark.asyncio
async def test_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false&duration=2', json={
            "provider": "aws",
            "instance_type": "a1.4xlarge",
            "usage": {
                "usage_location": "FRA",
                "time_workload": [
                    {
                        "time_percentage": "50",
                        "load_percentage": "0"
                    },
                    {
                        "time_percentage": "50",
                        "load_percentage": "50"
                    }
                ]
            }
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 8.1e-06,
                                               'min': 3.7e-06,
                                               'significant_figures': 2,
                                               'value': 5.6e-06,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4.36317e-09,
                                          'min': 3.07988e-09,
                                          'significant_figures': 6,
                                          'value': 3.41354e-09}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 0.036,
                                               'min': 0.015,
                                               'significant_figures': 2,
                                               'value': 0.026,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.0088,
                                          'min': 0.0062,
                                          'significant_figures': 2,
                                          'value': 0.0069}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 0.5,
                                              'min': 0.2,
                                              'significant_figures': 2,
                                              'value': 0.37,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 1.0139,
                                         'min': 0.7157,
                                         'significant_figures': 5,
                                         'value': 0.79324}}}
