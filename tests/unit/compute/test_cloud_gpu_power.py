"""GPU power is part of a cloud instance's use phase, allocated by GPU count.

Before this, the instance power model only covered CPU, RAM and disks, so GPU
instances got no electricity for their GPUs at all.
"""

import pytest
from pydantic import ValidationError

from boaviztapi.data.archetype import get_cloud_instance_archetype
from boaviztapi.dto.device.device import Cloud, mapper_cloud_instance
from boaviztapi.dto.usage.usage import UsageCloud
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component.gpu import IDLE_POWER_RATIO
from boaviztapi.models.services.cloud_instance import ServiceCloudInstance


def instance(instance_type, provider="aws", gpu_units=None):
    cloud_instance = ServiceCloudInstance(
        archetype=get_cloud_instance_archetype(instance_type, provider)
    )
    if gpu_units is not None:
        cloud_instance.gpu_units = Boattribute(default=gpu_units)
    return cloud_instance


def test_gpu_power_added_by_gpu_units():
    with_gpu = instance("g5.xlarge")
    without_gpu = instance("g5.xlarge", gpu_units=0)

    power = with_gpu.model_power_consumption().value
    gpu_power = with_gpu.platform.gpu.usage.avg_power.value

    assert gpu_power > 0
    assert power == pytest.approx(
        without_gpu.model_power_consumption().value
        + with_gpu.gpu_units.value * gpu_power
    )


def test_fractional_gpu_units_get_a_fraction_of_the_gpu_power():
    without_gpu = instance("g5.xlarge", gpu_units=0).model_power_consumption().value
    one_gpu = instance("g5.xlarge").model_power_consumption().value
    eighth = instance("g5.xlarge", gpu_units=0.125).model_power_consumption().value

    assert eighth - without_gpu == pytest.approx((one_gpu - without_gpu) / 8)


def test_instance_without_gpu_is_unaffected():
    no_gpu = instance("a1.4xlarge")
    assert no_gpu.platform.gpu is None
    assert no_gpu.gpu_allocation() == 0
    assert no_gpu.model_power_consumption().value > 0


def test_gpu_time_workload_sets_gpu_load_only():
    cloud_instance = mapper_cloud_instance(
        Cloud(
            provider="aws",
            instance_type="g5.xlarge",
            usage=UsageCloud(time_workload=80, gpu_time_workload=0),
        ),
        archetype=get_cloud_instance_archetype("g5.xlarge", "aws"),
    )
    cloud_instance.model_power_consumption()

    gpu = cloud_instance.platform.gpu
    # Idle GPU: 10% of its TDP
    assert gpu.usage.avg_power.value == pytest.approx(IDLE_POWER_RATIO * gpu.tdp.value)
    assert cloud_instance.platform.cpu.usage.time_workload.value == 80


def test_gpu_load_does_not_follow_time_workload():
    """time_workload is the CPU load; the GPU keeps its own 65% default."""
    cloud_instance = mapper_cloud_instance(
        Cloud(
            provider="aws",
            instance_type="g5.xlarge",
            usage=UsageCloud(time_workload=100),
        ),
        archetype=get_cloud_instance_archetype("g5.xlarge", "aws"),
    )
    cloud_instance.model_power_consumption()

    gpu = cloud_instance.platform.gpu
    assert gpu.usage.time_workload.value == 65
    assert cloud_instance.platform.cpu.usage.time_workload.value == 100
    assert gpu.usage.avg_power.value == pytest.approx(
        gpu.tdp.value
        / gpu.gpus_per_card.value
        * (IDLE_POWER_RATIO + (1 - IDLE_POWER_RATIO) * 0.65)
    )


def test_given_gpu_avg_power_is_not_modelled():
    without_gpu = instance("g5.xlarge", gpu_units=0).model_power_consumption().value
    with_gpu = instance("g5.xlarge")
    with_gpu.platform.gpu.usage.avg_power.set_input(100)

    assert with_gpu.model_power_consumption().value == pytest.approx(
        without_gpu + with_gpu.gpu_units.value * 100
    )
    assert with_gpu.platform.gpu.usage.avg_power.value == 100


@pytest.mark.parametrize("gpu_time_workload", [-1, 101])
def test_gpu_time_workload_out_of_range_is_rejected(gpu_time_workload):
    with pytest.raises(ValidationError):
        UsageCloud(gpu_time_workload=gpu_time_workload)
