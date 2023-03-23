from typing import Optional

from boaviztapi.dto.base_dto import BaseDTO
from boaviztapi.dto.usage import Usage


class ComponentDTO(BaseDTO):
    units: Optional[int]
    usage: Optional[Usage] = Usage()
