from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures


class ComponentRAM(Component):
    NAME = "RAM"

    DEFAULT_RAM_CAPACITY = 32
    DEFAULT_RAM_DENSITY = 0.625

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 2.20,
            'impact': 5.22
        },
        'pe': {
            'die_impact': 27.30,
            'impact': 74.00
        },
        'adp': {
            'die_impact': 6.30E-05,
            'impact': 1.69E-03
        }
    }

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

        self.process = Boattribute(value=None, status=Status.NONE, unit="none", default="TODO")
        self.manufacturer = Boattribute(value=None, status=Status.NONE, unit="none", default="None")
        self.capacity = Boattribute(value=None, status=Status.NONE, unit="Go", default=self.DEFAULT_RAM_CAPACITY)
        self.density = Boattribute(value=None, status=Status.NONE, unit="Go/cm2", default=self.DEFAULT_RAM_DENSITY)

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        ram_die_impact, ram_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(ram_die_impact, ram_impact)
        impact = self.__compute_impact_manufacture(ram_die_impact, ram_impact)
        return impact, sign_figures

    def __get_impact_constants(self, impact_type: str) -> Tuple[float, float]:
        ram_die_impact = self.IMPACT_FACTOR[impact_type]['die_impact']
        ram_impact = self.IMPACT_FACTOR[impact_type]['impact']
        return ram_die_impact, ram_impact

    def __compute_significant_numbers(self, ram_die_impact: float, ram_impact: float) -> int:
        return rd.min_significant_figures(self.density.value, ram_die_impact, ram_impact)

    def __compute_impact_manufacture(self, ram_die_impact: float, ram_impact: float) -> float:
        return (self.capacity.value / self.density.value) * ram_die_impact + ram_impact

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
