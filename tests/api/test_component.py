import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={"core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {
        "gwp": {
            "manufacture": 15.9,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 247,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.020,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_complete_cpu_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=true', json={"core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {'impacts': {'adp': {'manufacture': 0.02,
                                              'unit': 'kgSbeq',
                                              'use': 'not implemented'},
                                      'gwp': {'manufacture': 15.9,
                                              'unit': 'kgCO2eq',
                                              'use': 'not implemented'},
                                      'pe': {'manufacture': 247.0,
                                             'unit': 'MJ',
                                             'use': 'not implemented'}},
                          'verbose': {'USAGE': {'impacts': {'adp': {'unit': 'kgSbeq',
                                                                    'value': 'not implemented'},
                                                            'gwp': {'unit': 'kgCO2eq',
                                                                    'value': 'not implemented'},
                                                            'pe': {'unit': 'MJ',
                                                                   'value': 'not implemented'}}},
                                      'core_units': {'source': None,
                                                     'status': 'INPUT',
                                                     'unit': 'none',
                                                     'value': 12},
                                      'die_size_per_core': {'source': None,
                                                            'status': 'INPUT',
                                                            'unit': 'mm2',
                                                            'value': 0.245},
                                      'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                                  'gwp': {'unit': 'kgCO2eq', 'value': 15.9},
                                                  'pe': {'unit': 'MJ', 'value': 247.0}},
                                      'units': 1}}


@pytest.mark.asyncio
async def test_complete_cpu_with_low_precision():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={"core_units": 12, "die_size_per_core": 0.2})

    assert res.json() == {
        "gwp": {
            "manufacture": 10.0,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 200.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.02,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_empty_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={})

    assert res.json() == {
        "gwp": {
            "manufacture": 21.7,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 325.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.020,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_multiple_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={
            "units": 3, "core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {
        "gwp": {
            "manufacture": 47.7,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 741.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.061,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_incomplete_cpu_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=true', json={
            "core_units": 24, "family": "Skylake", "manufacture_date": 2017})

    assert res.json() == {'impacts': {'adp': {'manufacture': 0.02,
                                              'unit': 'kgSbeq',
                                              'use': 'not implemented'},
                                      'gwp': {'manufacture': 23.8,
                                              'unit': 'kgCO2eq',
                                              'use': 'not implemented'},
                                      'pe': {'manufacture': 353.0,
                                             'unit': 'MJ',
                                             'use': 'not implemented'}},
                          'verbose': {'USAGE': {'impacts': {'adp': {'unit': 'kgSbeq',
                                                                    'value': 'not implemented'},
                                                            'gwp': {'unit': 'kgCO2eq',
                                                                    'value': 'not implemented'},
                                                            'pe': {'unit': 'MJ',
                                                                   'value': 'not implemented'}}},
                                      'core_units': {'source': None,
                                                     'status': 'INPUT',
                                                     'unit': 'none',
                                                     'value': 24},
                                      'die_size_per_core': {'source': {
                                          '1': 'https://en.wikichip.org/wiki/intel/microarchitectures/skylake_(server)'},
                                                            'status': 'COMPLETED',
                                                            'unit': 'mm2',
                                                            'value': 0.289},
                                      'family': {'source': None,
                                                 'status': 'INPUT',
                                                 'unit': 'none',
                                                 'value': 'Skylake'},
                                      'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                                  'gwp': {'unit': 'kgCO2eq', 'value': 23.8},
                                                  'pe': {'unit': 'MJ', 'value': 353.0}},
                                      'units': 1}}


@pytest.mark.asyncio
async def test_complete_ram():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ram?verbose=false', json={"units": 12, "capacity": 32, "density": 1.79})

    assert res.json() == {
        "gwp": {
            "manufacture": 530.0,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 6700.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.034,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_empty_ram():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ram?verbose=false', json={})

    assert res.json() == {
        "gwp": {
            "manufacture": 120.0,
            "use": "not implemented",
            "unit": "kgCO2eq"

        },
        "pe": {
            "manufacture": 1500.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.0049,
            "use": "not implemented",
            "unit": "kgSbeq"
        }
    }


@pytest.mark.asyncio
async def test_complete_ssd():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ssd?verbose=false', json={"capacity": 400, "density": 50.6})

    assert res.json() == {
        "gwp": {
            "manufacture": 24.0,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 293.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.0011,
            "use": "not implemented",
            "unit": "kgSbeq"
        },
    }


@pytest.mark.asyncio
async def test_empty_ssd():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ssd?verbose=false', json={})

    assert res.json() == {
        "gwp": {
            "manufacture": 52.0,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 640.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.0019,
            "use": "not implemented",
            "unit": "kgSbeq"
        },
    }


@pytest.mark.asyncio
async def test_empty_blade():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/case?verbose=false', json={"case_type": "blade"})

    assert res.json() == {
        "gwp": {
            "manufacture": 85.9,
            "use": "not implemented",
            "unit": "kgCO2eq"
        },
        "pe": {
            "manufacture": 1230.0,
            "use": "not implemented",
            "unit": "MJ"
        },
        "adp": {
            "manufacture": 0.0277,
            "use": "not implemented",
            "unit": "kgSbeq"
        },
    }
