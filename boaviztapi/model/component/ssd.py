from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts


class ComponentSSD(Component):
    NAME = "SSD"

    __DISK_TYPE = 'ssd'

    DEFAULT_SSD_CAPACITY = 1000
    DEFAULT_SSD_DENSITY = 48.5

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 2.20,
            'impact': 6.34
        },
        'pe': {
            'die_impact': 27.30,
            'impact': 76.90
        },
        'adp': {
            'die_impact': 6.30E-05,
            'impact': 5.63E-04
        }
    }

    def __init__(self, default_config=config["DEFAULT"]["SSD"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.manufacturer = Boattribute(
            unit="none",
            default=default_config['manufacturer']['default'],
        )
        self.capacity = Boattribute(
            unit="GB",
            default=default_config['capacity']['default'],
            min=default_config['capacity']['min'],
            max=default_config['capacity']['max']
        )
        self.density = Boattribute(
            unit="GB/cm2",
            default=default_config['density']['default'],
            min=default_config['density']['min'],
            max=default_config['density']['max']
        )

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        ssd_die_impact, ssd_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(ssd_die_impact, ssd_impact)
        impact = self.__compute_impact_manufacture(ssd_die_impact, ssd_impact)
        return impact, sign_figures, 0, []

    def __get_impact_constants(self, impact_type: str) -> Tuple[float, float]:
        ssd_die_impact = self.IMPACT_FACTOR[impact_type]['die_impact']
        ssd_impact = self.IMPACT_FACTOR[impact_type]['impact']
        return ssd_die_impact, ssd_impact

    def __compute_significant_numbers(self, ssd_die_impact: float, ssd_impact: float) -> int:
        return rd.min_significant_figures(self.density.value, ssd_die_impact, ssd_impact)

    def __compute_impact_manufacture(self, ssd_die_impact: float, ssd_impact: float) -> float:
        return (self.capacity.value / self.density.value) * ssd_die_impact + ssd_impact

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')