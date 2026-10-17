"""RAM power of a cloud instance assumes typical DIMMs for the platform's memory type.

The DIMM layout recorded for cloud platforms is not reliable, so the per-DIMM
model uses the typical DIMM capacity of the memory type the platform's CPU
supports rather than the platform's RAM.capacity.
"""

import pytest

from boaviztapi.data.archetype import get_cloud_instance_archetype
from boaviztapi.dto.device import Cloud
from boaviztapi.dto.device.device import mapper_cloud_instance


def ram_power(instance_type, cpu_family, provider="aws"):
    cloud_instance = mapper_cloud_instance(
        Cloud(provider=provider, instance_type=instance_type),
        archetype=get_cloud_instance_archetype(instance_type, provider),
    )
    cpu = cloud_instance.platform.cpu
    cpu.threads.value  # complete the CPU from its name once...
    cpu.name_completion = True  # ...so that it doesn't overwrite the family below
    cpu.family.set_input(cpu_family)
    cloud_instance.model_power_consumption()
    return sum(ram.usage.avg_power.value for ram in cloud_instance.platform.ram)


def per_gb_at_half_load(dimm_capacity):
    return (3 + 0.055 * dimm_capacity) / dimm_capacity * 0.85


@pytest.mark.parametrize(
    "cpu_family,dimm_capacity",
    [
        ("Ivy Bridge-EP", 16),  # DDR3
        ("Graviton2", 32),  # DDR4
        ("Graviton4", 64),  # DDR5
        ("Unknown family", 32),  # defaults to DDR4
    ],
)
def test_cloud_ram_power_uses_typical_dimm_of_memory_type(cpu_family, dimm_capacity):
    # m6g.xlarge has 16 GB on a platform recorded as 8 x 32 GB DIMMs
    assert ram_power("m6g.xlarge", cpu_family) == pytest.approx(
        16 * per_gb_at_half_load(dimm_capacity), rel=1e-4
    )
