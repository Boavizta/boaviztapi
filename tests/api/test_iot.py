import pytest
from httpx import AsyncClient

from boaviztapi.main import app

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_empty_iot_device():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=false')

        assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                      'embedded': {'max': 0.0,
                                                   'min': 0.0,
                                                   'significant_figures': 5,
                                                   'value': 0.0,
                                                   'warnings': ['Connected object, not including associated '
                                                                'digital services (use of network, '
                                                                'datacenter, virtual machines or other '
                                                                'terminals not included)',
                                                                'Do not include the impact of '
                                                                'distribution']},
                                      'unit': 'kgSbeq',
                                      'use': 'not implemented'},
                              'gwp': {'description': 'Total climate change',
                                      'embedded': {'max': 0.0,
                                                   'min': 0.0,
                                                   'significant_figures': 5,
                                                   'value': 0.0,
                                                   'warnings': ['Connected object, not including associated '
                                                                'digital services (use of network, '
                                                                'datacenter, virtual machines or other '
                                                                'terminals not included)',
                                                                'Do not include the impact of '
                                                                'distribution']},
                                      'unit': 'kgCO2eq',
                                      'use': 'not implemented'},
                              'pe': {'description': 'Consumption of primary energy',
                                     'embedded': {'max': 0.0,
                                                  'min': 0.0,
                                                  'significant_figures': 5,
                                                  'value': 0.0,
                                                  'warnings': ['Connected object, not including associated '
                                                               'digital services (use of network, '
                                                               'datacenter, virtual machines or other '
                                                               'terminals not included)',
                                                               'Do not include the impact of distribution']},
                                     'unit': 'MJ',
                                     'use': 'not implemented'}}


@pytest.mark.asyncio
async def test_drone_mini():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=false&archetype=drone_mini&criteria=gwp')

        assert res.json() == {'gwp': {'description': 'Total climate change',
                                      'embedded': {'max': 15.368,
                                                   'min': 15.368,
                                                   'significant_figures': 5,
                                                   'value': 15.368,
                                                   'warnings': ['Connected object, not including associated '
                                                                'digital services (use of network, '
                                                                'datacenter, virtual machines or other '
                                                                'terminals not included)',
                                                                'Do not include the impact of '
                                                                'distribution']},
                                      'unit': 'kgCO2eq',
                                      'use': 'not implemented'}}


