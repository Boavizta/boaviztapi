from typing import Set, Optional, List

from API.api.model.components.component import Component

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_components(components: List[Component], impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    for item in components:
        item.smart_complete_data()

    impacts = {
        'gwp': sum([item.impact_gwp() for item in components]),
        'pe': sum([item.impact_pe() for item in components]),
        'adp': sum([item.impact_adp() for item in components])
    }
    return impacts


def bottom_up_component(component: Component, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    impacts = {
        'gwp': component.impact_gwp(),
        'pe': component.impact_pe(),
        'adp': component.impact_adp()
    }
    return impacts
