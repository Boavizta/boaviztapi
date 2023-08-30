from boaviztapi.service.verbose import verbose_component, verbose_device


def test_verbose_component_cpu_1(complete_cpu_model):
    verbose = verbose_component(complete_cpu_model, duration=complete_cpu_model.usage.hours_life_time.value)
    assert verbose["core_units"] == {'status': 'INPUT', 'value': 24}
    assert verbose["die_size_per_core"] == {'status': 'INPUT', 'unit': 'mm2', 'value': 24.5}

    assert verbose["impacts"] == {
        'adp': {
            'description': 'Use of minerals and fossil ressources',
            'embedded': {
                'max': 0.041,
                'min': 0.041,
                'significant_figures': 2,
                'value': 0.041,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'kgSbeq',
            'use': {
                'max': 0.0025,
                'min': 0.00013,
                'significant_figures': 2,
                'value': 0.00061
            }
        },
        'gwp': {
            'description': 'Total climate change',
            'embedded': {
                'max': 43.4,
                'min': 43.4,
                'significant_figures': 3,
                'value': 43.4,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'kgCO2eq',
            'use': {
                'max': 8600.0,
                'min': 220.0,
                'significant_figures': 2,
                'value': 3600.0
            }
        },
        'pe': {
            'description': 'Consumption of primary energy',
            'embedded': {
                'max': 650.0,
                'min': 650.0,
                'significant_figures': 3,
                'value': 650.0,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'MJ',
            'use': {
                'max': 4500000.0,
                'min': 120.0,
                'significant_figures': 2,
                'value': 120000.0
            }
        }
    }


def test_verbose_component_cpu_2(incomplete_cpu_model):
    verbose = verbose_component(incomplete_cpu_model, duration=incomplete_cpu_model.usage.hours_life_time.value)
    assert verbose["core_units"] == {'status': 'INPUT', 'value': 12}
    assert verbose["family"] == {'status': 'INPUT', 'value': 'Skylake'}
    assert verbose["impacts"] == {
        'adp': {
            'description': 'Use of minerals and fossil ressources',
            'embedded': {
                'max': 0.02,
                'min': 0.02,
                'significant_figures': 2,
                'value': 0.02,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'kgSbeq',
            'use': {
                'max': 0.0013,
                'min': 6.3e-05,
                'significant_figures': 2,
                'value': 0.00031
            }
        },
        'gwp': {
            'description': 'Total climate change',
            'embedded': {
                'max': 19.7,
                'min': 19.7,
                'significant_figures': 3,
                'value': 19.7,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'kgCO2eq',
            'use': {
                'max': 4300.0,
                'min': 110.0,
                'significant_figures': 2,
                'value': 1800.0
            }
        },
        'pe': {
            'description': 'Consumption of primary energy',
            'embedded': {
                'max': 297.0,
                'min': 297.0,
                'significant_figures': 3,
                'value': 297.0,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'MJ',
            'use': {
                'max': 2200000.0,
                'min': 62.0,
                'significant_figures': 2,
                'value': 62000.0
            }
        }
    }


def test_verbose_component_ram(complete_ram_model):
    verbose = verbose_component(complete_ram_model, duration=complete_ram_model.usage.hours_life_time.value)
    assert verbose["impacts"] == {
        'adp': {
            'description': 'Use of minerals and fossil ressources',
            'embedded': {
                'max': 0.034,
                'min': 0.034,
                'significant_figures': 2,
                'value': 0.034,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'kgSbeq',
            'use': {
                'max': 0.00076,
                'min': 3.8e-05,
                'significant_figures': 2,
                'value': 0.00018
            }
        },
        'gwp': {
            'description': 'Total climate change',
            'embedded': {
                'max': 530.0,
                'min': 530.0,
                'significant_figures': 2,
                'value': 530.0,
                'warnings': ['End of life is not included in the calculation']},
            'unit': 'kgCO2eq',
            'use': {
                'max': 2600.0,
                'min': 66.0,
                'significant_figures': 2,
                'value': 1100.0
            }
        },
        'pe': {
            'description': 'Consumption of primary energy',
            'embedded': {
                'max': 6700.0,
                'min': 6700.0,
                'significant_figures': 2,
                'value': 6700.0,
                'warnings': ['End of life is not included in the calculation']
            },
            'unit': 'MJ',
            'use': {
                'max': 1300000.0,
                'min': 37.0,
                'significant_figures': 2,
                'value': 37000.0
            }
        }
    }

    assert verbose["capacity"] == {'status': 'INPUT', 'unit': 'GB', 'value': 32}
    assert verbose["density"] == {'status': 'INPUT', 'unit': 'GB/cm2', 'value': 1.79}


def test_verbose_component_ssd(empty_ssd_model):
    assert verbose_component(empty_ssd_model, duration=empty_ssd_model.usage.hours_life_time.value) == {
        'capacity': {
            'max': 5000.0,
            'min': 100.0,
            'status': 'ARCHETYPE',
            'unit': 'GB',
            'value': 1000.0
        },
        'density': {
            'max': 1.0,
            'min': 0.1,
            'status': 'ARCHETYPE',
            'unit': 'GB/cm2',
            'value': 48.5
        },
        'duration': {
            'unit': 'hours',
            'value': 26280.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 3.2,
                    'min': 0.0069,
                    'significant_figures': 2,
                    'value': 0.0019,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 110000.0,
                    'min': 230.0,
                    'significant_figures': 2,
                    'value': 52.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 1370000.0,
                    'min': 2810.0,
                    'significant_figures': 3,
                    'value': 640.0,
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


def test_verbose_component_power_supply(empty_power_supply_model):
    assert verbose_component(empty_power_supply_model, duration=empty_power_supply_model.usage.hours_life_time.value) \
           == {
               'duration': {
                   'unit': 'hours', 'value': 26280.0
               },
               'impacts': {
                   'adp': {
                       'description': 'Use of minerals and fossil ressources',
                       'embedded': {
                           'max': 0.042,
                           'min': 0.0083,
                           'significant_figures': 2,
                           'value': 0.025,
                           'warnings': ['End of life is not included in the calculation']
                       },
                       'unit': 'kgSbeq',
                       'use': 'not implemented'
                   },
                   'gwp': {
                       'description': 'Total climate change',
                       'embedded': {
                           'max': 122.0,
                           'min': 24.3,
                           'significant_figures': 3,
                           'value': 72.7,
                           'warnings': ['End of life is not included in the calculation']
                       },
                       'unit': 'kgCO2eq',
                       'use': 'not implemented'
                   },
                   'pe': {
                       'description': 'Consumption of primary energy',
                       'embedded': {
                           'max': 1760.0,
                           'min': 352.0,
                           'significant_figures': 3,
                           'value': 1050.0,
                           'warnings': ['End of life is not included in the calculation']
                       },
                       'unit': 'MJ',
                       'use': 'not implemented'
                   }
               },
               'unit_weight': {
                   'max': 5.0,
                   'min': 1.0,
                   'status': 'ARCHETYPE',
                   'unit': 'kg',
                   'value': 2.99
               },
               'units': {
                   'max': 1.0, 'min': 1.0, 'status': 'ARCHETYPE', 'value': 1.0
               }
           }


def test_verbose_component_case(blade_case_model):
    assert verbose_component(blade_case_model, duration=blade_case_model.usage.hours_life_time.value) == {
        'case_type': {
            'status': 'INPUT',
            'value': 'blade'
        },
        'duration': {
            'unit': 'hours',
            'value': 2628.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.0277,
                    'min': 0.0277,
                    'significant_figures': 3,
                    'value': 0.0277,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 85.9,
                    'min': 85.9,
                    'significant_figures': 3,
                    'value': 85.9,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 1230.0,
                    'min': 1230.0,
                    'significant_figures': 3,
                    'value': 1230.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'units': {
            'max': 1.0,
            'min': 1.0,
            'status':
                'ARCHETYPE', 'value': 1.0
        }
    }


def test_verbose_device_server_1(incomplete_server_model):
    verbose = verbose_device(incomplete_server_model, duration=incomplete_server_model.usage.hours_life_time.value)

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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 4,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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

    assert verbose["POWER_SUPPLY-1"] == {
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.17,
                    'min': 0.0083,
                    'significant_figures': 2,
                    'value': 0.05,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 486.0,
                    'min': 24.3,
                    'significant_figures': 3,
                    'value': 145.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 7040.0,
                    'min': 352.0,
                    'significant_figures': 3,
                    'value': 2100.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'unit_weight': {
            'max': 5.0,
            'min': 1.0,
            'status': 'ARCHETYPE',
            'unit': 'kg',
            'value': 2.99},
        'units': {
            'max': 4.0,
            'min': 1.0,
            'status': 'ARCHETYPE',
            'value': 2.0
        }
    }


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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 4,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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
                    'significant_figures': 3,
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

    assert verbose["POWER_SUPPLY-1"] == {
        'duration': {
            'unit': 'hours',
            'value': 35040.0
        },
        'impacts': {
            'adp': {
                'description': 'Use of minerals and fossil ressources',
                'embedded': {
                    'max': 0.05,
                    'min': 0.05,
                    'significant_figures': 2,
                    'value': 0.05,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgSbeq',
                'use': 'not implemented'
            },
            'gwp': {
                'description': 'Total climate change',
                'embedded': {
                    'max': 145.0,
                    'min': 145.0,
                    'significant_figures': 3,
                    'value': 145.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'kgCO2eq',
                'use': 'not implemented'
            },
            'pe': {
                'description': 'Consumption of primary energy',
                'embedded': {
                    'max': 2100.0,
                    'min': 2100.0,
                    'significant_figures': 3,
                    'value': 2100.0,
                    'warnings': ['End of life is not included in the calculation']
                },
                'unit': 'MJ',
                'use': 'not implemented'
            }
        },
        'unit_weight': {
            'status': 'INPUT',
            'unit': 'kg',
            'value': 2.99
        },
        'units': {
            'status': 'INPUT',
            'value': 2
        }
    }
