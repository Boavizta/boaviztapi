import boaviztapi.utils.roundit as rd
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.component.component import Component


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
        impact = self.IMPACT_FACTOR[impact_type]['impact']
        significant_figures = rd.min_significant_figures(impact)
        return impact, significant_figures, 0, []

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