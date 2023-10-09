from boaviztapi.service.verbose import verbose_component, verbose_device


def test_verbose_component_cpu_1(complete_cpu_model):
    verbose = verbose_component(complete_cpu_model, duration=complete_cpu_model.usage.hours_life_time.value)
    assert verbose["core_units"] == {'status': 'INPUT', 'value': 24}
    assert verbose["die_size_per_core"] == {'status': 'INPUT', 'unit': 'mm2', 'value': 24.5}

    assert verbose["impacts"] == {'adp': {'description': 'Use of minerals and fossil ressources',
                                          'embedded': {'max': 0.04081,
                                                       'min': 0.04081,
                                                       'value': 0.04081,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgSbeq',
                                          'use': {'max': 0.002544, 'min': 0.0001264, 'value': 0.0006}},
                                  'gwp': {'description': 'Total climate change',
                                          'embedded': {'max': 43.38,
                                                       'min': 43.38,
                                                       'value': 43.38,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgCO2eq',
                                          'use': {'max': 8620.0, 'min': 220.3, 'value': 3600.0}},
                                  'pe': {'description': 'Consumption of primary energy',
                                         'embedded': {'max': 649.7,
                                                      'min': 649.7,
                                                      'value': 649.7,
                                                      'warnings': ['End of life is not included in the '
                                                                   'calculation']},
                                         'unit': 'MJ',
                                         'use': {'max': 4484000.0, 'min': 124.5, 'value': 100000.0}}}


def test_verbose_component_cpu_2(incomplete_cpu_model):
    verbose = verbose_component(incomplete_cpu_model, duration=incomplete_cpu_model.usage.hours_life_time.value)
    assert verbose["core_units"] == {'status': 'INPUT', 'value': 12}
    assert verbose["family"] == {'status': 'INPUT', 'value': 'Skylake'}
    assert verbose["impacts"] == {'adp': {'description': 'Use of minerals and fossil ressources',
                                          'embedded': {'max': 0.0204,
                                                       'min': 0.0204,
                                                       'value': 0.0204,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgSbeq',
                                          'use': {'max': 0.001272, 'min': 6.321e-05, 'value': 0.0003}},
                                  'gwp': {'description': 'Total climate change',
                                          'embedded': {'max': 19.66,
                                                       'min': 19.66,
                                                       'value': 19.66,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgCO2eq',
                                          'use': {'max': 4310.0, 'min': 110.1, 'value': 1800.0}},
                                  'pe': {'description': 'Consumption of primary energy',
                                         'embedded': {'max': 297.5,
                                                      'min': 297.5,
                                                      'value': 297.5,
                                                      'warnings': ['End of life is not included in the '
                                                                   'calculation']},
                                         'unit': 'MJ',
                                         'use': {'max': 2242000.0, 'min': 62.25, 'value': 100000.0}}}


def test_verbose_component_ram(complete_ram_model):
    verbose = verbose_component(complete_ram_model, duration=complete_ram_model.usage.hours_life_time.value)
    assert verbose["impacts"] == {'adp': {'description': 'Use of minerals and fossil ressources',
                                          'embedded': {'max': 0.0338,
                                                       'min': 0.0338,
                                                       'value': 0.0338,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgSbeq',
                                          'use': {'max': 0.0007612, 'min': 3.783e-05, 'value': 0.00018}},
                                  'gwp': {'description': 'Total climate change',
                                          'embedded': {'max': 534.6,
                                                       'min': 534.6,
                                                       'value': 534.6,
                                                       'warnings': ['End of life is not included in the '
                                                                    'calculation']},
                                          'unit': 'kgCO2eq',
                                          'use': {'max': 2579.0, 'min': 65.92, 'value': 1100.0}},
                                  'pe': {'description': 'Consumption of primary energy',
                                         'embedded': {'max': 6745.0,
                                                      'min': 6745.0,
                                                      'value': 6745.0,
                                                      'warnings': ['End of life is not included in the '
                                                                   'calculation']},
                                         'unit': 'MJ',
                                         'use': {'max': 1342000.0,
                                                 'min': 37.26,
                                                 'value': 40000.0,
                                                 'warnings': ['Uncertainty from technical characteristics is very important. '
                                                              'Results should be interpreted with caution (see '
                                                              'min and max values)']}}}

    assert verbose["capacity"] == {'status': 'INPUT', 'unit': 'GB', 'value': 32}
    assert verbose["density"] == {'status': 'INPUT', 'unit': 'GB/cm2', 'value': 1.79}


def test_verbose_component_ssd(empty_ssd_model):
    assert verbose_component(empty_ssd_model, duration=empty_ssd_model.usage.hours_life_time.value) == {
        'capacity': {'max': 5000.0,
                     'min': 100.0,
                     'status': 'ARCHETYPE',
                     'unit': 'GB',
                     'value': 1000.0},
        'density': {'max': 1.0,
                    'min': 0.1,
                    'status': 'ARCHETYPE',
                    'unit': 'GB/cm2',
                    'value': 48.5},
        'duration': {'unit': 'hours', 'value': 26280.0},
        'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                            'embedded': {'max': 3.151,
                                         'min': 0.006863,
                                         'value': 0.002,
                                         'warnings': ['End of life is not included in '
                                                      'the calculation',
                                                      'Uncertainty from technical characteristics is '
                                                      'very important. Results should '
                                                      'be interpreted with caution '
                                                      '(see min and max values)']},
                            'unit': 'kgSbeq',
                            'use': 'not implemented'},
                    'gwp': {'description': 'Total climate change',
                            'embedded': {'max': 110000.0,
                                         'min': 226.3,
                                         'value': 50.0,
                                         'warnings': ['End of life is not included in '
                                                      'the calculation',
                                                      'Uncertainty from technical characteristics is '
                                                      'very important. Results should '
                                                      'be interpreted with caution '
                                                      '(see min and max values)']},
                            'unit': 'kgCO2eq',
                            'use': 'not implemented'},
                    'pe': {'description': 'Consumption of primary energy',
                           'embedded': {'max': 1365000.0,
                                        'min': 2807.0,
                                        'value': 600.0,
                                        'warnings': ['End of life is not included in '
                                                     'the calculation',
                                                     'Uncertainty from technical characteristics is '
                                                     'very important. Results should '
                                                     'be interpreted with caution '
                                                     '(see min and max values)']},
                           'unit': 'MJ',
                           'use': 'not implemented'}},
        'units': {'max': 1.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 1.0}}


def test_verbose_component_power_supply(empty_power_supply_model):
    assert verbose_component(empty_power_supply_model, duration=empty_power_supply_model.usage.hours_life_time.value) \
           == {'duration': {'unit': 'hours', 'value': 26280.0},
               'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                   'embedded': {'max': 0.0415,
                                                'min': 0.0083,
                                                'value': 0.025,
                                                'warnings': ['End of life is not included in '
                                                             'the calculation']},
                                   'unit': 'kgSbeq',
                                   'use': 'not implemented'},
                           'gwp': {'description': 'Total climate change',
                                   'embedded': {'max': 121.5,
                                                'min': 24.3,
                                                'value': 73.0,
                                                'warnings': ['End of life is not included in '
                                                             'the calculation']},
                                   'unit': 'kgCO2eq',
                                   'use': 'not implemented'},
                           'pe': {'description': 'Consumption of primary energy',
                                  'embedded': {'max': 1760.0,
                                               'min': 352.0,
                                               'value': 1100.0,
                                               'warnings': ['End of life is not included in '
                                                            'the calculation']},
                                  'unit': 'MJ',
                                  'use': 'not implemented'}},
               'unit_weight': {'max': 5.0,
                               'min': 1.0,
                               'status': 'ARCHETYPE',
                               'unit': 'kg',
                               'value': 2.99},
               'units': {'max': 1.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 1.0}}


