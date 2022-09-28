from boaviztapi.service.verbose import verbose_component, verbose_device


def test_verbose_component_cpu_1(complete_cpu_model):
    verbose = verbose_component(complete_cpu_model)
    print(verbose)
    assert verbose["core_units"] == {'source': None, 'status': 'INPUT', 'unit': 'none', 'value': 24}
    assert verbose["die_size_per_core"] == {'source': None, 'status': 'INPUT', 'unit': 'mm2', 'value': 0.245}

    assert verbose["manufacture_impacts"] == {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                              'gwp': {'unit': 'kgCO2eq', 'value': 21.7},
                                              'pe': {'unit': 'MJ', 'value': 325.0}}


def test_verbose_component_cpu_2(incomplete_cpu_model):
    verbose = verbose_component(incomplete_cpu_model)
    assert verbose["core_units"] == {'source': None, 'status': 'INPUT', 'unit': 'none', 'value': 12}
    assert verbose["family"] == {'source': None, 'status': 'INPUT', 'unit': 'none', 'value': 'Skylake'}
    assert verbose["manufacture_impacts"] == {'adp': {'unit': 'kgSbeq', 'value': 0.02},
                                              'gwp': {'unit': 'kgCO2eq', 'value': 19.7},
                                              'pe': {'unit': 'MJ', 'value': 297.0}}


def test_verbose_component_ram(complete_ram_model):
    verbose = verbose_component(complete_ram_model)

    assert verbose["manufacture_impacts"] == {
        'adp': {'unit': 'kgSbeq', 'value': 0.0028},
        'gwp': {'unit': 'kgCO2eq', 'value': 45.0},
        'pe': {'unit': 'MJ', 'value': 560.0}}

    assert verbose["capacity"] == {'source': None, 'status': 'INPUT', 'unit': 'GB', 'value': 32}
    assert verbose["density"] == {'source': None, 'status': 'INPUT', 'unit': 'GB/cm2', 'value': 1.79}


def test_verbose_component_ssd(empty_ssd_model):
    assert verbose_component(empty_ssd_model) == {
        'capacity': {'source': None, 'status': 'DEFAULT', 'unit': 'GB', 'value': 1000},
        'density': {'source': None,
                    'status': 'DEFAULT',
                    'unit': 'GB/cm2',
                    'value': 48.5},
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0019},
                                'gwp': {'unit': 'kgCO2eq', 'value': 52.0},
                                'pe': {'unit': 'MJ', 'value': 640.0}},
        'units': 1}


def test_verbose_component_power_supply(empty_power_supply_model):
    assert verbose_component(empty_power_supply_model) == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.025},
                                'gwp': {'unit': 'kgCO2eq', 'value': 72.7},
                                'pe': {'unit': 'MJ', 'value': 1050.0}},
        'unit_weight': {'source': None,
                        'status': 'DEFAULT',
                        'unit': 'kg',
                        'value': 2.99},
        'units': 1}


def test_verbose_component_case(blade_case_model):
    assert verbose_component(blade_case_model) == {
        'case_type': {'source': None,
                      'status': 'INPUT',
                      'unit': 'none',
                      'value': 'blade'},
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0277},
                                'gwp': {'unit': 'kgCO2eq', 'value': 85.9},
                                'pe': {'unit': 'MJ', 'value': 1230.0}},
        'units': 1}


def test_verbose_device_server_1(incomplete_server_model):
    verbose = verbose_device(incomplete_server_model)

    assert verbose["ASSEMBLY-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 1.41e-06},
                                'gwp': {'unit': 'kgCO2eq', 'value': 6.68},
                                'pe': {'unit': 'MJ', 'value': 68.6}},
        'units': 1}
    assert verbose["CASE-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0202},
                                'gwp': {'unit': 'kgCO2eq', 'value': 150.0},
                                'pe': {'unit': 'MJ', 'value': 2200.0}},
        'units': 1}

    assert verbose["MOTHERBOARD-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.00369},
                                'gwp': {'unit': 'kgCO2eq', 'value': 66.1},
                                'pe': {'unit': 'MJ', 'value': 836.0}},
        'units': 1}

    assert verbose["POWER_SUPPLY-1"] == {'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.025},
                                                                 'gwp': {'unit': 'kgCO2eq', 'value': 72.7},
                                                                 'pe': {'unit': 'MJ', 'value': 1050.0}},
                                         'unit_weight': {'source': None,
                                                         'status': 'DEFAULT',
                                                         'unit': 'kg',
                                                         'value': 2.99},
                                         'units': 2}


def test_verbose_device_server_2(dell_r740_model):
    verbose = verbose_device(dell_r740_model)
    assert verbose["ASSEMBLY-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 1.41e-06},
                                'gwp': {'unit': 'kgCO2eq', 'value': 6.68},
                                'pe': {'unit': 'MJ', 'value': 68.6}},
        'units': 1}
    assert verbose["CASE-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.0202},
                                'gwp': {'unit': 'kgCO2eq', 'value': 150.0},
                                'pe': {'unit': 'MJ', 'value': 2200.0}},
        'units': 1}

    assert verbose["MOTHERBOARD-1"] == {
        'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.00369},
                                'gwp': {'unit': 'kgCO2eq', 'value': 66.1},
                                'pe': {'unit': 'MJ', 'value': 836.0}},
        'units': 1}

    assert verbose["POWER_SUPPLY-1"] == {'manufacture_impacts': {'adp': {'unit': 'kgSbeq', 'value': 0.025},
                                                                 'gwp': {'unit': 'kgCO2eq', 'value': 72.7},
                                                                 'pe': {'unit': 'MJ', 'value': 1050.0}},
                                         'unit_weight': {'source': None,
                                                         'status': 'INPUT',
                                                         'unit': 'kg',
                                                         'value': 2.99},
                                         'units': 2}
