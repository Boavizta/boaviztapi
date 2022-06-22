from typing import Optional

from boaviztapi.dto.base_dto import BaseDTO


class ComponentDTO(BaseDTO):
    units: Optional[int] = 1