from typing import Dict

import pytest

from boaviztapi.dto.consumption_profile.consumption_profile import WorkloadPower
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel

MODEL_TEST_DATA_POINTS = [0., 25., 50., 75., 100.]

DEFAULT_CPU_PARAMS = {'a': 342.4, 'b': 0.0347, 'c': 36.89, 'd': -16.40}


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


def validate_models_approx(actual_model: CPUConsumptionProfileModel, expected_model: CPUConsumptionProfileModel):
    actual_results = list(map(actual_model.apply_consumption_profile, MODEL_TEST_DATA_POINTS))
    expected_results = list(map(expected_model.apply_consumption_profile, MODEL_TEST_DATA_POINTS))
    assert actual_results == pytest.approx(expected_results, rel=10e-1)


@pytest.mark.parametrize('model_range,expected_model_params', [
    ('xeon platinum', {'a': 342.36, 'b': 0.0347, 'c': 36.89, 'd': -16.40}),
    ('xeon gold', {'a': 71.13, 'b': 0.2280, 'c': 9.66, 'd': 6.26}),
    ('xeon silver', {'a': 41.55, 'b': 0.2805, 'c': 8.42, 'd': 4.76})
])
def test_cpu_with_model_range(model_range: str, expected_model_params: Dict[str, float]):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model)


@pytest.mark.parametrize('manufacturer,model_range,expected_model_params', [
    ('intel', 'xeon platinum', {'a': 342.36, 'b': 0.0347, 'c': 36.89, 'd': -16.40}),
    ('intel', 'xeon gold', {'a': 71.13, 'b': 0.2280, 'c': 9.66, 'd': 6.26}),
    ('intel', 'xeon silver', {'a': 41.55, 'b': 0.2805, 'c': 8.42, 'd': 4.76})
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


@pytest.mark.parametrize('model_range,workload,expected_model_params', [
    (
            'xeon platinum',
            [
                WorkloadPower(load_percentage=0, power_watt=58),
                WorkloadPower(load_percentage=100, power_watt=618)
            ],
            {'a': 342.36, 'b': 0.0347, 'c': 36.89, 'd': -16.40}
    ),
    (
            'xeon platinum',
            [
                WorkloadPower(load_percentage=50, power_watt=448)
            ],
            {'a': 342.36, 'b': 0.0347, 'c': 36.89, 'd': -16.40}
    ),
    (
            'xeon platinum',
            [
                WorkloadPower(load_percentage=10, power_watt=176),
                WorkloadPower(load_percentage=20, power_watt=241),
                WorkloadPower(load_percentage=90, power_watt=607)
            ],
            {'a': 342.36, 'b': 0.0347, 'c': 36.89, 'd': -16.40}
    ),
    (
            'xeon silver',
            [
                WorkloadPower(load_percentage=30, power_watt=96),
                WorkloadPower(load_percentage=80, power_watt=130)
            ],
            {'a': 41.55, 'b': 0.2805, 'c': 8.42, 'd': 4.76}
    ),
])
def test_cpu_with_model_range_and_workload(
        model_range: str,
        workload: WorkloadPower,
        expected_model_params: Dict[str, float]
):
    cpu_cp = CPUConsumptionProfileModel()
    cpu_cp.compute_consumption_profile_model(cpu_model_range=model_range)
    expected_model = CPUConsumptionProfileModel()
    expected_model.params.value = expected_model_params
    validate_models_approx(cpu_cp, expected_model)
