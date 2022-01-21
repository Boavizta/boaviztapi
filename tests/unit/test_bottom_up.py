from boaviztapi.service.bottom_up import bottom_up_component


def test_bottom_up_component_cpu_empty(empty_cpu):
    assert bottom_up_component(empty_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented'},
        'gwp': {'manufacture': 22.0, 'use': 'not implemented'},
        'pe': {'manufacture': 325.0, 'use': 'not implemented'}}


def test_bottom_up_component_cpu_complete(complete_cpu):
    assert bottom_up_component(complete_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented'},
        'gwp': {'manufacture': 16.0, 'use': 'not implemented'},
        'pe': {'manufacture': 247.0, 'use': 'not implemented'}}


def test_bottom_up_component_cpu_incomplete(incomplete_cpu):
    assert bottom_up_component(incomplete_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented'},
        'gwp': {'manufacture': 22.0, 'use': 'not implemented'},
        'pe': {'manufacture': 325.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_ssd_empty(empty_ssd):
    assert bottom_up_component(empty_ssd) == {
        'adp': {'manufacture': 0.002, 'use': 'not implemented'},
        'gwp': {'manufacture': 52.0, 'use': 'not implemented'},
        'pe': {'manufacture': 640.0, 'use': 'not implemented'}}


def test_bottom_up_component_ssd_complete(complete_ssd):
    assert bottom_up_component(complete_ssd) == {
        'adp': {'manufacture': 0.001, 'use': 'not implemented'},
        'gwp': {'manufacture': 24.0, 'use': 'not implemented'},
        'pe': {'manufacture': 293.0, 'use': 'not implemented'}}


def test_bottom_up_component_ssd_incomplete(incomplete_ssd):
    assert bottom_up_component(incomplete_ssd) == {
        'adp': {'manufacture': 0.002, 'use': 'not implemented'},
        'gwp': {'manufacture': 47.0, 'use': 'not implemented'},
        'pe': {'manufacture': 586.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_ram_empty(empty_ram):
    assert bottom_up_component(empty_ram) == {
        'adp': {'manufacture': 0.005, 'use': 'not implemented'},
        'gwp': {'manufacture': 118.0, 'use': 'not implemented'},
        'pe': {'manufacture': 1472.0, 'use': 'not implemented'}}


def test_bottom_up_component_ram_complete(complete_ram):
    assert bottom_up_component(complete_ram) == {
        'adp': {'manufacture': 0.003, 'use': 'not implemented'},
        'gwp': {'manufacture': 45.0, 'use': 'not implemented'},
        'pe': {'manufacture': 562.0, 'use': 'not implemented'}}


def test_bottom_up_component_ram_incomplete(incomplete_ram):
    assert bottom_up_component(incomplete_ram) == {
        'adp': {'manufacture': 0.005, 'use': 'not implemented'},
        'gwp': {'manufacture': 118.0, 'use': 'not implemented'},
        'pe': {'manufacture': 1472.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_power_supply_complete(complete_power_supply):
    assert bottom_up_component(complete_power_supply) == {
        'adp': {'manufacture': 0.017, 'use': 'not implemented'},
        'gwp': {'manufacture': 49.0, 'use': 'not implemented'},
        'pe': {'manufacture': 704.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_power_supply_empty(empty_power_supply):
    assert bottom_up_component(empty_power_supply) == {
        'adp': {'manufacture': 0.025, 'use': 'not implemented'},
        'gwp': {'manufacture': 73.0, 'use': 'not implemented'},
        'pe': {'manufacture': 1052.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_hdd(hdd):
    assert bottom_up_component(hdd) == {
        'adp': {'manufacture': 0.0, 'use': 'not implemented'},
        'gwp': {'manufacture': 31.0, 'use': 'not implemented'},
        'pe': {'manufacture': 276.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_motherboard(motherboard):
    assert bottom_up_component(motherboard) == {
        'adp': {'manufacture': 0.004, 'use': 'not implemented'},
        'gwp': {'manufacture': 66.0, 'use': 'not implemented'},
        'pe': {'manufacture': 836.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_empty_case(empty_case):
    assert bottom_up_component(empty_case) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented'},
        'gwp': {'manufacture': 150.0, 'use': 'not implemented'},
        'pe': {'manufacture': 2200.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_blade_case(blade_case):
    assert bottom_up_component(blade_case) == {
        'adp': {'manufacture': 0.028, 'use': 'not implemented'},
        'gwp': {'manufacture': 86.0, 'use': 'not implemented'},
        'pe': {'manufacture': 1229.0, 'use': 'not implemented'}
    }


def test_bottom_up_component_assembly(assembly):
    assert bottom_up_component(assembly) == {
        'adp': {'manufacture': 0.0, 'use': 'not implemented'},
        'gwp': {'manufacture': 7.0, 'use': 'not implemented'},
        'pe': {'manufacture': 69.0, 'use': 'not implemented'}
    }
