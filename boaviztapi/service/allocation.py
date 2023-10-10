from typing import Tuple

NumberSignificantFigures = Tuple[float, int]


def allocate(impact, duration, life_time) -> [NumberSignificantFigures, NumberSignificantFigures, NumberSignificantFigures]:

    if duration > life_time.value:
        allocation_ratio, allocation_ratio_min, allocation_ratio_max = 1, 1, 1
    else:
        allocation_ratio = duration / life_time.value
        allocation_ratio_min = duration / life_time.max
        allocation_ratio_max = duration / life_time.min

    return impact.value * allocation_ratio, impact.min * allocation_ratio_min, impact.max * allocation_ratio_max