from boaviztapi.service.bottom_up import bottom_up


def test_bottom_up_component_cpu_empty(empty_cpu_model):
    assert bottom_up(empty_cpu_model, duration=empty_cpu_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.02,
                                 'min': 0.02,
                                 'significant_figures': 2,
                                 'value': 0.02,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 0.0013,
                            'min': 6.3e-05,
                            'significant_figures': 2,
                            'value': 0.00031}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 22.7,
                                 'min': 11.1,
                                 'significant_figures': 3,
                                 'value': 21.7,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 4300.0,
                            'min': 110.0,
                            'significant_figures': 2,
                            'value': 1800.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 339.0,
                                'min': 182.0,
                                'significant_figures': 3,
                                'value': 325.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 2200000.0,
                           'min': 62.0,
                           'significant_figures': 2,
                           'value': 62000.0}}}


def test_bottom_up_component_cpu_complete(complete_cpu_model):
    assert bottom_up(complete_cpu_model, duration=complete_cpu_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.041,
                                 'min': 0.041,
                                 'significant_figures': 2,
                                 'value': 0.041,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 0.0025,
                            'min': 0.00013,
                            'significant_figures': 2,
                            'value': 0.00061}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 43.4,
                                 'min': 43.4,
                                 'significant_figures': 3,
                                 'value': 43.4,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 8600.0,
                            'min': 220.0,
                            'significant_figures': 2,
                            'value': 3600.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 650.0,
                                'min': 650.0,
                                'significant_figures': 3,
                                'value': 650.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 4500000.0,
                           'min': 120.0,
                           'significant_figures': 2,
                           'value': 120000.0}}}


def test_bottom_up_component_cpu_incomplete(incomplete_cpu_model):
    assert bottom_up(incomplete_cpu_model, duration=incomplete_cpu_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.02,
                                 'min': 0.02,
                                 'significant_figures': 2,
                                 'value': 0.02,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 0.0013,
                            'min': 6.3e-05,
                            'significant_figures': 2,
                            'value': 0.00031}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 19.7,
                                 'min': 19.7,
                                 'significant_figures': 3,
                                 'value': 19.7,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 4300.0,
                            'min': 110.0,
                            'significant_figures': 2,
                            'value': 1800.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 297.0,
                                'min': 297.0,
                                'significant_figures': 3,
                                'value': 297.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 2200000.0,
                           'min': 62.0,
                           'significant_figures': 2,
                           'value': 62000.0}}}


def test_bottom_up_component_ssd_empty(empty_ssd_model):
    assert bottom_up(empty_ssd_model, duration=empty_ssd_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 3.2,
                                 'min': 0.0069,
                                 'significant_figures': 2,
                                 'value': 0.0019},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 110000.0,
                                 'min': 230.0,
                                 'significant_figures': 2,
                                 'value': 52.0},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 1370000.0,
                                'min': 2810.0,
                                'significant_figures': 3,
                                'value': 640.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_ssd_complete(complete_ssd_model):
    assert bottom_up(complete_ssd_model, duration=complete_ssd_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.0011,
                                 'min': 0.0011,
                                 'significant_figures': 2,
                                 'value': 0.0011},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 24.0,
                                 'min': 24.0,
                                 'significant_figures': 2,
                                 'value': 24.0},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 293.0,
                                'min': 293.0,
                                'significant_figures': 3,
                                'value': 293.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_ssd_incomplete(incomplete_ssd_model):
    assert bottom_up(incomplete_ssd_model, duration=incomplete_ssd_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.0064,
                                 'min': 0.00068,
                                 'significant_figures': 2,
                                 'value': 0.0017},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 210.0,
                                 'min': 10.0,
                                 'significant_figures': 2,
                                 'value': 47.0},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 2620.0,
                                'min': 128.0,
                                'significant_figures': 3,
                                'value': 586.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_ram_empty(empty_ram_model):
    assert bottom_up(empty_ram_model, duration=empty_ram_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.065,
                                 'min': 0.0018,
                                 'significant_figures': 2,
                                 'value': 0.0049,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 6.3e-05,
                            'min': 3.2e-06,
                            'significant_figures': 2,
                            'value': 1.5e-05}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 2200.0,
                                 'min': 7.4,
                                 'significant_figures': 2,
                                 'value': 120.0,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 210.0,
                            'min': 5.5,
                            'significant_figures': 2,
                            'value': 91.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 27000.0,
                                'min': 100.0,
                                'significant_figures': 2,
                                'value': 1500.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 110000.0,
                           'min': 3.1,
                           'significant_figures': 2,
                           'value': 3100.0}}}


def test_bottom_up_component_ram_complete(complete_ram_model):
    assert bottom_up(complete_ram_model, duration=complete_ram_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.034,
                                 'min': 0.034,
                                 'significant_figures': 2,
                                 'value': 0.034,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 0.00076,
                            'min': 3.8e-05,
                            'significant_figures': 2,
                            'value': 0.00018}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 530.0,
                                 'min': 530.0,
                                 'significant_figures': 2,
                                 'value': 530.0,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 2600.0,
                            'min': 66.0,
                            'significant_figures': 2,
                            'value': 1100.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 6700.0,
                                'min': 6700.0,
                                'significant_figures': 2,
                                'value': 6700.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 1300000.0,
                           'min': 37.0,
                           'significant_figures': 2,
                           'value': 37000.0}}}


