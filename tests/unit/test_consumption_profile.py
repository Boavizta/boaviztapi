from typing import Dict, Union, List, Tuple

import pytest

from boaviztapi.dto.consumption_profile.consumption_profile import WorkloadPower
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel, RAMConsumptionProfileModel

MODEL_TEST_DATA_POINTS = [0., 25., 50., 75., 100.]

DEFAULT_CPU_PARAMS = {'a': 171.2, 'b': 0.0354, 'c': 36.89, 'd': -10.13}

ConsumptionProfileModel = Union[CPUConsumptionProfileModel, RAMConsumptionProfileModel]


def test_cpu_default():
    cpu_cp = CPUConsumptionProfileModel()
    model = cpu_cp.compute_consumption_profile_model()
    assert model == DEFAULT_CPU_PARAMS


@pytest.mark.parametrize('manufacturer,expected_model', [
    ('Intel', DEFAULT_CPU_PARAMS),
    ('AMD', DEFAULT_CPU_PARAMS)
])
def test_cpu_with_manufacturer_name(manufacturer: str, expected_model: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    model = cpu_cp.compute_consumption_profile_model(cpu_manufacturer=manufacturer)
    assert model == expected_model


def validate_models_approx(actual_model: ConsumptionProfileModel,
                           expected_model: ConsumptionProfileModel,
                           rel: float = 0.2):
    actual_results = list(map(actual_model.apply_consumption_profile, MODEL_TEST_DATA_POINTS))
    expected_results = list(map(expected_model.apply_consumption_profile, MODEL_TEST_DATA_POINTS))
    assert actual_results == pytest.approx(expected_results, rel=rel)


@pytest.mark.parametrize('model_range,expected_model_params', [
    ('Xeon Platinum', {'a': 171.1813, 'b': 0.0354, 'c': 36.8953, 'd': -10.1336}),
    ('Xeon Gold', {'a': 35.5688, 'b': 0.2438, 'c': 9.6694, 'd': -0.6087}),
    ('Xeon Silver', {'a': 20.7794, 'b': 0.3043, 'c': 8.4241, 'd': 0.8613})
])
def test_cpu_with_model_range(model_range: str, expected_model_params: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model)


@pytest.mark.parametrize('model_range,expected_model_params', [
    ('xeon gold', {'a': 35.5688, 'b': 0.2438, 'c': 9.6694, 'd': -0.6087}),
])
def test_cpu_with_model_range_fuzzy(model_range: str, expected_model_params: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model)


@pytest.mark.parametrize('manufacturer,model_range,expected_model_params', [
    ('Intel', 'Xeon Platinum', {'a': 171.1813, 'b': 0.0354, 'c': 36.8953, 'd': -10.1336}),
    ('Intel', 'Xeon Gold', {'a': 35.5688, 'b': 0.2438, 'c': 9.6694, 'd': -0.6087}),
    ('Intel', 'Xeon Silver', {'a': 20.7794, 'b': 0.3043, 'c': 8.4241, 'd': 0.8613})
])
def test_cpu_with_manufacture_and_model_range(
        manufacturer: str,
        model_range: str,
        expected_model_params: Dict[str, float]
):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model)


def validate_power_approx(actual_model: ConsumptionProfileModel, expected_workload_power: List[Tuple[float, float]]):
    for workload, expected_power in expected_workload_power:
        assert actual_model.apply_consumption_profile(workload) == pytest.approx(expected_power, rel=0.2)


@pytest.mark.parametrize('model_range,workload,expected_workload_power', [
    (
        # Xeon Platinum 8124M
        'Xeon Platinum',
        [
            WorkloadPower(load_percentage=0, power_watt=25.3),
            WorkloadPower(load_percentage=100, power_watt=211.8)
        ],
        [
            (0, 25.3), (10, 67.4), (50, 146.6), (100, 211.8)
        ]
    ),
    (
        # Xeon Platinum 8151
        'Xeon Platinum',
        [
            WorkloadPower(load_percentage=0, power_watt=24.0),
            WorkloadPower(load_percentage=50, power_watt=180.5)
        ],
        [
            (0, 24.0), (10, 74.0), (50, 180.5), (100, 220.5)
        ]
    ),
    (
        # Xeon Platinum 8175M
        'Xeon Platinum',
        [
            WorkloadPower(load_percentage=10, power_watt=73.3),
            WorkloadPower(load_percentage=50, power_watt=171.9),
            WorkloadPower(load_percentage=100, power_watt=239.5),
        ],
        [
            (0, 28.9), (10, 73.3), (50, 171.9), (100, 239.5)
        ]
    ),
    (
        # Xeon E5-2686 v4
        'Xeon E5',
        [
            WorkloadPower(load_percentage=0, power_watt=17.5),
            WorkloadPower(load_percentage=10, power_watt=49.9),
            WorkloadPower(load_percentage=50, power_watt=102.7),
        ],
        [
            (0, 17.5), (10, 49.9), (50, 102.7), (100, 140.6)
        ]
    ),
    (
        # Graviton (estimation)
        'Graviton',
        [
            WorkloadPower(load_percentage=0, power_watt=4.6),
            WorkloadPower(load_percentage=50, power_watt=30.1)
        ],
        [
            (0, 4.6), (10, 12.7), (50, 30.1), (100, 40.7)
        ]
    ),
    (
        # EPYC 7571 (estimation)
        '',
        [
            WorkloadPower(load_percentage=0, power_watt=23.2),
            WorkloadPower(load_percentage=100, power_watt=203.7)
        ],
        [
            (0, 23.2), (10, 63.7), (50, 150.5), (100, 203.7)
        ]
    ),
])
def test_cpu_with_model_range_and_workload(
        model_range: str,
        workload: WorkloadPower,
        expected_workload_power: List[Tuple[float, float]]
):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.workloads.set_input(workload)
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    validate_power_approx(cpu_cp, expected_workload_power)


@pytest.mark.parametrize('tdp,expected_model_params', [
    (240, {'a': 171.1813, 'b': 0.0354, 'c': 36.8953, 'd': -10.1336}),
    (85, {'a': 41.56, 'b': 0.2805, 'c': 8.424, 'd': 4.7644})
])
def test_cpu_with_tdp(tdp: int, expected_model_params: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_tdp=tdp)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model, rel=1)


@pytest.mark.parametrize('model_range,tdp,expected_model_params', [
    ('Xeon Platinum', 240, {'a': 171.1813, 'b': 0.0354, 'c': 36.8953, 'd': -10.1336}),
    ('Xeon Silver', 85, {'a': 20.7794, 'b': 0.3043, 'c': 8.424, 'd': 0.8613})
])
def test_cpu_with_tdp_and_model_range(model_range: str, tdp: int, expected_model_params: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range, cpu_tdp=tdp)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model, rel=1)


@pytest.mark.parametrize('capacity,expected_model_params', [
    (16, {'a': 4.544}),
    (128, {'a': 36.352}),
    (512, {'a': 145.408}),
])
def test_ram_with_capacity(capacity: int, expected_model_params: Dict[str, float]):
    ram_cp = RAMConsumptionProfileModel()
    ram_cp.compute_consumption_profile_model(capacity)
    expected_model = RAMConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(ram_cp, expected_model)
