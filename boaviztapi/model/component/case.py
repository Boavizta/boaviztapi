from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_arch_value, get_component_archetype


class ComponentCase(Component):
    AVAILABLE_CASE_TYPE = ['blade', 'rack']
    NAME = "CASE"

    IMPACT_FACTOR = {
        'rack': {
            'gwp': {
                'impact': 150.00
            },
            'pe': {
                'impact': 2200.00
            },
            'adp': {
                'impact': 2.02E-02
            }
        },
        'blade': {
            'gwp': {
                'impact_blade_server': 30.90,
                'impact_blade_16_slots': 880.00
            },
            'pe': {
                'impact_blade_server': 435.00,
                'impact_blade_16_slots': 12700.00
            },
            'adp': {
                'impact_blade_server': 6.72E-04,
                'impact_blade_16_slots': 4.32E-01
            }
        }
    }

    def __init__(self, archetype=get_component_archetype(config["default_case"], "case"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.case_type = Boattribute(
            default=get_arch_value(archetype, 'case_type', 'default'),
            min=get_arch_value(archetype, 'case_type', 'min'),
            max=get_arch_value(archetype, 'case_type', 'max')
        )

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        if self.case_type.value == 'rack':
            return self.__impact_manufacture_rack(impact_type)
        elif self.case_type.value == 'blade':
            return self.__impact_manufacture_blade(impact_type)

    def __impact_manufacture_rack(self, impact_type: str) -> ComputedImpacts:
        impact_factor = ImpactFactor(
            value=self.IMPACT_FACTOR['rack'][impact_type]['impact'],
            min=self.IMPACT_FACTOR['rack'][impact_type]['impact'],
            max=self.IMPACT_FACTOR['rack'][impact_type]['impact']
        )

        significant_figures = rd.min_significant_figures(impact_factor.value)

        if self.case_type.is_default() and self.case_type.value == 'rack':
            blade_impact = self.__impact_manufacture_blade(impact_type)
            if blade_impact[0] > impact_factor.value:
                return impact_factor.value, significant_figures, impact_factor.min, blade_impact[3], []
            else:
                return impact_factor.value, significant_figures, blade_impact[2], impact_factor.max, []
        return impact_factor.value, significant_figures, impact_factor.min, impact_factor.max, []

    def __impact_manufacture_blade(self, impact_type: str) -> ComputedImpacts:
        impact_blade_server, impact_blade_16_slots = self.__get_impact_constants_blade(impact_type)

        impact = self.__compute_impact_manufacture_blade(impact_blade_server, impact_blade_16_slots)

        significant_figures = self.__compute_significant_numbers(impact_blade_server.value, impact_blade_16_slots.value)

        if self.case_type.is_default() and self.case_type.value == 'blade':
            rack_impact = self.__impact_manufacture_rack(impact_type)
            if rack_impact[0] > impact.value:
                return impact.value, significant_figures, impact.min, rack_impact[3], []
            else:
                return impact.value, significant_figures, rack_impact[2], impact.max, []

        return impact.value, significant_figures, impact.min, impact.max, []


    def __get_impact_constants_blade(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        impact_blade_server = ImpactFactor(
            value=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server'],
            min=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server'],
            max=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server']
        )
        impact_blade_16_slots = ImpactFactor(
            value=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_16_slots'],
            min=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server'],
            max=self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server']
        )

        return impact_blade_server, impact_blade_16_slots

    @staticmethod
    def __compute_impact_manufacture_blade(impact_blade_server: ImpactFactor, impact_blade_16_slots: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(impact_blade_16_slots.value / 16) + impact_blade_server.value,
            min=(impact_blade_16_slots.min / 16) + impact_blade_server.min,
            max=(impact_blade_16_slots.max / 16) + impact_blade_server.max
        )

    @staticmethod
    def __compute_significant_numbers(impact_blade_server: float, impact_blade_16_slots: float) -> int:
        return rd.min_significant_figures(impact_blade_server, impact_blade_16_slots)

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> ComputedImpacts:
        raise NotImplementedError

    def impact_use_pe(self) -> ComputedImpacts:
        raise NotImplementedError

    def impact_use_adp(self) -> ComputedImpacts:
        raise NotImplementedError
