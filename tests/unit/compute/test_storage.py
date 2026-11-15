"""Storage as a service is a share of a reference disk. See issue #143.

impact = impact(reference disk) * storage * replication / disk capacity
"""

import pytest

from boaviztapi.compute.impacts_computation import compute_single_impact
from boaviztapi.models.services.storage import ServiceStorage

PHASES = ["embedded", "use"]


def storage(storage_type="SSD", storage_gb=1000, replication=1):
    service = ServiceStorage(storage_type)
    service.storage.set_input(storage_gb)
    service.replication.set_input(replication)
    return service


def impact(service, phase):
    return compute_single_impact(service, phase, "gwp", duration=8760)


@pytest.mark.parametrize("storage_type", ["SSD", "HDD"])
@pytest.mark.parametrize("phase", PHASES)
def test_storage_scales_with_storage_and_replication(storage_type, phase):
    base = impact(storage(storage_type, 100), phase)
    double = impact(storage(storage_type, 200), phase)
    replicated = impact(storage(storage_type, 100, replication=3), phase)

    assert base.value > 0
    for attr in ("value", "min", "max"):
        assert getattr(double, attr) == pytest.approx(2 * getattr(base, attr))
        assert getattr(replicated, attr) == pytest.approx(3 * getattr(base, attr))


@pytest.mark.parametrize("storage_type", ["SSD", "HDD"])
@pytest.mark.parametrize("phase", PHASES)
def test_storage_of_one_disk_equals_reference_disk(storage_type, phase):
    service = storage(storage_type)
    service.storage.set_input(service.capacity.value)

    service_impact = impact(service, phase)
    disk_impact = impact(service.reference_disk(), phase)

    for attr in ("value", "min", "max"):
        assert getattr(service_impact, attr) == pytest.approx(
            getattr(disk_impact, attr)
        )


def test_hdd_warns_capacity_independent_factor():
    warnings = impact(storage("HDD"), "embedded").warnings
    assert any("does not depend on capacity" in w for w in warnings)


def test_storage_without_storage_is_not_implemented():
    assert impact(ServiceStorage("SSD"), "embedded") is None


def test_invalid_storage_type_raises():
    with pytest.raises(ValueError):
        ServiceStorage("TAPE")
