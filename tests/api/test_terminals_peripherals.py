import pytest
from httpx import AsyncClient, ASGITransport

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_laptop():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post('/v1/terminal/laptop?verbose=false&criteria=ir', json={})

    assert res.status_code == 200
    assert res.json() == {'impacts': {'ir': {'description': 'Emissions of radionizing substances',
                                             'embedded': {'max': 73.6,
                                                          'min': 73.6,
                                                          'value': 73.6,
                                                          'warnings': ['Generic data used for impact '
                                                                       'calculation.']},
                                             'unit': 'kg U235 eq.',
                                             'use': {'max': 3446.0, 'min': 0.05643, 'value': 900.0}}}}


@pytest.mark.asyncio
async def test_desktop():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/desktop?verbose=false&criteria=lu')

    assert res.status_code == 200
    assert res.json() == {'impacts': {'lu': {'description': 'Land use',
                                             'embedded': {'max': -101.0,
                                                          'min': -101.0,
                                                          'value': -101.0,
                                                          'warnings': ['Generic data used for impact '
                                                                       'calculation.']},
                                             'unit': 'No dimension',
                                             'use': 'not implemented'}}}


@pytest.mark.asyncio
async def test_smartphone():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/smartphone?verbose=true')

    assert res.status_code == 200
    assert res.json() == {'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                              'embedded': 'not implemented',
                                              'unit': 'kgSbeq',
                                              'use': {'max': 5.235e-06,
                                                      'min': 4.336e-08,
                                                      'value': 4e-07}},
                                      'gwp': {'description': 'Total climate change',
                                              'embedded': {'max': 84.0,
                                                           'min': 84.0,
                                                           'value': 84.0,
                                                           'warnings': ['Generic data used for impact '
                                                                        'calculation.']},
                                              'unit': 'kgCO2eq',
                                              'use': {'max': 17.74, 'min': 0.07555, 'value': 2.0}},
                                      'pe': {'description': 'Consumption of primary energy',
                                             'embedded': 'not implemented',
                                             'unit': 'MJ',
                                             'use': {'max': 9227.0, 'min': 0.0427, 'value': 100.0}}},
                          'verbose': {'adp_factor': {'max': 2.656e-07,
                                                     'min': 1.32e-08,
                                                     'source': 'ADEME Base IMPACTS ®',
                                                     'status': 'DEFAULT',
                                                     'unit': 'kg Sbeq/kWh',
                                                     'value': 6.42e-08},
                                      'avg_power': {'max': 3.0,
                                                    'min': 0.5,
                                                    'status': 'ARCHETYPE',
                                                    'unit': 'W',
                                                    'value': 1.0},
                                      'duration': {'unit': 'hours', 'value': 21900.0},
                                      'gwp_factor': {'max': 0.9,
                                                     'min': 0.023,
                                                     'source': 'https://www.sciencedirect.com/science/article/pii/S0306261921012149: \n'
                                                               'Average of 27 european countries',
                                                     'status': 'DEFAULT',
                                                     'unit': 'kg CO2eq/kWh',
                                                     'value': 0.38},
                                      'hours_life_time': {'status': 'ARCHETYPE',
                                                          'unit': 'hours',
                                                          'value': 21900.0},
                                      'pe_factor': {'max': 468.15,
                                                    'min': 0.013,
                                                    'source': 'ADPf / (1-%renewable_energy)',
                                                    'status': 'DEFAULT',
                                                    'unit': 'MJ/kWh',
                                                    'value': 12.874},
                                      'units': {'max': 1, 'min': 1, 'status': 'ARCHETYPE', 'value': 1},
                                      'usage_location': {'status': 'DEFAULT',
                                                         'unit': 'CodSP3 - NCS Country Codes - NATO',
                                                         'value': 'EEE'},
                                      'use_time_ratio': {'max': 0.3,
                                                         'min': 0.3,
                                                         'status': 'ARCHETYPE',
                                                         'unit': '/1',
                                                         'value': 0.3}}}


