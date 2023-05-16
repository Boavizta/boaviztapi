from enum import Enum
from typing import Tuple

from boaviztapi.model.usage import ModelUsage

NumberSignificantFigures = Tuple[float, int]


def allocate(impact, allocation_type, use_time, life_time) -> [NumberSignificantFigures, NumberSignificantFigures, NumberSignificantFigures]:
    allocation_ratio, allocation_ratio_min, allocation_ratio_max = 1,1,1

    if allocation_type == Allocation.LINEAR:
        allocation_ratio = use_time.value / life_time.value
        allocation_ratio_min = use_time.min / life_time.max
        allocation_ratio_max = use_time.max / life_time.min

    return impact.value * allocation_ratio, impact.min * allocation_ratio_min, impact.max * allocation_ratio_max


class Allocation(Enum):
    LINEAR = "LINEAR"
    TOTAL = "TOTAL"
