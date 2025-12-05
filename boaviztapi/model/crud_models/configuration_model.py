from datetime import datetime
from typing import Optional, Union, Annotated, Literal, Dict, Any

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict

from boaviztapi.model.crud_models.basemodel import BaseCRUDCollection, BaseCRUDModel, BaseCRUDUpdateModel


class ServerLoadAdvancedSlot(BaseModel):
    time: int = Field(..., ge=1, le=100)
    load: int = Field(..., ge=1, le=100)

class ServerLoadAdvanced(BaseModel):
    slot1: ServerLoadAdvancedSlot = Field(...)
    slot2: ServerLoadAdvancedSlot = Field(...)
    slot3: ServerLoadAdvancedSlot = Field(...)

class OnPremiseServerUsage(BaseModel):
    localisation: str = Field(...)
    lifespan: int = Field(...)
    method: str = Field(...)
    avgConsumption: Optional[float] = Field(default=None, ge=1, le=100000)
    serverLoad: Optional[float] = Field(default=None, ge=1, le=100)
    serverLoadAdvanced: Optional[ServerLoadAdvanced] = Field(default=None)
    operatingCosts: Optional[int] = Field(default=None, ge=0, le=100000000)

class OnPremiseConfigurationModel(BaseCRUDModel):
    type: Literal['on-premise']
    name: str = Field(...),
    created: datetime = Field(...)
    cpu_quantity: int = Field(..., ge=1, le=64)
    cpu_core_units: int = Field(..., ge=1, le=1000)
    cpu_tdp: int = Field(..., ge=5, le=1000)
    cpu_architecture: str = Field(...)
    ram_quantity: int = Field(..., ge=1, le=999)
    ram_capacity: int = Field(..., ge=1, le=100000)
    ram_manufacturer: str = Field(...)
    ssd_quantity: int = Field(..., ge=1, le=100)
    ssd_capacity: int = Field(..., ge=1, le=100000)
    ssd_manufacturer: str = Field(...)
    hdd_quantity: int = Field(..., ge=1, le=100)
    server_type: str = Field(...)
    psu_quantity: int = Field(..., ge=1, le=4)
    user_id: str = Field(..., pattern=r'(\d)+')
    usage: OnPremiseServerUsage = Field(...)
    costs: Optional[Dict[str, Any]] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "type": "on-premise",
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
                "user_id": "1234567890",
                "usage": {
                    "localisation": "NL",
                    "lifespan": 5,
                    "method": "Electricity",
                    "avgConsumption": 100,
                    "serverLoad": 50,
                    "operatingCosts": 700
                }
            }
        }
    )

class CloudServerUsage(BaseModel):
    localisation: str = Field(...)
    lifespan: int = Field(..., ge=1, le=10000)
    method: str = Field(...)
    serverLoad: Optional[float] = Field(default=None, ge=1, le=100)
    serverLoadAdvanced: Optional[ServerLoadAdvanced] = Field(default=None)
    instancePricingType: Optional[str] = Field(default=None)
    reservedPlan: Optional[str] = Field(default=None),

class CloudConfigurationModel(BaseCRUDModel):
    type: Literal['cloud']
    name: str = Field(...)
    created: datetime = Field(...)
    cloud_provider: str = Field(...)
    instance_type: str = Field(...)
    usage: CloudServerUsage = Field(...)
    costs: Optional[Dict[str, Any]] = Field(default=None)
    user_id: str = Field(..., pattern=r'(\d)+')
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "type": "cloud",
                "name": "Development Cloud",
                "created": "2023-01-01T00:00:00.000Z",
                "cloud_provider": "AWS",
                "instance_type": "a1.medium",
                "usage": {
                    "localisation": "NL",
                    "lifespan": 1000,
                    "method": "Load",
                    "serverLoad": 100,
                    "instancePricingType": "OnDemand",
                    "reservedPlan": "1y"
                },
                "user_id": "1234567890"
            }
        }
    )

ConfigurationModel = Annotated[
    Union[OnPremiseConfigurationModel, CloudConfigurationModel],
    Field(discriminator="type"),
]

class ConfigurationModelWithResults(BaseModel):
    configuration: ConfigurationModel
    results: Optional[Dict[str, Any]] = Field(default=None)


