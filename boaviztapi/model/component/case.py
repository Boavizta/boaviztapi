from typing import Tuple

from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_arch_value, get_component_archetype
from boaviztapi.service.factor_provider import get_impact_factor


class ComponentCase(Component):
    AVAILABLE_CASE_TYPE = ['blade', 'rack']
    NAME = "CASE"

    def __init__(self, archetype=get_component_archetype(config["default_case"], "case"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.case_type = Boattribute(
            default=get_arch_value(archetype, 'case_type', 'default'),
            min=get_arch_value(archetype, 'case_type', 'min'),
            max=get_arch_value(archetype, 'case_type', 'max')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        if self.case_type.value == 'rack':
            return self.__impact_manufacture_rack(impact_type)
        elif self.case_type.value == 'blade':
            return self.__impact_manufacture_blade(impact_type)

    def __impact_manufacture_rack(self, impact_type: str) -> ComputedImpacts:
        impact_factor = ImpactFactor(
            value=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact'],
            min=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact'],
            max=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact']
        )

        if self.case_type.is_archetype() and self.case_type.value == 'rack':
            blade_impact = self.__impact_manufacture_blade(impact_type)
            if blade_impact[0] > impact_factor.value:
                return impact_factor.value, impact_factor.min, blade_impact[2], ["End of life is not included in the calculation"]
            else:
                return impact_factor.value, blade_impact[1], impact_factor.max, ["End of life is not included in the calculation"]
        return impact_factor.value, impact_factor.min, impact_factor.max, ["End of life is not included in the calculation"]

    def __impact_manufacture_blade(self, impact_type: str) -> ComputedImpacts:
        impact_blade_server, impact_blade_16_slots = self.__get_impact_constants_blade(impact_type)

        impact = self.__compute_impact_manufacture_blade(impact_blade_server, impact_blade_16_slots)

        if self.case_type.is_archetype() and self.case_type.value == 'blade':
            rack_impact = self.__impact_manufacture_rack(impact_type)
            if rack_impact[0] > impact.value:
                return impact.value, impact.min, rack_impact[2], ["End of life is not included in the calculation"]
            else:
                return impact.value, rack_impact[1], impact.max, ["End of life is not included in the calculation"]

        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]

    def __get_impact_constants_blade(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        impact_blade_server = ImpactFactor(
            value=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
            min=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
            max=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
        )
        impact_blade_16_slots = ImpactFactor(
            value=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
            min=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
            max=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
        )

        return impact_blade_server, impact_blade_16_slots

    @staticmethod
    def __compute_impact_manufacture_blade(impact_blade_server: ImpactFactor, impact_blade_16_slots: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(impact_blade_16_slots.value / 16) + impact_blade_server.value,
            min=(impact_blade_16_slots.min / 16) + impact_blade_server.min,
            max=(impact_blade_16_slots.max / 16) + impact_blade_server.max
        )

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        raise NotImplementedError