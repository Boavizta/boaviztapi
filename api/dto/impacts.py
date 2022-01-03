from typing import Optional

from pydantic import BaseModel


class Impact(BaseModel):
    manufacture: Optional[float] = None
    use: Optional[float] = None
    total: Optional[float] = None


class Impacts(BaseModel):
    gwp: Optional[Impact] = None
    adp: Optional[Impact] = None
    pe: Optional[Impact] = None
