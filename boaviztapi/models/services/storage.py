from typing import Union

from boaviztapi import config
from boaviztapi.data.archetype import (
    get_arch_component,
    get_arch_value,
    get_component_archetype,
)
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component import ComponentHDD, ComponentSSD
from boaviztapi.models.services.cloud_instance import Service
from boaviztapi.models.usage import ModelUsage

DISKS = {
    "SSD": (ComponentSSD, config.default_ssd),
    "HDD": (ComponentHDD, config.default_hdd),
}


class ServiceStorage(Service):
    """Storage as a service, evaluated as a share of a reference disk."""

    NAME = "STORAGE_AS_A_SERVICE"

    def __init__(self, storage_type: str = "SSD", **kwargs):
        if storage_type not in DISKS:
            raise ValueError(
                f"Unknown storage type {storage_type!r}, expected one of {list(DISKS)}"
            )
        disk_class, archetype_name = DISKS[storage_type]
        archetype = get_component_archetype(archetype_name, disk_class.NAME.lower())
        super().__init__(archetype=archetype, **kwargs)

        self.storage_type = Boattribute()
        self.storage_type.set_input(storage_type)
        self.storage = Boattribute(unit="GB")
        self.replication = Boattribute(default=1)
        self.capacity = Boattribute(
            unit="GB", default=get_arch_value(archetype, "capacity", "default")
        )
        self.manufacturer = Boattribute(
            default=get_arch_value(archetype, "manufacturer", "default")
        )
        self.usage = ModelUsage(archetype=get_arch_component(archetype, "USAGE"))

    def reference_disk(self) -> Union[ComponentSSD, ComponentHDD]:
        disk_class, _ = DISKS[self.storage_type.value]
        disk = disk_class(archetype=self.archetype)
        # Fixed as an input so the archetype capacity range does not widen the
        # per-GB min/max: the allocation already divides by this capacity.
        disk.capacity.set_input(self.capacity.value)
        if disk_class is ComponentSSD and self.manufacturer.has_value():
            disk.manufacturer.set_input(self.manufacturer.value)
        disk.usage = self.usage
        return disk

    def allocation(self) -> float:
        """Share of the reference disk used: storage * replication / capacity."""
        if not self.storage.has_value():
            raise NotImplementedError
        return self.storage.value * self.replication.value / self.capacity.value
