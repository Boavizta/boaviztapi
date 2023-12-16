from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_component_archetype, get_arch_value


class ComponentHDD(Component):
    NAME = "HDD"

    __DISK_TYPE = 'hdd'

    def __init__(self, archetype=get_component_archetype(config["default_ssd"], "ssd"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'capacity', 'default'),
            min=get_arch_value(archetype, 'capacity', 'default'),
            max=get_arch_value(archetype, 'capacity', 'default')
        )