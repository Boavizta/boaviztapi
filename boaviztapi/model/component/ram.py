from typing import Tuple

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi.dto.component import RAM
from boaviztapi.model.boattribute import Boattribute, Status
from boaviztapi.model.component.component import Component, NumberSignificantFigures


class ComponentRAM(Component):

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
        super().__init__()

        self.__capacity = Boattribute(value=None, status=Status.NONE, unit="Go")
        self.__density = Boattribute(value=None, status=Status.NONE, unit="Go/cm2")

        for attr, val in kwargs.items():
            if val is not None and hasattr(self, f'_ComponentRAM__{attr}'):
                self.__setattr__(attr, val)

    @property
    def capacity(self) -> float:
        if self.__capacity.value is None:
            self.__capacity.value = self.DEFAULT_RAM_CAPACITY
            self.__capacity.status = Status.DEFAULT
        return self.__capacity.value

    @capacity.setter
    def capacity(self, value: float) -> None:
        self.__capacity.value = value

    @property
    def density(self) -> float:
        if self.__density.value is None:
            self.__density.value = self.DEFAULT_RAM_DENSITY
            self.__density.status = Status.DEFAULT
        return self.__density.value

    @density.setter
    def density(self, value: float) -> None:
        self.__density.value = value

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
        return rd.min_significant_figures(self.density, ram_die_impact, ram_impact)

    def __compute_impact_manufacture(self, ram_die_impact: float, ram_impact: float) -> float:
        return (self.capacity / self.density) * ram_die_impact + ram_impact

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

    def to_dto(self, original_ram: RAM) -> RAM:
        ram = RAM()
        for attr, val in original_ram.dict().items():
            if hasattr(self, f'_ComponentRAM__{attr}'):
                ram.__setattr__(attr, self.__getattribute__(attr))
            else:
                ram.__setattr__(attr, original_ram.__getattribute__(attr))
        return ram