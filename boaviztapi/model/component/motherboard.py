
import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor


class ComponentMotherboard(Component):
    NAME = "MOTHERBOARD"

    IMPACT_FACTOR = {
        'gwp': {
            'impact': 66.10
        },
        'pe': {
            'impact': 836.00
        },
        'adp': {
            'impact': 3.69E-03
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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