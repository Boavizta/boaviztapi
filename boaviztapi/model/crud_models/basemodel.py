
from typing import Annotated, Optional, Generic, TypeVar, List

from pydantic import BaseModel, BeforeValidator, Field, field_validator

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

TModel = TypeVar("TModel", bound=BaseModel)

class BaseCRUDModel(BaseModel):
    """
    Base class for all CRUD models with IDs. `(Usually used for CREATE operations)`.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    @field_validator("id")
    def validate_object_id(cls, v):
        try:
            PyObjectId(v)
        except Exception:
            raise ValueError("Invalid ObjectId")
        return v

class BaseCRUDUpdateModel(BaseModel):
    """
    Base class for all update models.
    """

class BaseCRUDCollection(BaseModel, Generic[TModel]):
    """
    Base class for all collection models.
    """
    items: List[TModel]