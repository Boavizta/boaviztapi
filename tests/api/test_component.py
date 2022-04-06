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

    assert res.json() == {
        "impacts": {
            "adp": {
                "manufacture": 0.02,
                "unit": "kgSbeq",
                "use": "not implemented"
            },
            "gwp": {
                "manufacture": 15.9,
                "unit": "kgCO2eq",
                "use": "not implemented"
            },
            "pe": {
                "manufacture": 247.0,
                "unit": "MJ",
                "use": "not implemented"
            }
        },
        "verbose": {
            "units": 1,
            "core_units": {
                "input_value": 12,
                "status": "UNCHANGED",
                "used_value": 12
            },
            "die_size_per_core": {
                "input_value": 0.245,
                "status": "UNCHANGED",
                "used_value": 0.245
            },
            "impacts": {
                "adp": {"value": 0.02, "unit": "kgSbeq"},
                "gwp": {"value": 15.9, "unit": "kgCO2eq"},
                "pe": {"value": 247.0, "unit": "MJ"}
            }
        }
    }


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

    assert res.json() == {
        "impacts": {
            "adp": {
                "manufacture": 0.02,
                "unit": "kgSbeq",
                "use": "not implemented"
            },
            "gwp": {
                "manufacture": 21.7,
                "unit": "kgCO2eq",
                "use": "not implemented"
            },
            "pe": {
                "manufacture": 325.0,
                "unit": "MJ",
                "use": "not implemented"
            }
        },
        'verbose': {'core_units': {'input_value': 24,
                                   'status': 'UNCHANGED',
                                   'used_value': 24},
                    'die_size_per_core': {'input_value': None,
                                          'status': 'SET',
                                          'used_value': 0.245},
                    'family': {'input_value': 'Skylake',
                               'status': 'UNCHANGED',
                               'used_value': 'Skylake'},
                    'impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                'gwp': {'unit': 'kgCO2eq', 'value': 21.7},
                                'pe': {'unit': 'MJ', 'value': 325.0}},
                    'manufacture_date': {'input_value': '2017',
                                         'status': 'UNCHANGED',
                                         'used_value': '2017'},
                    'units': 1
                    }
    }

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
