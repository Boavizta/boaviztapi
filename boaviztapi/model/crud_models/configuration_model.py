from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

from boaviztapi.model.crud_models.basemodel import BaseCRUDCollection, BaseCRUDModel, PyObjectId, BaseCRUDUpdateModel


class ConfigurationModel(BaseCRUDModel):
    name: str = Field(...),
    created: datetime = Field(...)
    cpu_quantity: int = Field(...)
    cpu_core_units: int = Field(...)
    cpu_tdp: int = Field(...)
    cpu_architecture: str = Field(...)
    ram_quantity: int = Field(...)
    ram_capacity: int = Field(...)
    ram_manufacturer: str = Field(...)
    ssd_quantity: int = Field(...)
    ssd_capacity: int = Field(...)
    ssd_manufacturer: str = Field(...)
    hdd_quantity: int = Field(...)
    server_type: str = Field(...)
    psu_quantity: int = Field(...)
    user_id: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Development",
                "created": "2023-01-01T00:00:00.000Z",
                "cpu_quantity": 2,
                "cpu_core_units": 16,
                "cpu_tdp": 120,
                "cpu_architecture": "Intel Xeon",
                "ram_quantity": 1,
                "ram_capacity": 16,
                "ram_manufacturer": "Micron",
                "ssd_quantity": 1,
                "ssd_capacity": 1000,
                "ssd_manufacturer": "Samsung",
                "hdd_quantity": 1,
                "server_type": "Blade",
                "psu_quantity": 1,
                "user_id": "1234567890"
            }
        }
    )

class UpdateConfigurationModel(BaseCRUDUpdateModel):
    """
    A set of optional updates to be made to a document in the database.
    """
    name: Optional[str] = None,
    created: Optional[datetime] = None,
    cpu_quantity: Optional[int] = None,
    cpu_core_units: Optional[int] = None,
    cpu_tdp: Optional[int] = None,
    cpu_architecture: Optional[str] = None,
    ram_quantity: Optional[int] = None,
    ram_capacity: Optional[int] = None,
    ram_manufacturer: Optional[str] = None,
    ssd_quantity: Optional[int] = None,
    ssd_capacity: Optional[int] = None,
    ssd_manufacturer: Optional[str] = None,
    hdd_quantity: Optional[int] = None,
    server_type: Optional[str] = None,
    psu_quantity: Optional[int] = None,
    user_id: Optional[str] = None,
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Development",
                "created": "2023-01-01T00:00:00.000Z",
                "cpu_quantity": 2,
                "cpu_core_units": 16,
                "cpu_tdp": 120,
                "cpu_architecture": "Intel Xeon",
                "ram_quantity": 1,
                "ram_capacity": 16,
                "ram_manufacturer": "Micron",
                "ssd_quantity": 1,
                "ssd_capacity": 1000,
                "ssd_manufacturer": "Samsung",
                "hdd_quantity": 1,
                "server_type": "Blade",
                "psu_quantity": 1,
                "user_id": "1234567890"
            }
        }
    )

class ConfigurationCollection(BaseCRUDCollection[ConfigurationModel]):
    """
    A container holding a list of `ConfigurationModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """