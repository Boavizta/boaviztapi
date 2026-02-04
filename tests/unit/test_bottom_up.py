from boaviztapi.service.impacts_computation import compute_impacts
from pprint import pprint


def test_bottom_up_component_cpu_empty(empty_cpu_model):
    assert compute_impacts(
        empty_cpu_model, duration=empty_cpu_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.02042,
                "min": 0.0204,
                "value": 0.0204,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 80.85,
                "min": 9.652,
                "value": 14.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 1121.0,
                "min": 162.9,
                "value": 220.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
        },
    }


def test_bottom_up_component_cpu_complete(complete_cpu_model):
    assert compute_impacts(
        complete_cpu_model, duration=complete_cpu_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.04081,
                "min": 0.04081,
                "value": 0.04081,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 0.002544, "min": 0.0001264, "value": 0.0006},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 41.45,
                "min": 41.45,
                "value": 41.45,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 8620.0, "min": 220.3, "value": 3600.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 623.6,
                "min": 623.6,
                "value": 623.6,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {"max": 4484000.0, "min": 124.5, "value": 100000.0},
        },
    }


def test_bottom_up_component_cpu_incomplete(incomplete_cpu_model):
    assert compute_impacts(
        incomplete_cpu_model, duration=incomplete_cpu_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.0204,
                "min": 0.0204,
                "value": 0.0204,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 0.001272, "min": 6.321e-05, "value": 0.0003},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 18.69,
                "min": 18.69,
                "value": 18.69,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 4310.0, "min": 110.1, "value": 1800.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 284.5,
                "min": 284.5,
                "value": 284.5,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {"max": 2242000.0, "min": 62.25, "value": 100000.0},
        },
    }


def test_bottom_up_component_gpu_empty(empty_gpu_model):
    assert compute_impacts(
        empty_gpu_model,
        selected_criteria=["adp", "gwp", "pe"],
        duration=empty_gpu_model.usage.hours_life_time.value,
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {"max": 0.005826, "min": 0.005826, "value": 0.005826},
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {"max": 575.1, "min": 575.1, "value": 575.1},
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {"max": 7912.0, "min": 7912.0, "value": 7912.0},
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_gpu_complete(complete_gpu_model):
    assert compute_impacts(
        complete_gpu_model,
        selected_criteria=["adp", "gwp", "pe"],
        duration=complete_gpu_model.usage.hours_life_time.value,
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {"max": 0.005819, "min": 0.005819, "value": 0.005819},
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {"max": 238.6, "min": 238.6, "value": 238.6},
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {"max": 3424.0, "min": 3424.0, "value": 3424.0},
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_gpu_incomplete(incomplete_gpu_model):
    res = compute_impacts(
        incomplete_gpu_model,
        selected_criteria=["adp", "gwp", "pe"],
        duration=incomplete_gpu_model.usage.hours_life_time.value,
    )

    pprint(res)

    assert compute_impacts(
        incomplete_gpu_model,
        selected_criteria=["adp", "gwp", "pe"],
        duration=incomplete_gpu_model.usage.hours_life_time.value,
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {"max": 0.005818, "min": 0.005818, "value": 0.005818},
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {"max": 284.4, "min": 284.4, "value": 284.4},
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {"max": 4034.0, "min": 4034.0, "value": 4034.0},
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_ssd_empty(empty_ssd_model):
    assert compute_impacts(
        empty_ssd_model, duration=empty_ssd_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 3.151,
                "min": 0.006863,
                "value": 0.002,
                "warnings": [
                    "End of life is not included in the calculation",
                    "Uncertainty from technical characteristics is very "
                    "important. Results should be interpreted "
                    "with caution (see min and max values)",
                ],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 110000.0,
                "min": 226.3,
                "value": 50.0,
                "warnings": [
                    "End of life is not included in the calculation",
                    "Uncertainty from technical characteristics is very "
                    "important. Results should be interpreted "
                    "with caution (see min and max values)",
                ],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 1365000.0,
                "min": 2804.0,
                "value": 600.0,
                "warnings": [
                    "End of life is not included in the calculation",
                    "Uncertainty from technical characteristics is very "
                    "important. Results should be interpreted "
                    "with caution (see min and max values)",
                ],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_ssd_complete(complete_ssd_model):
    assert compute_impacts(
        complete_ssd_model, duration=complete_ssd_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.001061,
                "min": 0.001061,
                "value": 0.001061,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 23.73,
                "min": 23.73,
                "value": 23.73,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 289.8,
                "min": 289.8,
                "value": 289.8,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_ssd_incomplete(incomplete_ssd_model):
    assert compute_impacts(
        incomplete_ssd_model, duration=incomplete_ssd_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.00644,
                "min": 0.0006805,
                "value": 0.0017,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 211.6,
                "min": 10.44,
                "value": 50.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 2621.0,
                "min": 124.9,
                "value": 600.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_ram_empty(empty_ram_model):
    assert compute_impacts(
        empty_ram_model, duration=empty_ram_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.06469,
                "min": 0.001753,
                "value": 0.005,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 6.343e-05, "min": 3.153e-06, "value": 1.5e-05},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 2205.0,
                "min": 7.42,
                "value": 100.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 214.9, "min": 5.493, "value": 90.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 27370.0,
                "min": 101.3,
                "value": 1000.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {
                "max": 111800.0,
                "min": 3.105,
                "value": 3000.0,
                "warnings": [
                    "Uncertainty from technical characteristics is very important. "
                    "Results should be interpreted with caution (see "
                    "min and max values)"
                ],
            },
        },
    }


def test_bottom_up_component_ram_complete(complete_ram_model):
    assert compute_impacts(
        complete_ram_model, duration=complete_ram_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.0338,
                "min": 0.0338,
                "value": 0.0338,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 0.0007612, "min": 3.783e-05, "value": 0.00018},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 534.6,
                "min": 534.6,
                "value": 534.6,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 2579.0, "min": 65.92, "value": 1100.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 6745.0,
                "min": 6745.0,
                "value": 6745.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {
                "max": 1342000.0,
                "min": 37.26,
                "value": 40000.0,
                "warnings": [
                    "Uncertainty from technical characteristics is "
                    "very important. Results should be interpreted "
                    "with caution (see min and max values)"
                ],
            },
        },
    }


def test_bottom_up_component_ram_incomplete(incomplete_ram_model):
    assert compute_impacts(
        incomplete_ram_model, duration=incomplete_ram_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.1412,
                "min": 0.02149,
                "value": 0.06,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": {"max": 0.0007612, "min": 3.783e-05, "value": 0.00018},
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 4287.0,
                "min": 104.9,
                "value": 1400.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": {"max": 2579.0, "min": 65.92, "value": 1100.0},
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 53300.0,
                "min": 1412.0,
                "value": 18000.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": {
                "max": 1342000.0,
                "min": 37.26,
                "value": 40000.0,
                "warnings": [
                    "Uncertainty from technical characteristics is "
                    "very important. Results should be interpreted "
                    "with caution (see min and max values)"
                ],
            },
        },
    }


