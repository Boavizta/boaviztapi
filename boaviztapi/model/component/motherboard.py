from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.factor_provider import get_impact_factor


class ComponentMotherboard(Component):
    NAME = "MOTHERBOARD"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = ImpactFactor(
            value=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='motherboard', impact_type=impact_type)['impact']
        )

        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]