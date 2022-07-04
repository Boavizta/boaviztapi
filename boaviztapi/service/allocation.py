from enum import Enum
from typing import Tuple

NumberSignificantFigures = Tuple[float, int]


def allocate(total_impact, allocation_type, use_time, life_time) -> NumberSignificantFigures:
    allocation_ratio = 1

    if allocation_type == Allocation.LINEAR:
        allocation_ratio = use_time / life_time

    return total_impact * allocation_ratio


class Allocation(Enum):
    LINEAR = "LINEAR"
    TOTAL = "TOTAL"