def test_bottom_up_component_power_supply_complete(complete_power_supply_model):
    assert compute_impacts(
        complete_power_supply_model,
        duration=complete_power_supply_model.usage.hours_life_time.value,
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.04963,
                "min": 0.04963,
                "value": 0.04963,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 145.3,
                "min": 145.3,
                "value": 145.3,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 2105.0,
                "min": 2105.0,
                "value": 2105.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_power_supply_empty(empty_power_supply_model):
    assert compute_impacts(
        empty_power_supply_model,
        duration=empty_power_supply_model.usage.hours_life_time.value,
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.0415,
                "min": 0.0083,
                "value": 0.025,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 121.5,
                "min": 24.3,
                "value": 73.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 1760.0,
                "min": 352.0,
                "value": 1100.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_hdd(hdd_model):
    assert compute_impacts(
        hdd_model, duration=hdd_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.00025,
                "min": 0.00025,
                "value": 0.00025,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 31.11,
                "min": 31.11,
                "value": 31.11,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 276.0,
                "min": 276.0,
                "value": 276.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_motherboard(motherboard_model):
    assert compute_impacts(
        motherboard_model, duration=motherboard_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.00369,
                "min": 0.00369,
                "value": 0.00369,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 66.1,
                "min": 66.1,
                "value": 66.1,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 836.0,
                "min": 836.0,
                "value": 836.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_empty_case(empty_case_model):
    assert compute_impacts(
        empty_case_model, duration=empty_case_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.02767,
                "min": 0.0202,
                "value": 0.0202,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 150.0,
                "min": 85.9,
                "value": 150.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 2200.0,
                "min": 1229.0,
                "value": 2200.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_blade_case(blade_case_model):
    assert compute_impacts(
        blade_case_model, duration=blade_case_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 0.02767,
                "min": 0.02767,
                "value": 0.02767,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 85.9,
                "min": 85.9,
                "value": 85.9,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 1229.0,
                "min": 1229.0,
                "value": 1229.0,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }


def test_bottom_up_component_assembly(assembly_model):
    assert compute_impacts(
        assembly_model, duration=assembly_model.usage.hours_life_time.value
    ) == {
        "adp": {
            "description": "Use of minerals and fossil ressources",
            "embedded": {
                "max": 1.41e-06,
                "min": 1.41e-06,
                "value": 1.41e-06,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgSbeq",
            "use": "not implemented",
        },
        "gwp": {
            "description": "Total climate change",
            "embedded": {
                "max": 6.68,
                "min": 6.68,
                "value": 6.68,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "kgCO2eq",
            "use": "not implemented",
        },
        "pe": {
            "description": "Consumption of primary energy",
            "embedded": {
                "max": 68.6,
                "min": 68.6,
                "value": 68.6,
                "warnings": ["End of life is not included in the calculation"],
            },
            "unit": "MJ",
            "use": "not implemented",
        },
    }
