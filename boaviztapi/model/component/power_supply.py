from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.service.factor_provider import get_impact_factor


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

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact_factor = ImpactFactor(
            value=get_impact_factor(item='power_supply', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='power_supply', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='power_supply', impact_type=impact_type)['impact']
        )

        impact = self.__compute_impact_manufacture(impact_factor)

        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]

    def __compute_impact_manufacture(self, power_supply_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=self.unit_weight.value * power_supply_impact.value,
            min=self.unit_weight.min * power_supply_impact.min,
            max=self.unit_weight.max * power_supply_impact.max
        )

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        raise NotImplementedError
