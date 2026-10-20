from boaviztapi import config
from boaviztapi.models.boattribute import Boattribute
from boaviztapi.models.component.component import Component
from boaviztapi.data.archetype import get_component_archetype, get_arch_value


class ComponentHDD(Component):
    NAME = "HDD"

    __DISK_TYPE = "hdd"

    # Average power per drive in W (value, min, max), close to constant with
    # load: 6.4 W per HDD in 2025 (LBNL 2024 United States Data Center Energy
    # Usage Report); 5.4 W idle to 9.4 W random read (Seagate Exos X20).
    POWER_PER_DRIVE = (6.4, 5.4, 9.4)

    def __init__(
        self, archetype=get_component_archetype(config.default_ssd, "ssd"), **kwargs
    ):
        super().__init__(archetype=archetype, **kwargs)

        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, "capacity", "default"),
            min=get_arch_value(archetype, "capacity", "default"),
            max=get_arch_value(archetype, "capacity", "default"),
        )
