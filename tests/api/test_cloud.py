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
                                  'embedded': {'max': 0.1414,
                                               'min': 0.06512,
                                               'value': 0.099,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0008218, 'min': 2.883e-05, 'value': 0.00016}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 636.6,
                                               'min': 258.9,
                                               'value': 450.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 2785.0, 'min': 50.23, 'value': 900.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8846.0,
                                              'min': 3542.0,
                                              'value': 6300.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 1448000.0,
                                         'min': 28.39,
                                         'value': 30000.0,
                                         'warnings': ['Uncertainty from technical characteristics is very important. '
                                                      'Results should be interpreted with caution (see '
                                                      'min and max values)']}}}


@pytest.mark.asyncio
async def test_empty_usage_m6gxlarge():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false', json={
            'provider': 'aws',
            'instance_type': "m6g.xlarge",
            'usage': {}
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.01088,
                                               'min': 0.005075,
                                               'value': 0.0075,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0001512, 'min': 6.377e-06, 'value': 3e-05}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 89.24,
                                               'min': 31.58,
                                               'value': 55.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 512.4, 'min': 11.11, 'value': 200.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 1168.0,
                                              'min': 416.4,
                                              'value': 730.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 266500.0, 'min': 6.281, 'value': 10000.0}}}


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/instance?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.07069,
                                               'min': 0.03256,
                                               'value': 0.049,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0003867, 'min': 1.441e-05, 'value': 8e-05}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 318.3,
                                               'min': 129.5,
                                               'value': 230.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 1310.0, 'min': 25.12, 'value': 500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 4423.0,
                                              'min': 1771.0,
                                              'value': 3200.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 681600.0, 'min': 14.2, 'value': 20000.0}}}


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/instance?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.1383,
                                               'min': 0.07273,
                                               'value': 0.099,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00358, 'min': 0.0001436, 'value': 0.0008}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1709.0,
                                               'min': 579.6,
                                               'value': 1000.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 12130.0, 'min': 250.2, 'value': 5000.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 21780.0,
                                              'min': 7481.0,
                                              'value': 13000.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 6310000.0, 'min': 141.4, 'value': 200000.0}}}


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
                                  'embedded': {'max': 0.1744,
                                               'min': 0.08627,
                                               'value': 0.124,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.002715, 'min': 0.0001109, 'value': 0.0006}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1216.0,
                                               'min': 459.3,
                                               'value': 780.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 9199.0, 'min': 193.2, 'value': 3500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 16090.0,
                                              'min': 6121.0,
                                              'value': 10500.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 4785000.0, 'min': 109.2, 'value': 100000.0}}}


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
                                  'embedded': {'max': 0.1744,
                                               'min': 0.08627,
                                               'value': 0.124,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.004625, 'min': 0.0001889, 'value': 0.001}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 1216.0,
                                               'min': 459.3,
                                               'value': 780.0,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 15670.0, 'min': 329.2, 'value': 6000.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 16090.0,
                                              'min': 6121.0,
                                              'value': 10500.0,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 8152000.0, 'min': 186.1, 'value': 200000.0}}}


@pytest.mark.asyncio
async def test_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/instance?verbose=false&duration=1', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {}
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 4.977e-06,
                                               'min': 2.462e-06,
                                               'value': 3.5e-06,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 1.024e-07, 'min': 4.182e-09, 'value': 2.3e-08}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 0.0347,
                                               'min': 0.01311,
                                               'value': 0.022,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.3469, 'min': 0.007287, 'value': 0.13}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 0.4591,
                                              'min': 0.1747,
                                              'value': 0.3,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 180.5,
                                         'min': 0.004119,
                                         'value': 5.0,
                                         'warnings': ['Uncertainty from technical characteristics is very important. '
                                                      'Results should be interpreted with caution (see '
                                                      'min and max values)']}}}


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
                                  'embedded': {'max': 8.07e-06,
                                               'min': 3.717e-06,
                                               'value': 5.6e-06,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4.363e-09, 'min': 3.08e-09, 'value': 3.4e-09}},
                          'gwp': {'description': 'Total climate change',
                                  'embedded': {'max': 0.03634,
                                               'min': 0.01478,
                                               'value': 0.026,
                                               'warnings': ['End of life is not included in the '
                                                            'calculation']},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.008802, 'min': 0.006213, 'value': 0.0069}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 0.5049,
                                              'min': 0.2022,
                                              'value': 0.36,
                                              'warnings': ['End of life is not included in the '
                                                           'calculation']},
                                 'unit': 'MJ',
                                 'use': {'max': 1.014, 'min': 0.7157, 'value': 0.79}}}
