from boaviztapi.service.bottom_up import bottom_up_component


def test_bottom_up_component_cpu_empty(empty_cpu):
    assert bottom_up_component(empty_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 21.7, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 325.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_cpu_complete(complete_cpu):
    assert bottom_up_component(complete_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 15.9, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 247.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_cpu_incomplete(incomplete_cpu):
    assert bottom_up_component(incomplete_cpu) == {
        'adp': {'manufacture': 0.02, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 21.7, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 325.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ssd_empty(empty_ssd):
    assert bottom_up_component(empty_ssd) == {
        'adp': {'manufacture': 0.0019, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 52.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 640.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ssd_complete(complete_ssd):
    assert bottom_up_component(complete_ssd) == {
        'adp': {'manufacture': 0.0011, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 24.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 293.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ssd_incomplete(incomplete_ssd):
    assert bottom_up_component(incomplete_ssd) == {
        'adp': {'manufacture': 0.0017, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 47.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 586.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ram_empty(empty_ram):
    assert bottom_up_component(empty_ram) == {
        'adp': {'manufacture': 0.0049, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 120.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 1500.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ram_complete(complete_ram):
    assert bottom_up_component(complete_ram) == {
        'adp': {'manufacture': 0.0028, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 45.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 560.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ram_incomplete(incomplete_ram):
    assert bottom_up_component(incomplete_ram) == {
        'adp': {'manufacture': 0.0049, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 120.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 1500.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_power_supply_complete(complete_power_supply):
    assert bottom_up_component(complete_power_supply) == {
        'adp': {'manufacture': 0.0166, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 48.6, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 704.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_power_supply_empty(empty_power_supply):
    assert bottom_up_component(empty_power_supply) == {
        'adp': {'manufacture': 0.0248, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 72.66, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 1050.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_hdd(hdd):
    assert bottom_up_component(hdd) == {
        'adp': {'manufacture': 0.00025, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 31.1, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 276.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_motherboard(motherboard):
    assert bottom_up_component(motherboard) == {
        'adp': {'manufacture': 0.00369, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 66.1, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 836.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_empty_case(empty_case):
    assert bottom_up_component(empty_case) == {
        'adp': {'manufacture': 0.0202, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 150.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 2200.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_blade_case(blade_case):
    assert bottom_up_component(blade_case) == {
        'adp': {'manufacture': 0.0277, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 85.9, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 1230.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_assembly(assembly):
    assert bottom_up_component(assembly) == {
        'adp': {'manufacture': 1.41e-06, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 6.68, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 68.6, 'use': 'not implemented', "unit": "MJ"}}
