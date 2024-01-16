from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_component_archetype, get_arch_value


class ComponentPowerSupply(Component):
    NAME = "POWER_SUPPLY"

    def __init__(self, archetype=get_component_archetype(config["default_power_supply"], "power_supply"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self.unit_weight = Boattribute(
            unit="kg",
            default=get_arch_value(archetype, 'unit_weight', 'default'),
            min=get_arch_value(archetype, 'unit_weight', 'min'),
            max=get_arch_value(archetype, 'unit_weight', 'max')
        )