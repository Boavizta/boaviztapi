import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_empty_iot_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=false')

        assert res.json() == {"impacts": {'adp': {'description': 'Use of minerals and fossil ressources',
                                                  'embedded': {'max': 0.0,
                                                               'min': 0.0,
                                                               'value': 0.0,
                                                               'warnings': [
                                                                   'Connected object, not including associated '
                                                                   'digital services (use of network, '
                                                                   'datacenter, virtual machines or other '
                                                                   'terminals not included)',
                                                                   'Do not include the impact of distribution',
                                                                   'Uncertainty from technical characteristics '
                                                                   'is very important. Results should be '
                                                                   'interpreted with caution (see min and max '
                                                                   'values)']},
                                                  'unit': 'kgSbeq',
                                                  'use': 'not implemented'},
                                          'gwp': {'description': 'Total climate change',
                                                  'embedded': {'max': 0.0,
                                                               'min': 0.0,
                                                               'value': 0.0,
                                                               'warnings': [
                                                                   'Connected object, not including associated '
                                                                   'digital services (use of network, '
                                                                   'datacenter, virtual machines or other '
                                                                   'terminals not included)',
                                                                   'Do not include the impact of distribution',
                                                                   'Uncertainty from technical characteristics '
                                                                   'is very important. Results should be '
                                                                   'interpreted with caution (see min and max '
                                                                   'values)']},
                                                  'unit': 'kgCO2eq',
                                                  'use': 'not implemented'},
                                          'pe': {'description': 'Consumption of primary energy',
                                                 'embedded': {'max': 0.0,
                                                              'min': 0.0,
                                                              'value': 0.0,
                                                              'warnings': ['Connected object, not including associated '
                                                                           'digital services (use of network, '
                                                                           'datacenter, virtual machines or other '
                                                                           'terminals not included)',
                                                                           'Do not include the impact of distribution',
                                                                           'Uncertainty from technical characteristics '
                                                                           'is very important. Results should be '
                                                                           'interpreted with caution (see min and max '
                                                                           'values)']},
                                                 'unit': 'MJ',
                                                 'use': 'not implemented'}}}


@pytest.mark.asyncio
async def test_drone_mini():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=false&archetype=drone_mini&criteria=gwp')

        assert res.json() == {"impacts": {'gwp': {'description': 'Total climate change',
                                                  'embedded': {'max': 15.37,
                                                               'min': 15.37,
                                                               'value': 15.37,
                                                               'warnings': [
                                                                   'Connected object, not including associated '
                                                                   'digital services (use of network, '
                                                                   'datacenter, virtual machines or other '
                                                                   'terminals not included)',
                                                                   'Do not include the impact of '
                                                                   'distribution']},
                                                  'unit': 'kgCO2eq',
                                                  'use': 'not implemented'}}}


