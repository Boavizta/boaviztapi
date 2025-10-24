from pydantic import BaseModel, ConfigDict


class BaseDTO(BaseModel):
    """
    BaseDTO is simple BaseModel object
    """
    model_config = ConfigDict(from_attributes=True)
