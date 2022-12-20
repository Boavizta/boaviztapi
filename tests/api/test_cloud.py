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

    assert res.json() == {
        'gwp': {
            'manufacture': 500.0,
            'use': 230.0,
            'unit': 'kgCO2eq'
        },
        'pe': {
            'manufacture': 7000.0,
            'use': 7791.0,
            'unit': 'MJ'
        },
        'adp': {
            'manufacture': 0.1,
            'use': 3.89e-05,
            'unit': 'kgSbeq'
        }}

@pytest.mark.asyncio
async def test_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=a1.2xlarge&provider=aws')

    assert res.json() == {'adp': {'manufacture': 0.05, 'unit': 'kgSbeq', 'use': 1.94e-05},
                         'gwp': {'manufacture': 250.0, 'unit': 'kgCO2eq', 'use': 110.0},
                         'pe': {'manufacture': 3500.0, 'unit': 'MJ', 'use': 3895.0}}

@pytest.mark.asyncio
async def test_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/cloud/?verbose=false&instance_type=r5ad.12xlarge&provider=aws')
    assert res.json() == {'adp': {'manufacture': 0.12, 'unit': 'kgSbeq', 'use': 0.000193},
                          'gwp': {'manufacture': 1700.0, 'unit': 'kgCO2eq', 'use': 1100.0},
                          'pe': {'manufacture': 21000.0, 'unit': 'MJ', 'use': 38800.0}}

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

    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 0.000149},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 880.0},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 29970.0}}

@pytest.mark.asyncio
async def test_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false', json={
        "provider": "aws",
        "instance_type": "c5a.24xlarge",
        "usage": {
            "time_workload": 100
        }})
    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 0.000255},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 1500.0},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 51050.0}}


@pytest.mark.asyncio
async def test_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/?verbose=false&allocation=TOTAL', json={
        "provider": "aws",
        "instance_type": "c5a.24xlarge",
        "usage": {
            "hours_use_time": 1
        }})
    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 2e-08},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 0.1},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 5.0}}

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
    assert res.json() == {
    "gwp": {
        "manufacture": 500.0,
        "use": 0.007,
        "unit": "kgCO2eq"
    },
    "pe": {
        "manufacture": 7000.0,
        "use": 0.8,
        "unit": "MJ"
    },
    "adp": {
        "manufacture": 0.1,
        "use": 3e-09,
        "unit": "kgSbeq"
    }}


@pytest.mark.asyncio
async def test_legacy_empty_usage_1():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=a1.2xlarge', json={})

    assert res.json() == {'adp': {'manufacture': 0.05, 'unit': 'kgSbeq', 'use': 1.94e-05},
                         'gwp': {'manufacture': 250.0, 'unit': 'kgCO2eq', 'use': 110.0},
                         'pe': {'manufacture': 3500.0, 'unit': 'MJ', 'use': 3895.0}}

@pytest.mark.asyncio
async def test_legacy_empty_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=r5ad.12xlarge', json={})
    assert res.json() == {'adp': {'manufacture': 0.12, 'unit': 'kgSbeq', 'use': 0.000193},
                          'gwp': {'manufacture': 1700.0, 'unit': 'kgCO2eq', 'use': 1100.0},
                          'pe': {'manufacture': 21000.0, 'unit': 'MJ', 'use': 38800.0}}

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

    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 0.000149},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 880.0},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 29970.0}}

@pytest.mark.asyncio
async def test_legacy_usage_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=c5a.24xlarge', json={
            "time_workload": 100
        })
    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 0.000255},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 1500.0},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 51050.0}}


@pytest.mark.asyncio
async def test_legacy_usage_3():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/cloud/aws?verbose=false&instance_type=c5a.24xlarge', json={
            "hours_use_time": 1
        })
    assert res.json() == {'adp': {'manufacture': 0.13, 'unit': 'kgSbeq', 'use': 2e-08},
                          'gwp': {'manufacture': 1100.0, 'unit': 'kgCO2eq', 'use': 0.1},
                          'pe': {'manufacture': 15000.0, 'unit': 'MJ', 'use': 5.0}}