@pytest.mark.asyncio
async def test_drone_mini_verbose():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        res = await ac.get('/v1/iot/iot_device?verbose=true&archetype=drone_mini')

        assert res.json() == {'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                  'embedded': 'not implemented',
                                                  'unit': 'kgSbeq',
                                                  'use': 'not implemented'},
                                          'gwp': {'description': 'Total climate change',
                                                  'embedded': {'max': 15.368,
                                                               'min': 15.368,
                                                               'significant_figures': 5,
                                                               'value': 15.368,
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
                                                 'embedded': {'max': 222.05,
                                                              'min': 222.05,
                                                              'significant_figures': 5,
                                                              'value': 222.05,
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
                                                                                           'significant_figures': 5,
                                                                                           'value': 2.081},
                                                                              'unit': 'kgCO2eq',
                                                                              'use': 'not implemented'},
                                                                      'pe': {'description': 'Consumption of '
                                                                                            'primary energy',
                                                                             'embedded': {'max': 33.02,
                                                                                          'min': 33.02,
                                                                                          'significant_figures': 5,
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
                                                                                        'significant_figures': 5,
                                                                                        'value': 0.5222},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 11.4,
                                                                                       'min': 11.4,
                                                                                       'significant_figures': 5,
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
                                                                                 'embedded': {'max': 0.25801,
                                                                                              'min': 0.25801,
                                                                                              'significant_figures': 5,
                                                                                              'value': 0.25801},
                                                                                 'unit': 'kgCO2eq',
                                                                                 'use': 'not implemented'},
                                                                         'pe': {'description': 'Consumption '
                                                                                               'of primary '
                                                                                               'energy',
                                                                                'embedded': {'max': 3.4401,
                                                                                             'min': 3.4401,
                                                                                             'significant_figures': 5,
                                                                                             'value': 3.4401},
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
                                                                           'embedded': {'max': 0.27901,
                                                                                        'min': 0.27901,
                                                                                        'significant_figures': 5,
                                                                                        'value': 0.27901},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 3.7201,
                                                                                       'min': 3.7201,
                                                                                       'significant_figures': 5,
                                                                                       'value': 3.7201},
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
                                                                           'embedded': {'max': 2.0693,
                                                                                        'min': 2.0693,
                                                                                        'significant_figures': 5,
                                                                                        'value': 2.0693},
                                                                           'unit': 'kgCO2eq',
                                                                           'use': 'not implemented'},
                                                                   'pe': {'description': 'Consumption of '
                                                                                         'primary energy',
                                                                          'embedded': {'max': 39.186,
                                                                                       'min': 39.186,
                                                                                       'significant_figures': 5,
                                                                                       'value': 39.186},
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
                                                                                     'significant_figures': 5,
                                                                                     'value': 0.646},
                                                                        'unit': 'kgCO2eq',
                                                                        'use': 'not implemented'},
                                                                'pe': {'description': 'Consumption of '
                                                                                      'primary energy',
                                                                       'embedded': {'max': 13.263,
                                                                                    'min': 13.263,
                                                                                    'significant_figures': 5,
                                                                                    'value': 13.263},
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
                                                                                 'embedded': {'max': 5.0357,
                                                                                              'min': 5.0357,
                                                                                              'significant_figures': 5,
                                                                                              'value': 5.0357},
                                                                                 'unit': 'kgCO2eq',
                                                                                 'use': 'not implemented'},
                                                                         'pe': {'description': 'Consumption '
                                                                                               'of primary '
                                                                                               'energy',
                                                                                'embedded': {'max': 57.871,
                                                                                             'min': 57.871,
                                                                                             'significant_figures': 5,
                                                                                             'value': 57.871},
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
                                                                               'embedded': {'max': 3.5301,
                                                                                            'min': 3.5301,
                                                                                            'significant_figures': 5,
                                                                                            'value': 3.5301},
                                                                               'unit': 'kgCO2eq',
                                                                               'use': 'not implemented'},
                                                                       'pe': {'description': 'Consumption '
                                                                                             'of primary '
                                                                                             'energy',
                                                                              'embedded': {'max': 47.101,
                                                                                           'min': 47.101,
                                                                                           'significant_figures': 5,
                                                                                           'value': 47.101},
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
                                                                            'embedded': {'max': 0.79604,
                                                                                         'min': 0.79604,
                                                                                         'significant_figures': 5,
                                                                                         'value': 0.79604},
                                                                            'unit': 'kgCO2eq',
                                                                            'use': 'not implemented'},
                                                                    'pe': {'description': 'Consumption of '
                                                                                          'primary energy',
                                                                           'embedded': {'max': 10.6,
                                                                                        'min': 10.6,
                                                                                        'significant_figures': 5,
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
                                                                                   'embedded': {'max': 0.15054,
                                                                                                'min': 0.15054,
                                                                                                'significant_figures': 5,
                                                                                                'value': 0.15054},
                                                                                   'unit': 'kgCO2eq',
                                                                                   'use': 'not implemented'},
                                                                           'pe': {'description': 'Consumption '
                                                                                                 'of '
                                                                                                 'primary '
                                                                                                 'energy',
                                                                                  'embedded': {'max': 2.4511,
                                                                                               'min': 2.4511,
                                                                                               'significant_figures': 5,
                                                                                               'value': 2.4511},
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

        assert res.json() == {'adp': {'description': 'Use of minerals and fossil ressources',
                                      'embedded': 'not implemented',
                                      'unit': 'kgSbeq',
                                      'use': {'max': 4.858e-09,
                                              'min': 4.858e-09,
                                              'significant_figures': 5,
                                              'value': 4.858e-09}},
                              'gwp': {'description': 'Total climate change',
                                      'embedded': {'max': 0.00043858,
                                                   'min': 0.00043858,
                                                   'significant_figures': 5,
                                                   'value': 0.00043858,
                                                   'warnings': ['Connected object, not including associated '
                                                                'digital services (use of network, '
                                                                'datacenter, virtual machines or other '
                                                                'terminals not included)',
                                                                'Do not include the impact of '
                                                                'distribution']},
                                      'unit': 'kgCO2eq',
                                      'use': {'max': 0.0098,
                                              'min': 0.0098,
                                              'significant_figures': 5,
                                              'value': 0.0098}},
                              'pe': {'description': 'Consumption of primary energy',
                                     'embedded': {'max': 0.0063371,
                                                  'min': 0.0063371,
                                                  'significant_figures': 5,
                                                  'value': 0.0063371,
                                                  'warnings': ['Connected object, not including associated '
                                                               'digital services (use of network, '
                                                               'datacenter, virtual machines or other '
                                                               'terminals not included)',
                                                               'Do not include the impact of distribution']},
                                     'unit': 'MJ',
                                     'use': {'max': 1.1289,
                                             'min': 1.1289,
                                             'significant_figures': 5,
                                             'value': 1.1289}}}


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

        assert res.json() == {'lu': {'description': 'Land use',
                                     'embedded': {'max': 0.06678,
                                                  'min': 0.06678,
                                                  'significant_figures': 5,
                                                  'value': 0.06678,
                                                  'warnings': ['Connected object, not including associated '
                                                               'digital services (use of network, '
                                                               'datacenter, virtual machines or other '
                                                               'terminals not included)',
                                                               'Do not include the impact of distribution']},
                                     'unit': 'No dimension',
                                     'use': 'not implemented'}}
