import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={"core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                          'gwp': {'manufacture': 15.9, 'unit': 'kgCO2eq', 'use': 610.0},
                          'pe': {'manufacture': 247.0, 'unit': 'MJ', 'use': 20550.0}}


@pytest.mark.asyncio
async def test_complete_cpu_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=true', json={"core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {'impacts': {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                                      'gwp': {'manufacture': 15.9, 'unit': 'kgCO2eq', 'use': 610.0},
                                      'pe': {'manufacture': 247.0, 'unit': 'MJ', 'use': 20550.0}},
                          'verbose': {'USAGE': {'adp_factor': {'source': {'1': 'ADEME BASE IMPACT'},
                                                               'status': 'COMPLETED',
                                                               'unit': 'KgSbeq/kWh',
                                                               'value': 6.42e-08},
                                                'gwp_factor': {'source': {
                                                    '1': 'https://www.sciencedirect.com/science/article/pii'
                                                         '/S0306261921012149 '
                                                         ': \n'
                                                         'Average of 27 european '
                                                         'countries'},
                                                    'status': 'COMPLETED',
                                                    'unit': 'kgCO2e/kWh',
                                                    'value': 0.38},
                                                'hours_electrical_consumption': {'source': None,
                                                                                 'status': 'COMPLETED',
                                                                                 'unit': 'W',
                                                                                 'value': 182.23023303189055},
                                                'params': {'source': None,
                                                           'status': 'DEFAULT',
                                                           'unit': 'none',
                                                           'value': {'a': 171.2,
                                                                     'b': 0.0354,
                                                                     'c': 36.89,
                                                                     'd': -10.13}},
                                                'pe_factor': {'source': {'1': 'ADPf / '
                                                                              '(1-%renewable_energy)'},
                                                              'status': 'COMPLETED',
                                                              'unit': 'MJ/kWh',
                                                              'value': 12.874},
                                                'time_workload': {'source': None,
                                                                  'status': 'DEFAULT',
                                                                  'unit': '%',
                                                                  'value': 50.0},
                                                'usage_impacts': {'adp': {'unit': 'kgSbeq',
                                                                          'value': 0.000102},
                                                                  'gwp': {'unit': 'kgCO2eq',
                                                                          'value': 610.0},
                                                                  'pe': {'unit': 'MJ',
                                                                         'value': 20550.0}},
                                                'usage_location': {'source': None,
                                                                   'status': 'DEFAULT',
                                                                   'unit': 'CodSP3 - NCS Country Codes '
                                                                           '- NATO',
                                                                   'value': 'EEE'},
                                                'use_time': {'source': None,
                                                             'status': 'DEFAULT',
                                                             'unit': 'hours',
                                                             'value': 8760}},
                                      'core_units': {'source': None,
                                                     'status': 'INPUT',
                                                     'unit': 'none',
                                                     'value': 12},
                                      'die_size_per_core': {'source': None,
                                                            'status': 'INPUT',
                                                            'unit': 'mm2',
                                                            'value': 0.245},
                                      'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                                              'gwp': {'unit': 'kgCO2eq', 'value': 15.9},
                                                              'pe': {'unit': 'MJ', 'value': 247.0}},
                                      'units': 1}}


@pytest.mark.asyncio
async def test_complete_cpu_with_low_precision():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={"core_units": 12, "die_size_per_core": 0.2})

    assert res.json() == {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                          'gwp': {'manufacture': 10.0, 'unit': 'kgCO2eq', 'use': 610.0},
                          'pe': {'manufacture': 200.0, 'unit': 'MJ', 'use': 20550.0}}


@pytest.mark.asyncio
async def test_empty_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={})

    assert res.json() == {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                          'gwp': {'manufacture': 21.7, 'unit': 'kgCO2eq', 'use': 610.0},
                          'pe': {'manufacture': 325.0, 'unit': 'MJ', 'use': 20550.0}}


@pytest.mark.asyncio
async def test_multiple_cpu():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=false', json={
            "units": 3, "core_units": 12, "die_size_per_core": 0.245})

    assert res.json() == {'adp': {'manufacture': 0.061, 'unit': 'kgSbeq', 'use': 0.000307},
                          'gwp': {'manufacture': 47.7, 'unit': 'kgCO2eq', 'use': 1800.0},
                          'pe': {'manufacture': 741.0, 'unit': 'MJ', 'use': 61650.0}}


