import boaviztapi.utils.roundit as rd
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.component.component import Component
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.factor_provider import get_impact_factor


class ComponentAssembly(Component):
    NAME = "ASSEMBLY"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact_factor = ImpactFactor(
            value=get_impact_factor(item='assembly', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='assembly', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='assembly', impact_type=impact_type)['impact']
        )

        return impact_factor.value, impact_factor.min, impact_factor.max, ["End of life is not included in the calculation"]

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        raise NotImplementedError

