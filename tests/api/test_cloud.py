import pytest
from httpx import AsyncClient
from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_empty_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
            'provider': 'aws',
            'instance_type': 'a1.4xlarge',
            'usage': {}
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.1,
                                                  'min': 0.06,
                                                  'significant_figures': 1,
                                                  'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000187,
                                          'min': 6.58e-06,
                                          'significant_figures': 3,
                                          'value': 3.89e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 500.0,
                                                  'min': 200.0,
                                                  'significant_figures': 1,
                                                  'value': 400.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 640.0,
                                          'min': 11.0,
                                          'significant_figures': 2,
                                          'value': 230.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 3000.0,
                                                 'significant_figures': 1,
                                                 'value': 6000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 330400.0,
                                         'min': 6.477,
                                         'significant_figures': 4,
                                         'value': 7791.0}}}


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() =={'adp': {'description': 'Use of minerals and fossil ressources',
                                 'manufacture': {'max': 0.1,
                                                 'min': 0.06,
                                                 'significant_figures': 1,
                                                 'value': 0.05},
                                 'unit': 'kgSbeq',
                                 'use': {'max': 0.000176,
                                         'min': 6.58e-06,
                                         'significant_figures': 3,
                                         'value': 1.94e-05}},
                         'gwp': {'description': 'Effects on global warming',
                                 'manufacture': {'max': 500.0,
                                                 'min': 200.0,
                                                 'significant_figures': 1,
                                                 'value': 200.0},
                                 'unit': 'kgCO2eq',
                                 'use': {'max': 600.0,
                                         'min': 11.0,
                                         'significant_figures': 2,
                                         'value': 110.0}},
                         'pe': {'description': 'Consumption of primary energy',
                                'manufacture': {'max': 8000.0,
                                                'min': 3000.0,
                                                'significant_figures': 1,
                                                'value': 3000.0},
                                'unit': 'MJ',
                                'use': {'max': 311000.0,
                                        'min': 6.477,
                                        'significant_figures': 4,
                                        'value': 3895.0}}}


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.11,
                                                  'min': 0.068,
                                                  'significant_figures': 2,
                                                  'value': 0.099},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000549,
                                          'min': 2.2e-05,
                                          'significant_figures': 3,
                                          'value': 0.000193}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 560.0,
                                                  'min': 340.0,
                                                  'significant_figures': 2,
                                                  'value': 990.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 1900.0,
                                          'min': 38.0,
                                          'significant_figures': 2,
                                          'value': 1100.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 7900.0,
                                                 'min': 4400.0,
                                                 'significant_figures': 2,
                                                 'value': 13000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 968000.0,
                                         'min': 21.69,
                                         'significant_figures': 4,
                                         'value': 38800.0}}}

@pytest.mark.asyncio
async def test_wrong_input():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
            "provider": "test",
            "instance_type": "a1.4xlarge",
            "usage": {}
        })
    assert res.json() == {'detail': 'a1.4xlarge at test not found'}


@pytest.mark.asyncio
async def test_wrong_input_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
            "provider": "aws",
            "instance_type": "test",
            "usage": {}
        })
    assert res.json() == {'detail': 'test at aws not found'}


@pytest.mark.asyncio
async def test_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
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
                                  'manufacture': {'max': 0.11,
                                                  'min': 0.065,
                                                  'significant_figures': 2,
                                                  'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000509,
                                          'min': 2.08e-05,
                                          'significant_figures': 3,
                                          'value': 0.000149}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 520.0,
                                                  'min': 250.0,
                                                  'significant_figures': 2,
                                                  'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 1700.0,
                                          'min': 36.0,
                                          'significant_figures': 2,
                                          'value': 880.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 7300.0,
                                                 'min': 3300.0,
                                                 'significant_figures': 2,
                                                 'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 896900.0,
                                         'min': 20.47,
                                         'significant_figures': 4,
                                         'value': 29970.0}}}


@pytest.mark.asyncio
async def test_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {
                "time_workload": 100
            }})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.11,
                                                  'min': 0.065,
                                                  'significant_figures': 2,
                                                  'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000986,
                                          'min': 4.03e-05,
                                          'significant_figures': 3,
                                          'value': 0.000255}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 520.0,
                                                  'min': 250.0,
                                                  'significant_figures': 2,
                                                  'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 3300.0,
                                          'min': 70.0,
                                          'significant_figures': 2,
                                          'value': 1500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 7300.0,
                                                 'min': 3300.0,
                                                 'significant_figures': 2,
                                                 'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 1739000.0,
                                         'min': 39.68,
                                         'significant_figures': 4,
                                         'value': 51050.0}}}


@pytest.mark.asyncio
async def test_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false&allocation=TOTAL', json={
            "provider": "aws",
            "instance_type": "c5a.24xlarge",
            "usage": {
                "hours_use_time": 1
            }})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.11,
                                                  'min': 0.065,
                                                  'significant_figures': 2,
                                                  'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 8e-08,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 2e-08}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 520.0,
                                                  'min': 250.0,
                                                  'significant_figures': 2,
                                                  'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.3,
                                          'min': 0.006,
                                          'significant_figures': 1,
                                          'value': 0.1}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 7300.0,
                                                 'min': 3300.0,
                                                 'significant_figures': 2,
                                                 'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 100.0,
                                         'min': 0.003,
                                         'significant_figures': 1,
                                         'value': 5.0}}}


@pytest.mark.asyncio
async def test_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
            "provider": "aws",
            "instance_type": "a1.4xlarge",
            "usage": {
                "hours_use_time": "2",
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
                                  'manufacture': {'max': 0.1,
                                                  'min': 0.06,
                                                  'significant_figures': 1,
                                                  'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4e-09,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 3e-09}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 500.0,
                                                  'min': 200.0,
                                                  'significant_figures': 1,
                                                  'value': 400.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.007,
                                          'min': 0.005,
                                          'significant_figures': 1,
                                          'value': 0.007}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 3000.0,
                                                 'significant_figures': 1,
                                                 'value': 6000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 0.8,
                                         'min': 0.6,
                                         'significant_figures': 1,
                                         'value': 0.8}}}