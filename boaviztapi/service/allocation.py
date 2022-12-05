from enum import Enum
from typing import Tuple

from boaviztapi.model.usage import ModelUsage

NumberSignificantFigures = Tuple[float, int]


def allocate(total_impact, allocation_type, usage: ModelUsage) -> NumberSignificantFigures:
    allocation_ratio = 1

    if allocation_type == Allocation.LINEAR:
        allocation_ratio = usage.use_time.value / usage.life_time.value

    return total_impact * allocation_ratio


class Allocation(Enum):
    LINEAR = "LINEAR"
    TOTAL = "TOTAL"
