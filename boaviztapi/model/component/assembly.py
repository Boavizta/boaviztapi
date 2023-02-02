import boaviztapi.utils.roundit as rd
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.component.component import Component
from boaviztapi.model.impact import ImpactFactor


class ComponentAssembly(Component):

    NAME = "ASSEMBLY"

    IMPACT_FACTOR = {
        'gwp': {
            'impact': 6.68
        },
        'pe': {
            'impact': 68.60
        },
        'adp': {
            'impact': 1.41E-06
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        impact_factor = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['impact'],
            min=self.IMPACT_FACTOR[impact_type]['impact'],
            max=self.IMPACT_FACTOR[impact_type]['impact']
        )

        significant_figures = rd.min_significant_figures(impact_factor.value)
        return impact_factor.value, significant_figures, impact_factor.min, impact_factor.max, []

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self, model=None) -> ComputedImpacts:
        raise NotImplementedError

    def impact_use_pe(self, model=None) -> ComputedImpacts:
        raise NotImplementedError

    def impact_use_adp(self, model=None) -> ComputedImpacts:
        raise NotImplementedError