"""Local disks add to the use-phase power of a cloud instance. See issue #595.

Their power is allocated by the instance's share of the platform's storage, as
for the embedded impacts.
"""

import pytest

from boaviztapi.data.archetype import get_cloud_instance_archetype
from boaviztapi.models.services.cloud_instance import ServiceCloudInstance


def instance(instance_type, provider="aws"):
    return ServiceCloudInstance(
        archetype=get_cloud_instance_archetype(instance_type, provider)
    )


def test_cloud_disk_power_allocated_by_storage_share():
    with_disk = instance("r5ad.12xlarge")
    without_disk = instance("r5ad.12xlarge")
    without_disk.ssd_storage.set_input(0)

    platform = with_disk.platform
    (ssd,) = [disk for disk in platform.disk if disk.NAME == "SSD"]
    share = with_disk.ssd_storage.value / platform.get_total_disk_capacity("SSD")
    expected = ssd.POWER_PER_DRIVE[0] * ssd.units.value * share

    assert with_disk.model_power_consumption().value - (
        without_disk.model_power_consumption().value
    ) == pytest.approx(expected)