def test_verbose_component_case(blade_case_model):
    assert verbose_component(blade_case_model, duration=blade_case_model.usage.hours_life_time.value) == {
        'case_type': {'status': 'INPUT', 'value': 'blade'},
        'duration': {'unit': 'hours', 'value': 2628.0},
        'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                            'embedded': {'max': 0.02767,
                                         'min': 0.02767,
                                         'value': 0.02767,
                                         'warnings': ['End of life is not included in '
                                                      'the calculation']},
                            'unit': 'kgSbeq',
                            'use': 'not implemented'},
                    'gwp': {'description': 'Total climate change',
                            'embedded': {'max': 85.9,
                                         'min': 85.9,
                                         'value': 85.9,
                                         'warnings': ['End of life is not included in '
                                                      'the calculation']},
                            'unit': 'kgCO2eq',
                            'use': 'not implemented'},
                    'pe': {'description': 'Consumption of primary energy',
                           'embedded': {'max': 1229.0,
                                        'min': 1229.0,
                                        'value': 1229.0,
                                        'warnings': ['End of life is not included in '
                                                     'the calculation']},
                           'unit': 'MJ',
                           'use': 'not implemented'}},
        'units': {'max': 1.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 1.0}}


def test_verbose_device_server_1(incomplete_server_model):
    verbose = verbose_device(incomplete_server_model, duration=incomplete_server_model.usage.hours_life_time.value)

    assert verbose["ASSEMBLY-1"] == {'duration': {'unit': 'hours', 'value': 35040.0},
                                     'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                         'embedded': {'max': 1.41e-06,
                                                                      'min': 1.41e-06,
                                                                      'value': 1.41e-06,
                                                                      'warnings': ['End of life is not included in '
                                                                                   'the calculation']},
                                                         'unit': 'kgSbeq',
                                                         'use': 'not implemented'},
                                                 'gwp': {'description': 'Total climate change',
                                                         'embedded': {'max': 6.68,
                                                                      'min': 6.68,
                                                                      'value': 6.68,
                                                                      'warnings': ['End of life is not included in '
                                                                                   'the calculation']},
                                                         'unit': 'kgCO2eq',
                                                         'use': 'not implemented'},
                                                 'pe': {'description': 'Consumption of primary energy',
                                                        'embedded': {'max': 68.6,
                                                                     'min': 68.6,
                                                                     'value': 68.6,
                                                                     'warnings': ['End of life is not included in '
                                                                                  'the calculation']},
                                                        'unit': 'MJ',
                                                        'use': 'not implemented'}},
                                     'units': {'max': 1, 'min': 1, 'status': 'ARCHETYPE', 'value': 1}}

    assert verbose["CASE-1"] == {'case_type': {'status': 'INPUT', 'value': 'rack'},
                                 'duration': {'unit': 'hours', 'value': 35040.0},
                                 'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                     'embedded': {'max': 0.0202,
                                                                  'min': 0.0202,
                                                                  'value': 0.0202,
                                                                  'warnings': ['End of life is not included in '
                                                                               'the calculation']},
                                                     'unit': 'kgSbeq',
                                                     'use': 'not implemented'},
                                             'gwp': {'description': 'Total climate change',
                                                     'embedded': {'max': 150.0,
                                                                  'min': 150.0,
                                                                  'value': 150.0,
                                                                  'warnings': ['End of life is not included in '
                                                                               'the calculation']},
                                                     'unit': 'kgCO2eq',
                                                     'use': 'not implemented'},
                                             'pe': {'description': 'Consumption of primary energy',
                                                    'embedded': {'max': 2200.0,
                                                                 'min': 2200.0,
                                                                 'value': 2200.0,
                                                                 'warnings': ['End of life is not included in '
                                                                              'the calculation']},
                                                    'unit': 'MJ',
                                                    'use': 'not implemented'}},
                                 'units': {'max': 1.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 1.0}}

    assert verbose["MOTHERBOARD-1"] == {
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.00369,
                    'min': 0.00369,
                    'value': 0.00369,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 66.1,
                    'min': 66.1,
                    'value': 66.1,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 836.0,
                    'min': 836.0,
                    'value': 836.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'units': {
            'max': 1,
            'min': 1,
            'status': 'ARCHETYPE',
            'value': 1
        }
    }

    assert verbose["POWER_SUPPLY-1"] == {'duration': {'unit': 'hours', 'value': 35040.0},
                                         'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                             'embedded': {'max': 0.166,
                                                                          'min': 0.0083,
                                                                          'value': 0.05,
                                                                          'warnings': ['End of life is not included in '
                                                                                       'the calculation']},
                                                             'unit': 'kgSbeq',
                                                             'use': 'not implemented'},
                                                     'gwp': {'description': 'Total climate change',
                                                             'embedded': {'max': 486.0,
                                                                          'min': 24.3,
                                                                          'value': 150.0,
                                                                          'warnings': ['End of life is not included in '
                                                                                       'the calculation']},
                                                             'unit': 'kgCO2eq',
                                                             'use': 'not implemented'},
                                                     'pe': {'description': 'Consumption of primary energy',
                                                            'embedded': {'max': 7040.0,
                                                                         'min': 352.0,
                                                                         'value': 2100.0,
                                                                         'warnings': ['End of life is not included in '
                                                                                      'the calculation']},
                                                            'unit': 'MJ',
                                                            'use': 'not implemented'}},
                                         'unit_weight': {'max': 5.0,
                                                         'min': 1.0,
                                                         'status': 'ARCHETYPE',
                                                         'unit': 'kg',
                                                         'value': 2.99},
                                         'units': {'max': 4.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 2.0}}