@pytest.mark.asyncio
async def test_drone_mini_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=true&archetype=drone_mini')

        assert res.json() == {'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                  'embedded': 'not implemented',
                                                  'unit': 'kgSbeq',
                                                  'use': 'not implemented'},
                                          'gwp': {'description': 'Total climate change',
                                                  'embedded': {'max': 15.37,
                                                               'min': 15.37,
                                                               'value': 15.37,
                                                               'warnings': ['Connected object, not '
                                                                            'including associated digital '
                                                                            'services (use of network, '
                                                                            'datacenter, virtual machines '
                                                                            'or other terminals not '
                                                                            'included)',
                                                                            'Do not include the impact of '
                                                                            'distribution']},
                                                  'unit': 'kgCO2eq',
                                                  'use': 'not implemented'},
                                          'pe': {'description': 'Consumption of primary energy',
                                                 'embedded': {'max': 222.1,
                                                              'min': 222.1,
                                                              'value': 222.1,
                                                              'warnings': ['Connected object, not including '
                                                                           'associated digital services '
                                                                           '(use of network, datacenter, '
                                                                           'virtual machines or other '
                                                                           'terminals not included)',
                                                                           'Do not include the impact of '
                                                                           'distribution']},
                                                 'unit': 'MJ',
                                                 'use': 'not implemented'}},
                              'verbose': {'ACTUATORS-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                          'hsl_level': {'status': 'ARCHETYPE',
                                                                        'unit': 'none',
                                                                        'value': 'HSL-3'},
                                                          'impacts': {'adp': {'description': 'Use of '
                                                                                             'minerals and '
                                                                                             'fossil '
                                                                                             'ressources',
                                                                              'embedded': 'not implemented',
                                                                              'unit': 'kgSbeq',
                                                                              'use': 'not implemented'},
                                                                      'gwp': {'description': 'Total climate '
                                                                                             'change',
                                                                              'embedded': {'max': 2.081,
                                                                                           'min': 2.081,
                                                                                           'value': 2.081},
                                                                              'unit': 'kgCO2eq',
                                                                              'use': 'not implemented'},
                                                                      'pe': {'description': 'Consumption of '
                                                                                            'primary energy',
                                                                             'embedded': {'max': 33.02,
                                                                                          'min': 33.02,
                                                                                          'value': 33.02},
                                                                             'unit': 'MJ',
                                                                             'use': 'not implemented'}},
                                                          'units': {'max': 1,
                                                                    'min': 1,
                                                                    'status': 'ARCHETYPE',
                                                                    'value': 1}},
                                          'CASING-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                       'hsl_level': {'status': 'ARCHETYPE',
                                                                     'unit': 'none',
                                                                     'value': 'HSL-1'},
                                                       'impacts': {'adp': {'description': 'Use of minerals '
                                                                                          'and fossil '
                                                                                          'ressources',
                                                                           'embedded': 'not implemented',
                                                                           'unit': 'kgSbeq',
                                                                           'use': 'not implemented'},
                                                                   'gwp': {'description': 'Total climate '
                                                                                          'change',
                                                                           'embedded': {'max': 0.5222,
                                                                                        'min': 0.5222,
                                                                                        'value': 0.5222},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 11.4,
                                                                                       'min': 11.4,
                                                                                       'value': 11.4},
                                                                          'unit': 'MJ',
                                                                          'use': 'not implemented'}},
                                                       'units': {'max': 1,
                                                                 'min': 1,
                                                                 'status': 'ARCHETYPE',
                                                                 'value': 1}},
                                          'CONNECTIVITY-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                             'hsl_level': {'status': 'ARCHETYPE',
                                                                           'unit': 'none',
                                                                           'value': 'HSL-1'},
                                                             'impacts': {'adp': {'description': 'Use of '
                                                                                                'minerals '
                                                                                                'and fossil '
                                                                                                'ressources',
                                                                                 'embedded': 'not '
                                                                                             'implemented',
                                                                                 'unit': 'kgSbeq',
                                                                                 'use': 'not implemented'},
                                                                         'gwp': {'description': 'Total '
                                                                                                'climate '
                                                                                                'change',
                                                                                 'embedded': {'max': 0.258,
                                                                                              'min': 0.258,
                                                                                              'value': 0.258},
                                                                                 'unit': 'kgCO2eq',
                                                                                 'use': 'not implemented'},
                                                                         'pe': {'description': 'Consumption '
                                                                                               'of primary '
                                                                                               'energy',
                                                                                'embedded': {'max': 3.44,
                                                                                             'min': 3.44,
                                                                                             'value': 3.44},
                                                                                'unit': 'MJ',
                                                                                'use': 'not implemented'}},
                                                             'units': {'max': 1,
                                                                       'min': 1,
                                                                       'status': 'ARCHETYPE',
                                                                       'value': 1}},
                                          'MEMORY-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                       'hsl_level': {'status': 'ARCHETYPE',
                                                                     'unit': 'none',
                                                                     'value': 'HSL-1'},
                                                       'impacts': {'adp': {'description': 'Use of minerals '
                                                                                          'and fossil '
                                                                                          'ressources',
                                                                           'embedded': 'not implemented',
                                                                           'unit': 'kgSbeq',
                                                                           'use': 'not implemented'},
                                                                   'gwp': {'description': 'Total climate '
                                                                                          'change',
                                                                           'embedded': {'max': 0.279,
                                                                                        'min': 0.279,
                                                                                        'value': 0.279},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 3.72,
                                                                                       'min': 3.72,
                                                                                       'value': 3.72},
                                                                          'unit': 'MJ',
                                                                          'use': 'not implemented'}},
                                                       'units': {'max': 1,
                                                                 'min': 1,
                                                                 'status': 'ARCHETYPE',
                                                                 'value': 1}},
                                          'OTHERS-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                       'hsl_level': {'status': 'ARCHETYPE',
                                                                     'unit': 'none',
                                                                     'value': 'HSL-3'},
                                                       'impacts': {'adp': {'description': 'Use of minerals '
                                                                                          'and fossil '
                                                                                          'ressources',
                                                                           'embedded': 'not implemented',
                                                                           'unit': 'kgSbeq',
                                                                           'use': 'not implemented'},
                                                                   'gwp': {'description': 'Total climate '
                                                                                          'change',
                                                                           'embedded': {'max': 2.069,
                                                                                        'min': 2.069,
                                                                                        'value': 2.069},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 39.19,
                                                                                       'min': 39.19,
                                                                                       'value': 39.19},
                                                                          'unit': 'MJ',
                                                                          'use': 'not implemented'}},
                                                       'units': {'max': 1,
                                                                 'min': 1,
                                                                 'status': 'ARCHETYPE',
                                                                 'value': 1}},
                                          'PCB-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                    'hsl_level': {'status': 'ARCHETYPE',
                                                                  'unit': 'none',
                                                                  'value': 'HSL-2'},
                                                    'impacts': {'adp': {'description': 'Use of minerals and '
                                                                                       'fossil ressources',
                                                                        'embedded': 'not implemented',
                                                                        'unit': 'kgSbeq',
                                                                        'use': 'not implemented'},
                                                                'gwp': {'description': 'Total climate '
                                                                                       'change',
                                                                        'embedded': {'max': 0.646,
                                                                                     'min': 0.646,
                                                                                     'value': 0.646},
                                                                        'unit': 'kgCO2eq',
                                                                        'use': 'not implemented'},
                                                                'pe': {'description': 'Consumption of '
                                                                                      'primary energy',
                                                                       'embedded': {'max': 13.26,
                                                                                    'min': 13.26,
                                                                                    'value': 13.26},
                                                                       'unit': 'MJ',
                                                                       'use': 'not implemented'}},
                                                    'units': {'max': 1,
                                                              'min': 1,
                                                              'status': 'ARCHETYPE',
                                                              'value': 1}},
                                          'POWER_SUPPLY-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                             'hsl_level': {'status': 'ARCHETYPE',
                                                                           'unit': 'none',
                                                                           'value': 'HSL-3'},
                                                             'impacts': {'adp': {'description': 'Use of '
                                                                                                'minerals '
                                                                                                'and fossil '
                                                                                                'ressources',
                                                                                 'embedded': 'not '
                                                                                             'implemented',
                                                                                 'unit': 'kgSbeq',
                                                                                 'use': 'not implemented'},
                                                                         'gwp': {'description': 'Total '
                                                                                                'climate '
                                                                                                'change',
                                                                                 'embedded': {'max': 5.036,
                                                                                              'min': 5.036,
                                                                                              'value': 5.036},
                                                                                 'unit': 'kgCO2eq',
                                                                                 'use': 'not implemented'},
                                                                         'pe': {'description': 'Consumption '
                                                                                               'of primary '
                                                                                               'energy',
                                                                                'embedded': {'max': 57.87,
                                                                                             'min': 57.87,
                                                                                             'value': 57.87},
                                                                                'unit': 'MJ',
                                                                                'use': 'not implemented'}},
                                                             'units': {'max': 1,
                                                                       'min': 1,
                                                                       'status': 'ARCHETYPE',
                                                                       'value': 1}},
                                          'PROCESSING-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                           'hsl_level': {'status': 'ARCHETYPE',
                                                                         'unit': 'none',
                                                                         'value': 'HSL-2'},
                                                           'impacts': {'adp': {'description': 'Use of '
                                                                                              'minerals and '
                                                                                              'fossil '
                                                                                              'ressources',
                                                                               'embedded': 'not implemented',
                                                                               'unit': 'kgSbeq',
                                                                               'use': 'not implemented'},
                                                                       'gwp': {'description': 'Total '
                                                                                              'climate '
                                                                                              'change',
                                                                               'embedded': {'max': 3.53,
                                                                                            'min': 3.53,
                                                                                            'value': 3.53},
                                                                               'unit': 'kgCO2eq',
                                                                               'use': 'not implemented'},
                                                                       'pe': {'description': 'Consumption '
                                                                                             'of primary '
                                                                                             'energy',
                                                                              'embedded': {'max': 47.1,
                                                                                           'min': 47.1,
                                                                                           'value': 47.1},
                                                                              'unit': 'MJ',
                                                                              'use': 'not implemented'}},
                                                           'units': {'max': 1,
                                                                     'min': 1,
                                                                     'status': 'ARCHETYPE',
                                                                     'value': 1}},
                                          'SENSING-1': {'duration': {'unit': 'hours', 'value': 35040.0},
                                                        'hsl_level': {'status': 'ARCHETYPE',
                                                                      'unit': 'none',
                                                                      'value': 'HSL-3'},
                                                        'impacts': {'adp': {'description': 'Use of minerals '
                                                                                           'and fossil '
                                                                                           'ressources',
                                                                            'embedded': 'not implemented',
                                                                            'unit': 'kgSbeq',
                                                                            'use': 'not implemented'},
                                                                    'gwp': {'description': 'Total climate '
                                                                                           'change',
                                                                            'embedded': {'max': 0.796,
                                                                                         'min': 0.796,
                                                                                         'value': 0.796},
                                                                            'unit': 'kgCO2eq',
                                                                            'use': 'not implemented'},
                                                                    'pe': {'description': 'Consumption of '
                                                                                          'primary energy',
                                                                           'embedded': {'max': 10.6,
                                                                                        'min': 10.6,
                                                                                        'value': 10.6},
                                                                           'unit': 'MJ',
                                                                           'use': 'not implemented'}},
                                                        'units': {'max': 1,
                                                                  'min': 1,
                                                                  'status': 'ARCHETYPE',
                                                                  'value': 1}},
                                          'USER_INTERFACE-1': {'duration': {'unit': 'hours',
                                                                            'value': 35040.0},
                                                               'hsl_level': {'status': 'ARCHETYPE',
                                                                             'unit': 'none',
                                                                             'value': 'HSL-1'},
                                                               'impacts': {'adp': {'description': 'Use of '
                                                                                                  'minerals '
                                                                                                  'and '
                                                                                                  'fossil '
                                                                                                  'ressources',
                                                                                   'embedded': 'not '
                                                                                               'implemented',
                                                                                   'unit': 'kgSbeq',
                                                                                   'use': 'not implemented'},
                                                                           'gwp': {'description': 'Total '
                                                                                                  'climate '
                                                                                                  'change',
                                                                                   'embedded': {'max': 0.1505,
                                                                                                'min': 0.1505,
                                                                                                'value': 0.1505},
                                                                                   'unit': 'kgCO2eq',
                                                                                   'use': 'not implemented'},
                                                                           'pe': {'description': 'Consumption '
                                                                                                 'of '
                                                                                                 'primary '
                                                                                                 'energy',
                                                                                  'embedded': {'max': 2.451,
                                                                                               'min': 2.451,
                                                                                               'value': 2.451},
                                                                                  'unit': 'MJ',
                                                                                  'use': 'not implemented'}},
                                                               'units': {'max': 1,
                                                                         'min': 1,
                                                                         'status': 'ARCHETYPE',
                                                                         'value': 1}},
                                          'duration': {'unit': 'hours', 'value': 35040.0},
                                          'hours_life_time': {'max': 35040.0,
                                                              'min': 35040.0,
                                                              'status': 'ARCHETYPE',
                                                              'unit': 'hours',
                                                              'value': 35040.0},
                                          'units': {'max': 1, 'min': 1, 'status': 'ARCHETYPE', 'value': 1}}}


