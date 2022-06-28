from typing import Optional, List

from boaviztapi.dto import BaseDTO
from boaviztapi.dto.component import CPU


class Workload:
    load: int = None
    power: int = None


class ConsumptionProfile(BaseDTO):
    workload: List[Workload] = None


class ConsumptionProfileCPU(ConsumptionProfile):
    cpu: CPU = None