class UpdateServerLoadAdvancedSlot(BaseModel):
    time: Optional[int] = Field(default=None, ge=1, le=100)
    load: Optional[int] = Field(default=None, ge=1, le=100)

class UpdateServerLoadAdvanced(BaseModel):
    slot1: Optional[ServerLoadAdvancedSlot] = None
    slot2: Optional[ServerLoadAdvancedSlot] = None
    slot3: Optional[ServerLoadAdvancedSlot] = None

class UpdateOnPremiseServerUsage(BaseModel):
    localisation: Optional[str] = None
    lifespan: Optional[int] = None
    method: Optional[str] = None
    avgConsumption: Optional[float] = None
    serverLoad: Optional[float] = None
    serverLoadAdvanced: Optional[UpdateServerLoadAdvanced] = None
    operatingCosts: Optional[int] = None

class UpdateOnPremiseConfigurationModel(BaseCRUDUpdateModel):
    type: Literal['on-premise']
    name: Optional[str] = None
    created: Optional[datetime] = None
    cpu_quantity: Optional[int] = Field(default=None, ge=1, le=64)
    cpu_core_units: Optional[int] = Field(default=None, ge=1, le=1000)
    cpu_tdp: Optional[int] = Field(default=None, ge=5, le=1000)
    cpu_architecture: Optional[str] = None
    ram_quantity: Optional[int] = Field(default=None, ge=1, le=999)
    ram_capacity: Optional[int] = Field(default=None, ge=1, le=100000)
    ram_manufacturer: Optional[str] = None
    ssd_quantity: Optional[int] = Field(default=None, ge=1, le=100)
    ssd_capacity: Optional[int] = Field(default=None, ge=1, le=100000)
    ssd_manufacturer: Optional[str] = None
    hdd_quantity: Optional[int] = Field(default=None, ge=1, le=100)
    server_type: Optional[str] = None
    psu_quantity: Optional[int] = Field(default=None, ge=1, le=4)
    user_id: Optional[str] = Field(default=None, pattern=r'(\d)+')
    usage: Optional[UpdateOnPremiseServerUsage] = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "type": "on-premise",
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
                "user_id": "1234567890",
                "usage": {
                    "localisation": "NL",
                    "lifespan": 5,
                    "method": "Electricity",
                    "avgConsumption": 100,
                    "serverLoad": 50,
                    "operatingCosts": 700
                }
            }
        }
    )

class UpdateCloudServerUsage(BaseModel):
    localisation: Optional[str] = None
    lifespan: Optional[int] = Field(default=None, ge=1, le=10000)
    method: Optional[str] = None
    serverLoad: Optional[float] = Field(default=None, ge=1, le=100000)
    serverLoadAdvanced: Optional[UpdateServerLoadAdvanced] = None
    instancePricingType: Optional[str] = None
    reservedPlan: Optional[str] = None

class UpdateCloudConfigurationModel(BaseCRUDUpdateModel):
    type: Literal['cloud']
    name: Optional[str] = None
    created: Optional[datetime] = None
    cloud_provider: Optional[str] = None
    instance_type: Optional[str] = None
    usage: Optional[UpdateCloudServerUsage] = None
    user_id: Optional[str] = Field(default=None, pattern=r'(\d)+')
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "type": "cloud",
                "name": "Development Cloud",
                "created": "2023-01-01T00:00:00.000Z",
                "cloud_provider": "AWS",
                "instance_type": "a1.medium",
                "usage": {
                    "localisation": "NL",
                    "lifespan": 1000,
                    "method": "Load",
                    "serverLoad": 100,
                    "instancePricingType": "OnDemand",
                    "reservedPlan": "1y"
                },
                "user_id": "1234567890"
            }
        }
    )
UpdateConfigurationModel = Annotated[
    Union[UpdateOnPremiseConfigurationModel, UpdateCloudConfigurationModel],
    Field(discriminator="type")
]

class ConfigurationCollection(BaseCRUDCollection[ConfigurationModel]):
    """
    A container holding a list of `ConfigurationModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """
class ConfigurationWithResultsCollection(BaseCRUDCollection[ConfigurationModelWithResults]):
    """
    A container holding a list of `ConfigurationModelWithResults` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """