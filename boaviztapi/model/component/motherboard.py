
import boaviztapi.utils.roundit as rd
from boaviztapi.model.component.component import Component, ComputedImpacts


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
        impact = self.IMPACT_FACTOR[impact_type]['impact']
        significant_figures = rd.min_significant_figures(impact)
        return impact, significant_figures, 0, []

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')