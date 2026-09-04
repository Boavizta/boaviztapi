"""GPU embodied impacts are allocated to a cloud instance by its GPU count.

Before this, every component that was not RAM/SSD/HDD fell through to a vCPU
prorata, so a GPU instance was billed a share of the host's GPUs proportional
to its vCPUs rather than to the GPUs it actually gets. See issue #563.
"""

import pytest

from boaviztapi.compute.impacts_computation import compute_single_impact
from boaviztapi.data.archetype import (
    get_cloud_instance_archetype,
    get_server_archetype,
)
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.device.server import DeviceServer
from boaviztapi.models.services.cloud_instance import ServiceCloudInstance

DURATION = 8760


def instance(instance_type, provider="aws"):
    return ServiceCloudInstance(
        archetype=get_cloud_instance_archetype(instance_type, provider)
    )


def gpu_embedded_gwp(cloud_instance):
    """Embedded GWP booked against the instance's share of the platform GPUs."""
    compute_single_impact(cloud_instance, "embedded", "gwp", DURATION)
    gpu = cloud_instance.platform.gpu
    if gpu is None or "gwp" not in gpu.impacts:
        return None
    return gpu.impacts["gwp"]["embedded"].value


def vcpu_allocation(cloud_instance):
    return cloud_instance.vcpu.value / cloud_instance.platform.get_total_vcpu()


def test_get_total_gpu_returns_platform_gpu_count():
    server = DeviceServer(archetype=get_server_archetype("g5.48xlarge"))
    assert server.get_total_gpu() == server.gpu.units.value == 8


def test_get_total_gpu_is_zero_without_gpu():
    server = DeviceServer(archetype=get_server_archetype("a1.metal"))
    assert server.gpu is None
    assert server.get_total_gpu() == 0


def test_gpu_allocated_by_gpu_units_not_vcpu():
    """A g5.xlarge gets 1 of the g5.48xlarge platform's 8 A10Gs."""
    g5_xlarge = instance("g5.xlarge")
    g5_full = instance("g5.48xlarge")

    share = gpu_embedded_gwp(g5_xlarge) / gpu_embedded_gwp(g5_full)

    assert share == pytest.approx(1 / 8)
    # ...and emphatically not the 4/192 vCPU prorata it used to get.
    assert vcpu_allocation(g5_xlarge) == pytest.approx(4 / 192)
    assert share != pytest.approx(vcpu_allocation(g5_xlarge))


def test_full_platform_instance_keeps_the_whole_gpu_impact():
    """No regression for an instance that occupies its entire host."""
    g5_full = instance("g5.48xlarge")
    platform = DeviceServer(archetype=get_server_archetype("g5.48xlarge"))

    assert g5_full.gpu_units.value == platform.get_total_gpu()
    assert gpu_embedded_gwp(g5_full) == pytest.approx(
        compute_single_impact(platform.gpu, "embedded", "gwp", DURATION).value
    )


def test_instance_is_not_overcharged_for_its_vcpu_share():
    """g5.16xlarge takes a third of the host's vCPUs but only 1 of its 8 GPUs."""
    g5_16xlarge = instance("g5.16xlarge")
    g5_full = instance("g5.48xlarge")

    share = gpu_embedded_gwp(g5_16xlarge) / gpu_embedded_gwp(g5_full)

    assert share == pytest.approx(1 / 8)
    # The vCPU prorata used to bill it 2.67x the GPU it actually gets.
    assert vcpu_allocation(g5_16xlarge) == pytest.approx(64 / 192)
    assert share < vcpu_allocation(g5_16xlarge)


def test_fractional_gpu_units_get_a_fraction_of_one_gpu():
    """A vGPU/MIG slice (Azure NVas_v4) gets its fraction of a single card."""
    one_gpu = instance("g5.xlarge")
    assert one_gpu.gpu_units.value == 1

    eighth = instance("g5.xlarge")
    eighth.gpu_units = Boattribute(default=0.125)

    assert gpu_embedded_gwp(eighth) == pytest.approx(gpu_embedded_gwp(one_gpu) / 8)


def test_instance_without_gpu_is_unaffected():
    no_gpu = instance("a1.4xlarge")
    assert no_gpu.platform.gpu is None
    assert gpu_embedded_gwp(no_gpu) is None


def test_zero_gpu_units_books_no_gpu_impact():
    """A GPU-less instance sold off a GPU host must not be billed for the cards."""
    no_gpu = instance("g5.xlarge")
    no_gpu.gpu_units = Boattribute(default=0)

    assert gpu_embedded_gwp(no_gpu) is None
