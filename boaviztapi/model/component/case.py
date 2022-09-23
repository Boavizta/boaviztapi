from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures


class ComponentCase(Component):
    AVAILABLE_CASE_TYPE = ['blade', 'rack']
    NAME = "CASE"

    DEFAULT_CASE_TYPE = 'rack'

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.case_type = Boattribute(default=self.DEFAULT_CASE_TYPE)

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        if self.case_type.value == 'rack':
            return self.__impact_manufacture_rack(impact_type)
        elif self.case_type.value == 'blade':
            return self.__impact_manufacture_blade(impact_type)
        else:
            return self.__impact_manufacture_rack(impact_type)

    def __impact_manufacture_rack(self, impact_type: str) -> NumberSignificantFigures:
        impact = self.IMPACT_FACTOR['rack'][impact_type]['impact']
        significant_figures = rd.min_significant_figures(impact)
        return impact, significant_figures

    def __impact_manufacture_blade(self, impact_type: str) -> NumberSignificantFigures:
        impact_blade_server, impact_blade_16_slots = self.__get_impact_constants_blade(impact_type)
        impact = self.__compute_impact_manufacture_blade(impact_blade_server, impact_blade_16_slots)
        sign_figures = self.__compute_significant_numbers(impact_blade_server, impact_blade_16_slots)
        return impact, sign_figures

    def __get_impact_constants_blade(self, impact_type: str) -> Tuple[float, float]:
        impact_blade_server = self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_server']
        impact_blade_16_slots = self.IMPACT_FACTOR['blade'][impact_type]['impact_blade_16_slots']
        return impact_blade_server, impact_blade_16_slots

    @staticmethod
    def __compute_impact_manufacture_blade(impact_blade_server: float, impact_blade_16_slots: float) -> float:
        return (impact_blade_16_slots / 16) + impact_blade_server

    @staticmethod
    def __compute_significant_numbers(impact_blade_server: float, impact_blade_16_slots: float) -> int:
        return rd.min_significant_figures(impact_blade_server, impact_blade_16_slots)

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError
