from pydantic import BaseModel


class ConsumptionProfile(BaseModel):
    param: dict = None
