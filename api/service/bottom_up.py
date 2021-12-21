from typing import Set, Optional, List

from api.model.components.component import Component

_default_impacts_code = {"gwp", "pe", "adp"}


def bottom_up_components(components: List[Component], impact_codes: Optional[Set[str]] = None) -> dict:
    # Smart complete data
    for item in components:
        item.smart_complete_data()

    impacts = {
        'gwp': round(sum([item.impact_gwp() for item in components]), 0),
        'pe': round(sum([item.impact_pe() for item in components]), 0),
        'adp': round(sum([item.impact_adp() for item in components]), 3)
    }
    return impacts


def bottom_up_component(component: Component, impact_codes: Optional[Set[str]] = None) -> dict:
    component.smart_complete_data()
    impacts = {
        'gwp': round(component.impact_gwp(), 0),
        'pe': round(component.impact_pe(), 0),
        'adp': round(component.impact_adp(), 3)
    }
    return impacts