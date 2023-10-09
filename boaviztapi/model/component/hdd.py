import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.service.factor_provider import get_impact_factor


class ComponentHDD(Component):
    NAME = "HDD"

    __DISK_TYPE = 'hdd'

    def __init__(self, archetype=get_component_archetype(config["default_ssd"], "ssd"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'manufacturer', 'default'),
            min=get_arch_value(archetype, 'manufacturer', 'default'),
            max=get_arch_value(archetype, 'manufacturer', 'default')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = ImpactFactor(
            value=get_impact_factor(item='hdd', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='hdd', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='hdd', impact_type=impact_type)['impact']
        )

        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]