@pytest.mark.asyncio
async def test_box():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/box?verbose=true&criteria=adpe')

    assert res.status_code == 200
    assert res.json() == {'impacts': {'adpe': {'description': 'Use of mineral and metal resources',
                                               'embedded': {'max': 4.41e-05,
                                                            'min': 4.41e-05,
                                                            'value': 4.41e-05,
                                                            'warnings': ['Generic data used for impact '
                                                                         'calculation.']},
                                               'unit': 'kg SB eq.',
                                               'use': {'max': 0.0002327,
                                                       'min': 2.891e-06,
                                                       'value': 3e-05}}},
                          'verbose': {'adpe_factor': {'max': 2.656e-07,
                                                      'min': 1.32e-08,
                                                      'source': 'ADEME Base IMPACTS ®',
                                                      'status': 'DEFAULT',
                                                      'unit': 'kg Sbeq/kWh',
                                                      'value': 6.42e-08},
                                      'avg_power': {'max': 20.0,
                                                    'min': 5.0,
                                                    'status': 'ARCHETYPE',
                                                    'unit': 'W',
                                                    'value': 10.0},
                                      'duration': {'unit': 'hours', 'value': 43800.0},
                                      'hours_life_time': {'status': 'ARCHETYPE',
                                                          'unit': 'hours',
                                                          'value': 43800.0},
                                      'units': {'max': 1, 'min': 1, 'status': 'ARCHETYPE', 'value': 1},
                                      'usage_location': {'status': 'DEFAULT',
                                                         'unit': 'CodSP3 - NCS Country Codes - NATO',
                                                         'value': 'EEE'},
                                      'use_time_ratio': {'max': 1.0,
                                                         'min': 1.0,
                                                         'status': 'ARCHETYPE',
                                                         'unit': '/1',
                                                         'value': 1.0}}}


@pytest.mark.asyncio
async def test_tv_archetype_perso():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/terminal/television?verbose=true&criteria=adpe&archetype=tv-perso')

    assert res.status_code == 200
    assert res.json() == {'impacts': {'adpe': {'description': 'Use of mineral and metal resources',
                                               'embedded': {'max': 0.0383,
                                                            'min': 0.0383,
                                                            'value': 0.0383,
                                                            'warnings': ['Generic data used for impact '
                                                                         'calculation.']},
                                               'unit': 'kg SB eq.',
                                               'use': {'max': 0.006701,
                                                       'min': 1.665e-05,
                                                       'value': 0.0004}}},
                          'verbose': {'adpe_factor': {'max': 2.656e-07,
                                                      'min': 1.32e-08,
                                                      'source': 'ADEME Base IMPACTS ®',
                                                      'status': 'DEFAULT',
                                                      'unit': 'kg Sbeq/kWh',
                                                      'value': 6.42e-08},
                                      'avg_power': {'max': 1200.0,
                                                    'min': 60.0,
                                                    'status': 'ARCHETYPE',
                                                    'unit': 'W',
                                                    'value': 300.0},
                                      'duration': {'unit': 'hours', 'value': 70080.0},
                                      'hours_life_time': {'status': 'ARCHETYPE',
                                                          'unit': 'hours',
                                                          'value': 70080.0},
                                      'type': {'status': 'ARCHETYPE', 'value': 'perso'},
                                      'units': {'max': 1, 'min': 1, 'status': 'ARCHETYPE', 'value': 1},
                                      'usage_location': {'status': 'DEFAULT',
                                                         'unit': 'CodSP3 - NCS Country Codes - NATO',
                                                         'value': 'EEE'},
                                      'use_time_ratio': {'max': 0.3,
                                                         'min': 0.3,
                                                         'status': 'ARCHETYPE',
                                                         'unit': '/1',
                                                         'value': 0.3}}}