def test_verbose_device_server_2(dell_r740_model):
    verbose = verbose_device(dell_r740_model, duration=dell_r740_model.usage.hours_life_time.value)
    assert verbose["ASSEMBLY-1"] == {
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 1.41e-06,
                    'min': 1.41e-06,
                    'value': 1.41e-06,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 6.68,
                    'min': 6.68,
                    'value': 6.68,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 68.6,
                    'min': 68.6,
                    'value': 68.6,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'units': {
            'max': 1,
            'min': 1,
            'status': 'ARCHETYPE',
            'value': 1
        }
    }

    assert verbose["CASE-1"] == {
        'case_type': {
            'status': 'INPUT',
            'value': 'rack'
        },
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.0202,
                    'min': 0.0202,
                    'value': 0.0202,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 150.0,
                    'min': 150.0,
                    'value': 150.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 2200.0,
                    'min': 2200.0,
                    'value': 2200.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'units': {
            'max': 1.0,
            'min': 1.0,
            'status': 'ARCHETYPE',
            'value': 1.0
        }
    }

    assert verbose["MOTHERBOARD-1"] == {
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.00369,
                    'min': 0.00369,
                    'value': 0.00369,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 66.1,
                    'min': 66.1,
                    'value': 66.1,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 836.0,
                    'min': 836.0,
                    'value': 836.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'units': {
            'max': 1,
            'min': 1,
            'status': 'ARCHETYPE',
            'value': 1
        }
    }

    assert verbose["POWER_SUPPLY-1"] == {'duration': {'unit': 'hours', 'value': 35040.0},
                                         'impacts': {'adp': {'description': 'Use of minerals and fossil ressources',
                                                             'embedded': {'max': 0.04963,
                                                                          'min': 0.04963,
                                                                          'value': 0.04963,
                                                                          'warnings': ['End of life is not included in '
                                                                                       'the calculation']},
                                                             'unit': 'kgSbeq',
                                                             'use': 'not implemented'},
                                                     'gwp': {'description': 'Total climate change',
                                                             'embedded': {'max': 145.3,
                                                                          'min': 145.3,
                                                                          'value': 145.3,
                                                                          'warnings': ['End of life is not included in '
                                                                                       'the calculation']},
                                                             'unit': 'kgCO2eq',
                                                             'use': 'not implemented'},
                                                     'pe': {'description': 'Consumption of primary energy',
                                                            'embedded': {'max': 2105.0,
                                                                         'min': 2105.0,
                                                                         'value': 2105.0,
                                                                         'warnings': ['End of life is not included in '
                                                                                      'the calculation']},
                                                            'unit': 'MJ',
                                                            'use': 'not implemented'}},
                                         'unit_weight': {'status': 'INPUT', 'unit': 'kg', 'value': 2.99},
                                         'units': {'status': 'INPUT', 'value': 2}}