def test_bottom_up_component_ram_incomplete(incomplete_ram_model):
    assert bottom_up(incomplete_ram_model, duration=incomplete_ram_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'max': 0.14,
                                 'min': 0.021,
                                 'significant_figures': 2,
                                 'value': 0.059,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgSbeq',
                    'use': {'max': 0.00076,
                            'min': 3.8e-05,
                            'significant_figures': 2,
                            'value': 0.00018}},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'max': 4300.0,
                                 'min': 100.0,
                                 'significant_figures': 2,
                                 'value': 1400.0,
                                 'warnings': ['End of life is not included in the '
                                              'calculation']},
                    'unit': 'kgCO2eq',
                    'use': {'max': 2600.0,
                            'min': 66.0,
                            'significant_figures': 2,
                            'value': 1100.0}},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'max': 53000.0,
                                'min': 1400.0,
                                'significant_figures': 2,
                                'value': 18000.0,
                                'warnings': ['End of life is not included in the '
                                             'calculation']},
                   'unit': 'MJ',
                   'use': {'max': 1300000.0,
                           'min': 37.0,
                           'significant_figures': 2,
                           'value': 37000.0}}}


def test_bottom_up_component_power_supply_complete(complete_power_supply_model):
    assert bottom_up(complete_power_supply_model, duration=complete_power_supply_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.05,
                                 'min': 0.05,
                                 'significant_figures': 2,
                                 'value': 0.05},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 145.0,
                                 'min': 145.0,
                                 'significant_figures': 3,
                                 'value': 145.0},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 2100.0,
                                'min': 2100.0,
                                'significant_figures': 3,
                                'value': 2100.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_power_supply_empty(empty_power_supply_model):
    assert bottom_up(empty_power_supply_model, duration=empty_power_supply_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.042,
                                 'min': 0.0083,
                                 'significant_figures': 2,
                                 'value': 0.025},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 122.0,
                                 'min': 24.3,
                                 'significant_figures': 3,
                                 'value': 72.7},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 1760.0,
                                'min': 352.0,
                                'significant_figures': 3,
                                'value': 1050.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_hdd(hdd_model):
    assert bottom_up(hdd_model, duration=hdd_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.00025,
                                 'min': 0.00025,
                                 'significant_figures': 2,
                                 'value': 0.00025},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 31.1,
                                 'min': 31.1,
                                 'significant_figures': 3,
                                 'value': 31.1},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 276.0,
                                'min': 276.0,
                                'significant_figures': 3,
                                'value': 276.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_motherboard(motherboard_model):
    assert bottom_up(motherboard_model, duration=motherboard_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.00369,
                                 'min': 0.00369,
                                 'significant_figures': 3,
                                 'value': 0.00369},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 66.1,
                                 'min': 66.1,
                                 'significant_figures': 3,
                                 'value': 66.1},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 836.0,
                                'min': 836.0,
                                'significant_figures': 3,
                                'value': 836.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_empty_case(empty_case_model):
    assert bottom_up(empty_case_model, duration=empty_case_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.0277,
                                 'min': 0.0202,
                                 'significant_figures': 3,
                                 'value': 0.0202},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 150.0,
                                 'min': 85.9,
                                 'significant_figures': 3,
                                 'value': 150.0},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 2200.0,
                                'min': 1229.0,
                                'significant_figures': 4,
                                'value': 2200.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_blade_case(blade_case_model):
    assert bottom_up(blade_case_model, duration=blade_case_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 0.0277,
                                 'min': 0.0277,
                                 'significant_figures': 3,
                                 'value': 0.0277},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 85.9,
                                 'min': 85.9,
                                 'significant_figures': 3,
                                 'value': 85.9},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 1230.0,
                                'min': 1230.0,
                                'significant_figures': 3,
                                'value': 1230.0},
                   'unit': 'MJ',
                   'use': 'not implemented'}}


def test_bottom_up_component_assembly(assembly_model):
    assert bottom_up(assembly_model, duration=assembly_model.usage.hours_life_time.value) == \
           {'adp': {'description': 'Use of minerals and fossil ressources',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 1.41e-06,
                                 'min': 1.41e-06,
                                 'significant_figures': 3,
                                 'value': 1.41e-06},
                    'unit': 'kgSbeq',
                    'use': 'not implemented'},
            'gwp': {'description': 'Total climate change',
                    'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 6.68,
                                 'min': 6.68,
                                 'significant_figures': 3,
                                 'value': 6.68},
                    'unit': 'kgCO2eq',
                    'use': 'not implemented'},
            'pe': {'description': 'Consumption of primary energy',
                   'embedded': {'warnings': ['End of life is not included in the calculation'], 'max': 68.6,
                                'min': 68.6,
                                'significant_figures': 3,
                                'value': 68.6},
                   'unit': 'MJ',
                   'use': 'not implemented'}}
