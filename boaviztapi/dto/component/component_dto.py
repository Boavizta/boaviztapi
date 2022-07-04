from typing import Optional

from boaviztapi.dto.base_dto import BaseDTO
from boaviztapi.dto.usage.usage import UsageComponent


class ComponentDTO(BaseDTO):
    units: Optional[int] = 1
    usage: Optional[UsageComponent]
