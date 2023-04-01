import boaviztapi.utils.roundit as rd
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.factor_provider import get_impact_factor


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

    def impact_other(self, impact_type: str) -> ComputedImpacts:
        impact = ImpactFactor(
            value=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='motherboard', impact_type=impact_type)['impact']
        )

        significant_figures = rd.min_significant_figures(impact.value)
        return impact.value, significant_figures, impact.min, impact.max, []