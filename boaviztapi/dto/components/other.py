from typing import Optional

from boaviztapi.dto.components import ComponentDTO


class PowerSupply(ComponentDTO):
    unit_weight: Optional[float] = None


class Motherboard(ComponentDTO):
    pass


class Case(ComponentDTO):
    case_type: str = None