@pytest.mark.asyncio
async def test_incomplete_cpu_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=true', json={
            "core_units": 24, "family": "Skylake", "manufacture_date": 2017})

    assert res.json() == {'impacts': {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                                      'gwp': {'manufacture': 23.8, 'unit': 'kgCO2eq', 'use': 610.0},
                                      'pe': {'manufacture': 353.0, 'unit': 'MJ', 'use': 20550.0}},
                          'verbose': {'USAGE': {'adp_factor': {'source': {'1': 'ADEME BASE IMPACT'},
                                                               'status': 'COMPLETED',
                                                               'unit': 'KgSbeq/kWh',
                                                               'value': 6.42e-08},
                                                'gwp_factor': {'source': {
                                                    '1': 'https://www.sciencedirect.com/science/article/pii'
                                                         '/S0306261921012149 '
                                                         ': \n'
                                                         'Average of 27 european '
                                                         'countries'},
                                                    'status': 'COMPLETED',
                                                    'unit': 'kgCO2e/kWh',
                                                    'value': 0.38},
                                                'hours_electrical_consumption': {'source': None,
                                                                                 'status': 'COMPLETED',
                                                                                 'unit': 'W',
                                                                                 'value': 182.23023303189055},
                                                'params': {'source': None,
                                                           'status': 'DEFAULT',
                                                           'unit': 'none',
                                                           'value': {'a': 171.2,
                                                                     'b': 0.0354,
                                                                     'c': 36.89,
                                                                     'd': -10.13}},
                                                'pe_factor': {'source': {'1': 'ADPf / '
                                                                              '(1-%renewable_energy)'},
                                                              'status': 'COMPLETED',
                                                              'unit': 'MJ/kWh',
                                                              'value': 12.874},
                                                'time_workload': {'source': None,
                                                                  'status': 'DEFAULT',
                                                                  'unit': '%',
                                                                  'value': 50.0},
                                                'usage_impacts': {'adp': {'unit': 'kgSbeq',
                                                                          'value': 0.000102},
                                                                  'gwp': {'unit': 'kgCO2eq',
                                                                          'value': 610.0},
                                                                  'pe': {'unit': 'MJ',
                                                                         'value': 20550.0}},
                                                'usage_location': {'source': None,
                                                                   'status': 'DEFAULT',
                                                                   'unit': 'CodSP3 - NCS Country Codes '
                                                                           '- NATO',
                                                                   'value': 'EEE'},
                                                'use_time': {'source': None,
                                                             'status': 'DEFAULT',
                                                             'unit': 'hours',
                                                             'value': 8760}},
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
                                                 'status': 'CHANGED',
                                                 'unit': 'none',
                                                 'value': 'skylake'},
                                      'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                                              'gwp': {'unit': 'kgCO2eq', 'value': 23.8},
                                                              'pe': {'unit': 'MJ', 'value': 353.0}},
                                      'units': 1}}


@pytest.mark.asyncio
async def test_incomplete_cpu_verbose_2():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/cpu?verbose=true', json={
            "core_units": 24, "family": "skylak", "manufacture_date": 2017})

    assert res.json() == {'impacts': {'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
                                      'gwp': {'manufacture': 23.8, 'unit': 'kgCO2eq', 'use': 610.0},
                                      'pe': {'manufacture': 353.0, 'unit': 'MJ', 'use': 20550.0}},
                          'verbose': {'USAGE': {'adp_factor': {'source': {'1': 'ADEME BASE IMPACT'},
                                                               'status': 'COMPLETED',
                                                               'unit': 'KgSbeq/kWh',
                                                               'value': 6.42e-08},
                                                'gwp_factor': {'source': {
                                                    '1': 'https://www.sciencedirect.com/science/article/pii'
                                                         '/S0306261921012149 '
                                                         ': \n'
                                                         'Average of 27 european '
                                                         'countries'},
                                                    'status': 'COMPLETED',
                                                    'unit': 'kgCO2e/kWh',
                                                    'value': 0.38},
                                                'hours_electrical_consumption': {'source': None,
                                                                                 'status': 'COMPLETED',
                                                                                 'unit': 'W',
                                                                                 'value': 182.23023303189055},
                                                'params': {'source': None,
                                                           'status': 'DEFAULT',
                                                           'unit': 'none',
                                                           'value': {'a': 171.2,
                                                                     'b': 0.0354,
                                                                     'c': 36.89,
                                                                     'd': -10.13}},
                                                'pe_factor': {'source': {'1': 'ADPf / '
                                                                              '(1-%renewable_energy)'},
                                                              'status': 'COMPLETED',
                                                              'unit': 'MJ/kWh',
                                                              'value': 12.874},
                                                'time_workload': {'source': None,
                                                                  'status': 'DEFAULT',
                                                                  'unit': '%',
                                                                  'value': 50.0},
                                                'usage_impacts': {'adp': {'unit': 'kgSbeq',
                                                                          'value': 0.000102},
                                                                  'gwp': {'unit': 'kgCO2eq',
                                                                          'value': 610.0},
                                                                  'pe': {'unit': 'MJ',
                                                                         'value': 20550.0}},
                                                'usage_location': {'source': None,
                                                                   'status': 'DEFAULT',
                                                                   'unit': 'CodSP3 - NCS Country Codes '
                                                                           '- NATO',
                                                                   'value': 'EEE'},
                                                'use_time': {'source': None,
                                                             'status': 'DEFAULT',
                                                             'unit': 'hours',
                                                             'value': 8760}},
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
                                                 'status': 'CHANGED',
                                                 'unit': 'none',
                                                 'value': 'skylake'},
                                      'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                                              'gwp': {'unit': 'kgCO2eq', 'value': 23.8},
                                                              'pe': {'unit': 'MJ', 'value': 353.0}},
                                      'units': 1}}


@pytest.mark.asyncio
async def test_complete_ram():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ram?verbose=false', json={"units": 12, "capacity": 32, "density": 1.79})

    assert res.json() == {'adp': {'manufacture': 0.034, 'unit': 'kgSbeq', 'use': 6.13e-05},
                          'gwp': {'manufacture': 530.0, 'unit': 'kgCO2eq', 'use': 360.0},
                          'pe': {'manufacture': 6700.0, 'unit': 'MJ', 'use': 12300.0}}


@pytest.mark.asyncio
async def test_empty_ram():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/component/ram?verbose=false', json={})

    assert res.json() == {'adp': {'manufacture': 0.0049, 'unit': 'kgSbeq', 'use': 5.11e-06},
                          'gwp': {'manufacture': 120.0, 'unit': 'kgCO2eq', 'use': 30.0},
                          'pe': {'manufacture': 1500.0, 'unit': 'MJ', 'use': 1025.0}}


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
