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
                                  'embedded': {'max': 0.1,
                                            'min': 0.07,
                                            'significant_figures': 1,
                                            'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000205,
                                          'min': 7.21e-06,
                                          'significant_figures': 3,
                                          'value': 3.89e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 500.0,
                                            'min': 300.0,
                                            'significant_figures': 1,
                                            'value': 400.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 700.0,
                                          'min': 13.0,
                                          'significant_figures': 2,
                                          'value': 230.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8000.0,
                                           'min': 5000.0,
                                           'significant_figures': 1,
                                           'value': 6000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 362100.0,
                                         'min': 7.098,
                                         'significant_figures': 4,
                                         'value': 7791.0}}}


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.1,
                                            'min': 0.07,
                                            'significant_figures': 1,
                                            'value': 0.05},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000193,
                                          'min': 7.21e-06,
                                          'significant_figures': 3,
                                          'value': 1.94e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 500.0,
                                            'min': 300.0,
                                            'significant_figures': 1,
                                            'value': 200.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 660.0,
                                          'min': 13.0,
                                          'significant_figures': 2,
                                          'value': 110.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8000.0,
                                           'min': 5000.0,
                                           'significant_figures': 1,
                                           'value': 3000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 340800.0,
                                         'min': 7.098,
                                         'significant_figures': 4,
                                         'value': 3895.0}}}


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'embedded': {'max': 0.22,
                                            'min': 0.2,
                                            'significant_figures': 2,
                                            'value': 0.099},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00179,
                                          'min': 7.18e-05,
                                          'significant_figures': 3,
                                          'value': 0.000193}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 1400.0,
                                            'min': 3200.0,
                                            'significant_figures': 2,
                                            'value': 990.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 6100.0,
                                          'min': 130.0,
                                          'significant_figures': 2,
                                          'value': 1100.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 19000.0,
                                           'min': 40000.0,
                                           'significant_figures': 2,
                                           'value': 13000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 3155000.0,
                                         'min': 70.7,
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
                                  'embedded': {'max': 0.16,
                                            'min': 0.1,
                                            'significant_figures': 2,
                                            'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.000679,
                                          'min': 2.77e-05,
                                          'significant_figures': 3,
                                          'value': 0.000149}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 730.0,
                                            'min': 970.0,
                                            'significant_figures': 2,
                                            'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 2300.0,
                                          'min': 48.0,
                                          'significant_figures': 2,
                                          'value': 880.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 10000.0,
                                           'min': 12000.0,
                                           'significant_figures': 2,
                                           'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 1196000.0,
                                         'min': 27.3,
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
                                  'embedded': {'max': 0.16,
                                            'min': 0.1,
                                            'significant_figures': 2,
                                            'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00116,
                                          'min': 4.72e-05,
                                          'significant_figures': 3,
                                          'value': 0.000255}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 730.0,
                                            'min': 970.0,
                                            'significant_figures': 2,
                                            'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 3900.0,
                                          'min': 82.0,
                                          'significant_figures': 2,
                                          'value': 1500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 10000.0,
                                           'min': 12000.0,
                                           'significant_figures': 2,
                                           'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 2038000.0,
                                         'min': 46.51,
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
                                  'embedded': {'max': 0.16,
                                            'min': 0.1,
                                            'significant_figures': 2,
                                            'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 1e-07,
                                          'min': 4e-09,
                                          'significant_figures': 1,
                                          'value': 2e-08}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 730.0,
                                            'min': 970.0,
                                            'significant_figures': 2,
                                            'value': 790.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.3,
                                          'min': 0.007,
                                          'significant_figures': 1,
                                          'value': 0.1}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 10000.0,
                                           'min': 12000.0,
                                           'significant_figures': 2,
                                           'value': 11000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 200.0,
                                         'min': 0.004,
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
                                  'embedded': {'max': 0.1,
                                            'min': 0.07,
                                            'significant_figures': 1,
                                            'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 4e-09,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 3e-09}},
                          'gwp': {'description': 'Effects on global warming',
                                  'embedded': {'max': 500.0,
                                            'min': 300.0,
                                            'significant_figures': 1,
                                            'value': 400.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.009,
                                          'min': 0.006,
                                          'significant_figures': 1,
                                          'value': 0.007}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'embedded': {'max': 8000.0,
                                           'min': 5000.0,
                                           'significant_figures': 1,
                                           'value': 6000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 1.0,
                                         'min': 0.7,
                                         'significant_figures': 1,
                                         'value': 0.8}}}