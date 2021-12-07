from typing import List
from pydantic import BaseModel


class Impact(BaseModel):
    type: str
    value: float
