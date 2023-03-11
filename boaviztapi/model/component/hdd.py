import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor


class ComponentHDD(Component):
    NAME = "HDD"

    __DISK_TYPE = 'hdd'

    IMPACT_FACTOR = {
        'gwp': {
            'impact': 31.10
        },
        'pe': {
            'impact': 276.00
        },
        'adp': {
            'impact': 2.50E-04
        }
    }

    def __init__(self, default_config=config["DEFAULT"]["HDD"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.capacity = Boattribute(
            unit="GB",
            default=default_config['capacity']['default'],
            min=default_config['capacity']['min'],
            max=default_config['capacity']['max']
        )

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['impact'],
            min=self.IMPACT_FACTOR[impact_type]['impact'],
            max=self.IMPACT_FACTOR[impact_type]['impact']
        )

        significant_figures = rd.min_significant_figures(impact.value)
        return impact.value, significant_figures, impact.min, impact.max, []

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')