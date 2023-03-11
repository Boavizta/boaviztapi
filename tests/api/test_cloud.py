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
                                                  'min': 0.08,
                                                  'significant_figures': 1,
                                                  'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00242,
                                          'min': 6.86e-10,
                                          'significant_figures': 3,
                                          'value': 3.89e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 600.0,
                                                  'min': 1000.0,
                                                  'significant_figures': 1,
                                                  'value': 500.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 8200.0,
                                          'min': 0.0012,
                                          'significant_figures': 2,
                                          'value': 230.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 10000.0,
                                                 'significant_figures': 1,
                                                 'value': 7000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 4260000.0,
                                         'min': 0.0006752,
                                         'significant_figures': 4,
                                         'value': 7791.0}}}


@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.1,
                                                  'min': 0.08,
                                                  'significant_figures': 1,
                                                  'value': 0.05},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00242,
                                          'min': 6.86e-10,
                                          'significant_figures': 3,
                                          'value': 1.94e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 600.0,
                                                  'min': 1000.0,
                                                  'significant_figures': 1,
                                                  'value': 300.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 8200.0,
                                          'min': 0.0012,
                                          'significant_figures': 2,
                                          'value': 110.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 10000.0,
                                                 'significant_figures': 1,
                                                 'value': 3000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 4260000.0,
                                         'min': 0.0006752,
                                         'significant_figures': 4,
                                         'value': 3895.0}}}


@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.35,
                                                  'min': 1.7,
                                                  'significant_figures': 2,
                                                  'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0241,
                                          'min': 6.83e-09,
                                          'significant_figures': 3,
                                          'value': 0.000193}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 6300.0,
                                                  'min': 57000.0,
                                                  'significant_figures': 2,
                                                  'value': 1700.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 82000.0,
                                          'min': 0.012,
                                          'significant_figures': 2,
                                          'value': 1100.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 79000.0,
                                                 'min': 710000.0,
                                                 'significant_figures': 2,
                                                 'value': 21000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 42440000.0,
                                         'min': 0.006726,
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
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0093,
                                          'min': 2.64e-09,
                                          'significant_figures': 3,
                                          'value': 0.000149}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 32000.0,
                                          'min': 0.0046,
                                          'significant_figures': 2,
                                          'value': 880.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 16390000.0,
                                         'min': 0.002597,
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
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0158,
                                          'min': 4.49e-09,
                                          'significant_figures': 3,
                                          'value': 0.000255}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 54000.0,
                                          'min': 0.0078,
                                          'significant_figures': 2,
                                          'value': 1500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 27920000.0,
                                         'min': 0.004425,
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
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 1e-07,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 2e-08}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.5,
                                          'min': 0.006,
                                          'significant_figures': 1,
                                          'value': 0.1}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 200.0,
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
                                                  'min': 0.08,
                                                  'significant_figures': 1,
                                                  'value': 0.1},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 5e-09,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 3e-09}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 600.0,
                                                  'min': 1000.0,
                                                  'significant_figures': 1,
                                                  'value': 500.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.01,
                                          'min': 0.005,
                                          'significant_figures': 1,
                                          'value': 0.007}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 10000.0,
                                                 'significant_figures': 1,
                                                 'value': 7000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 1.0,
                                         'min': 0.6,
                                         'significant_figures': 1,
                                         'value': 0.8}}}


@pytest.mark.asyncio
async def test_legacy_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=a1.2xlarge', json={})

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.1,
                                                  'min': 0.08,
                                                  'significant_figures': 1,
                                                  'value': 0.05},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.00242,
                                          'min': 6.86e-10,
                                          'significant_figures': 3,
                                          'value': 1.94e-05}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 600.0,
                                                  'min': 1000.0,
                                                  'significant_figures': 1,
                                                  'value': 300.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 8200.0,
                                          'min': 0.0012,
                                          'significant_figures': 2,
                                          'value': 110.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 8000.0,
                                                 'min': 10000.0,
                                                 'significant_figures': 1,
                                                 'value': 3000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 4260000.0,
                                         'min': 0.0006752,
                                         'significant_figures': 4,
                                         'value': 3895.0}}}


@pytest.mark.asyncio
async def test_legacy_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=r5ad.12xlarge', json={})
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.35,
                                                  'min': 1.7,
                                                  'significant_figures': 2,
                                                  'value': 0.12},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0241,
                                          'min': 6.83e-09,
                                          'significant_figures': 3,
                                          'value': 0.000193}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 6300.0,
                                                  'min': 57000.0,
                                                  'significant_figures': 2,
                                                  'value': 1700.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 82000.0,
                                          'min': 0.012,
                                          'significant_figures': 2,
                                          'value': 1100.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 79000.0,
                                                 'min': 710000.0,
                                                 'significant_figures': 2,
                                                 'value': 21000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 42440000.0,
                                         'min': 0.006726,
                                         'significant_figures': 4,
                                         'value': 38800.0}}}


@pytest.mark.asyncio
async def test_legacy_wrong_input():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=test', json={})
    assert res.json() == {'detail': 'test not found'}


@pytest.mark.asyncio
async def test_legacy_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=c5a.24xlarge', json={
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
        })

    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0093,
                                          'min': 2.64e-09,
                                          'significant_figures': 3,
                                          'value': 0.000149}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 32000.0,
                                          'min': 0.0046,
                                          'significant_figures': 2,
                                          'value': 880.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 16390000.0,
                                         'min': 0.002597,
                                         'significant_figures': 4,
                                         'value': 29970.0}}}


@pytest.mark.asyncio
async def test_legacy_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=c5a.24xlarge', json={
            "time_workload": 100
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 0.0158,
                                          'min': 4.49e-09,
                                          'significant_figures': 3,
                                          'value': 0.000255}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 54000.0,
                                          'min': 0.0078,
                                          'significant_figures': 2,
                                          'value': 1500.0}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 27920000.0,
                                         'min': 0.004425,
                                         'significant_figures': 4,
                                         'value': 51050.0}}}


@pytest.mark.asyncio
async def test_legacy_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=c5a.24xlarge', json={
            "hours_use_time": 1
        })
    assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                  'manufacture': {'max': 0.16,
                                                  'min': 0.2,
                                                  'significant_figures': 2,
                                                  'value': 0.13},
                                  'unit': 'kgSbeq',
                                  'use': {'max': 1e-07,
                                          'min': 3e-09,
                                          'significant_figures': 1,
                                          'value': 2e-08}},
                          'gwp': {'description': 'Effects on global warming',
                                  'manufacture': {'max': 970.0,
                                                  'min': 4600.0,
                                                  'significant_figures': 2,
                                                  'value': 1100.0},
                                  'unit': 'kgCO2eq',
                                  'use': {'max': 0.5,
                                          'min': 0.006,
                                          'significant_figures': 1,
                                          'value': 0.1}},
                          'pe': {'description': 'Consumption of primary energy',
                                 'manufacture': {'max': 13000.0,
                                                 'min': 58000.0,
                                                 'significant_figures': 2,
                                                 'value': 15000.0},
                                 'unit': 'MJ',
                                 'use': {'max': 200.0,
                                         'min': 0.003,
                                         'significant_figures': 1,
                                         'value': 5.0}}}
