from typing import Union, Optional

from boaviztapi import config
from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
from boaviztapi.model.impact import Impact, IMPACT_CRITERIAS, IMPACT_PHASES
from boaviztapi.service.allocation import allocate, Allocation

NOT_IMPLEMENTED = 'not implemented'
def get_model_single_impact(model: Union[Component, Device],
                            phase: str,
                            impact_type: str,
                            allocation_type: Allocation = Allocation.TOTAL) -> Optional[Impact]:
    try:
        impact_function = model.__getattribute__(f'impact_{phase}')
        impact, significant_figures, min_impact, max_impact, warnings = impact_function(impact_type)

        if phase == "other":
            impact = allocate(impact, allocation_type, model.usage)

        return Impact(
            value=impact*model.units.value,
            significant_figures=significant_figures,
            min=min_impact*model.units.min,
            max=max_impact*model.units.max,
            warnings=warnings
        )
    except (AttributeError, NotImplementedError):
        pass

def bottom_up(model: Union[Component, Device], allocation, selected_criteria=config["default_criteria"]) -> dict:
    impacts = {}
    for criteria in IMPACT_CRITERIAS:
        if criteria.name not in selected_criteria:
            continue
        impacts[criteria.name] = {}
        for phase in IMPACT_PHASES:
            single_impact = get_model_single_impact(model, phase, criteria.name, allocation_type=allocation)
            impacts[criteria.name][phase] = single_impact.to_json() if single_impact else NOT_IMPLEMENTED
        impacts[criteria.name]["unit"] = criteria.unit
        impacts[criteria.name]["description"] = criteria.description

    return impacts
