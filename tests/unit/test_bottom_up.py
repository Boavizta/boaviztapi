from boaviztapi.service.allocation import Allocation
from boaviztapi.service.bottom_up import bottom_up_component


def test_bottom_up_component_cpu_empty(empty_cpu_model):
    assert bottom_up_component(empty_cpu_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
        'gwp': {'manufacture': 21.7, 'unit': 'kgCO2eq', 'use': 610.0},
        'pe': {'manufacture': 325.0, 'unit': 'MJ', 'use': 20550.0}}


def test_bottom_up_component_cpu_complete(complete_cpu_model):
    assert bottom_up_component(complete_cpu_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.041, 'unit': 'kgSbeq', 'use': 0.000205},
        'gwp': {'manufacture': 43.4, 'unit': 'kgCO2eq', 'use': 1200.0},
        'pe': {'manufacture': 650.0, 'unit': 'MJ', 'use': 41100.0}}


def test_bottom_up_component_cpu_incomplete(incomplete_cpu_model):
    assert bottom_up_component(incomplete_cpu_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.02, 'unit': 'kgSbeq', 'use': 0.000102},
        'gwp': {'manufacture': 19.7, 'unit': 'kgCO2eq', 'use': 610.0},
        'pe': {'manufacture': 297.0, 'unit': 'MJ', 'use': 20550.0}}


def test_bottom_up_component_ssd_empty(empty_ssd_model):
    assert bottom_up_component(empty_ssd_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0019, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 52.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 640.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ssd_complete(complete_ssd_model):
    assert bottom_up_component(complete_ssd_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0011, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 24.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 293.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ssd_incomplete(incomplete_ssd_model):
    assert bottom_up_component(incomplete_ssd_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0017, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 47.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 586.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_ram_empty(empty_ram_model):
    assert bottom_up_component(empty_ram_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0049, 'unit': 'kgSbeq', 'use': 5.11e-06},
        'gwp': {'manufacture': 120.0, 'unit': 'kgCO2eq', 'use': 30.0},
        'pe': {'manufacture': 1500.0, 'unit': 'MJ', 'use': 1025.0}}


def test_bottom_up_component_ram_complete(complete_ram_model):
    assert bottom_up_component(complete_ram_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.034, 'unit': 'kgSbeq', 'use': 6.13e-05},
        'gwp': {'manufacture': 530.0, 'unit': 'kgCO2eq', 'use': 360.0},
        'pe': {'manufacture': 6700.0, 'unit': 'MJ', 'use': 12300.0}}


def test_bottom_up_component_ram_incomplete(incomplete_ram_model):
    assert bottom_up_component(incomplete_ram_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.059, 'unit': 'kgSbeq', 'use': 6.13e-05},
        'gwp': {'manufacture': 1400.0, 'unit': 'kgCO2eq', 'use': 360.0},
        'pe': {'manufacture': 18000.0, 'unit': 'MJ', 'use': 12300.0}}


def test_bottom_up_component_power_supply_complete(complete_power_supply_model):
    assert bottom_up_component(complete_power_supply_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.05, 'unit': 'kgSbeq', 'use': 'not implemented'},
        'gwp': {'manufacture': 145.0, 'unit': 'kgCO2eq', 'use': 'not implemented'},
        'pe': {'manufacture': 2100.0, 'unit': 'MJ', 'use': 'not implemented'}}


def test_bottom_up_component_power_supply_empty(empty_power_supply_model):
    assert bottom_up_component(empty_power_supply_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.025, 'unit': 'kgSbeq', 'use': 'not implemented'},
        'gwp': {'manufacture': 72.7, 'unit': 'kgCO2eq', 'use': 'not implemented'},
        'pe': {'manufacture': 1050.0, 'unit': 'MJ', 'use': 'not implemented'}}


def test_bottom_up_component_hdd(hdd_model):
    assert bottom_up_component(hdd_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.00025, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 31.1, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 276.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_motherboard(motherboard_model):
    assert bottom_up_component(motherboard_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.00369, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 66.1, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 836.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_empty_case(empty_case_model):
    assert bottom_up_component(empty_case_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0202, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 150.0, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 2200.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_blade_case(blade_case_model):
    assert bottom_up_component(blade_case_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 0.0277, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 85.9, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 1230.0, 'use': 'not implemented', "unit": "MJ"}}


def test_bottom_up_component_assembly(assembly_model):
    assert bottom_up_component(assembly_model, allocation=Allocation.TOTAL) == {
        'adp': {'manufacture': 1.41e-06, 'use': 'not implemented', "unit": "kgSbeq"},
        'gwp': {'manufacture': 6.68, 'use': 'not implemented', "unit": "kgCO2eq"},
        'pe': {'manufacture': 68.6, 'use': 'not implemented', "unit": "MJ"}}
