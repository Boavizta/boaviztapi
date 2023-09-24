from typing import Union, Optional

from boaviztapi import config
from boaviztapi.model.component import Component
from boaviztapi.model.device import Device
from boaviztapi.model.impact import Impact, IMPACT_CRITERIAS, IMPACT_PHASES
from boaviztapi.service.allocation import allocate

NOT_IMPLEMENTED = 'not implemented'


def get_model_single_impact(model: Union[Component, Device],
                            phase: str,
                            impact_type: str,
                            duration: Union[int, str] = config["default_duration"]) -> Optional[Impact]:
    try:
        impact_function = model.__getattribute__(f'impact_{phase}')

        if phase == "use":
            impact, min_impact, max_impact, warnings = impact_function(impact_type, duration)
        else:
            impact, min_impact, max_impact, warnings = impact_function(impact_type)
            impact, min_impact, max_impact = allocate(Impact(value=impact, min=min_impact, max=max_impact), duration,
                                                      model.usage.hours_life_time)

        return Impact(
            value=impact * model.units.value,
            min=min_impact * model.units.min,
            max=max_impact * model.units.max,
            warnings=list(set(warnings))
        )
    except (AttributeError, NotImplementedError):
        pass


def bottom_up(model: Union[Component, Device], selected_criteria=config["default_criteria"],
              duration=config["default_duration"]) -> dict:
    impacts = {}
    for criteria in IMPACT_CRITERIAS:
        if "all" not in selected_criteria:
            if criteria.name not in selected_criteria:
                continue
        impacts[criteria.name] = {}
        for phase in IMPACT_PHASES:
            single_impact = get_model_single_impact(model, phase, criteria.name, duration=duration)
            impacts[criteria.name][phase] = single_impact.to_json() if single_impact else NOT_IMPLEMENTED
        impacts[criteria.name]["unit"] = criteria.unit
        impacts[criteria.name]["description"] = criteria.description

    return impacts