@pytest.mark.asyncio
async def test_drone_mini_costume_usage():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/iot/iot_device?verbose=false&archetype=drone_mini&duration=1', json={
            "usage": {
                "avg_power": 100,
                "usage_location": "FRA"
            }
        })

        assert res.json() == {"impacts": {'adp': {'description': 'Use of minerals and fossil ressources',
                                                  'embedded': 'not implemented',
                                                  'unit': 'kgSbeq',
                                                  'use': {'max': 4.858e-09, 'min': 4.858e-09, 'value': 4.858e-09}},
                                          'gwp': {'description': 'Total climate change',
                                                  'embedded': {'max': 0.0004386,
                                                               'min': 0.0004386,
                                                               'value': 0.0004386,
                                                               'warnings': [
                                                                   'Connected object, not including associated '
                                                                   'digital services (use of network, '
                                                                   'datacenter, virtual machines or other '
                                                                   'terminals not included)',
                                                                   'Do not include the impact of '
                                                                   'distribution']},
                                                  'unit': 'kgCO2eq',
                                                  'use': {'max': 0.0098, 'min': 0.0098, 'value': 0.0098}},
                                          'pe': {'description': 'Consumption of primary energy',
                                                 'embedded': {'max': 0.006337,
                                                              'min': 0.006337,
                                                              'value': 0.006337,
                                                              'warnings': ['Connected object, not including associated '
                                                                           'digital services (use of network, '
                                                                           'datacenter, virtual machines or other '
                                                                           'terminals not included)',
                                                                           'Do not include the impact of distribution']},
                                                 'unit': 'MJ',
                                                 'use': {'max': 1.129, 'min': 1.129, 'value': 1.129}}}}


@pytest.mark.asyncio
async def test_custom_iot():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.post('/v1/iot/iot_device?verbose=false&criteria=lu', json={
            "functional_blocks": [
                {
                    "hsl_level": "HSL-1",
                    "type": "security"
                },
                {
                    "hsl_level": "HSL-1",
                    "type": "pcb"
                }
            ]
        })

        assert res.json() == {"impacts": {'lu': {'description': 'Land use',
                                                 'embedded': {'max': 0.06678,
                                                              'min': 0.06678,
                                                              'value': 0.06678,
                                                              'warnings': ['Connected object, not including associated '
                                                                           'digital services (use of network, '
                                                                           'datacenter, virtual machines or other '
                                                                           'terminals not included)',
                                                                           'Do not include the impact of distribution']},
                                                 'unit': 'No dimension',
                                                 'use': 'not implemented'}}}
