from datetime import datetime
from typing import Optional, List, Annotated, Union

from bson import ObjectId
from pydantic import Field, ConfigDict, field_validator

from boaviztapi.model.crud_models.basemodel import BaseCRUDModel, BaseCRUDCollection, BaseCRUDUpdateModel, PyObjectId
from boaviztapi.model.crud_models.configuration_model import ConfigurationModel, ConfigurationModelWithResults


class PortfolioModel(BaseCRUDModel):
    name: str = Field(...)
    created: datetime = Field(...)
    configuration_ids: list[str] = Field(...)
    user_id: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Development",
                "created": "2023-01-01T00:00:00.000Z",
                "configuration_ids": ["617777777777777777777777", "617777777777777777777778"],
                "user_id": "1234567890"
            }
        }
    )


class UpdatePortfolioModel(BaseCRUDUpdateModel):
    name: Optional[str] = None,
    created: Optional[datetime] = None,
    configuration_ids: list[str] = None,
    user_id: Optional[str] = None,
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Development",
                "created": "2023-01-01T00:00:00.000Z",
                "configuration_ids": ["617777777777777777777777", "617777777777777777777778"],
                "user_id": "1234567890"
            }
        }
    )

class ExtendedPortfolioModel(PortfolioModel):
    configuration_ids: List[PyObjectId] = Field(...)
    configurations: List[ConfigurationModel] = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={
            ObjectId: str,
            datetime: lambda dt: dt.isoformat() if dt else None
        },
        json_schema_extra={
            "example": [
                {
                '_id': '6919eb29d50531ad3f572173',
                'name': 'Development',
                'created': '2023-01-01T00:00:00',
                'configuration_ids': ['6919df6f4e03b99d4d2f6373', '6919df764e03b99d4d2f6374'],
                'user_id': '118250194734512207866',
                'configurations': [
                    {
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
                        "user_id": "118250194734512207866"
                    },
                    {
                        "type": "cloud",
                        "name": "Development Cloud",
                        "created": "2023-01-01T00:00:00.000Z",
                        "localisation": "NL",
                        "lifespan": 1000,
                        "method": "Load",
                        "serverLoad": 100,
                        "instancePricingType": "OnDemand",
                        "reservedPlan": "1y",
                        "user_id": "118250194734512207866"
                    }
                ]
                }
            ]
        }
    )

class ExtendedPortfolioWithResultsModel(ExtendedPortfolioModel):
    configurations: List[ConfigurationModelWithResults] = Field(...)
    portfolio_costs: dict | None = None

class PortfolioCollection(BaseCRUDCollection[PortfolioModel]):
    """
    A container holding a list of `PortfolioModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

class ExtendedPortfolioCollection(BaseCRUDCollection[ExtendedPortfolioModel]):
    """
    A container holding a list of `ExtendedPortfolioModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

class ExtendedPortfolioWithResultsCollection(BaseCRUDCollection[ExtendedPortfolioWithResultsModel]):
    """
    A container holding a list of `ExtendedPortfolioWithResultsModel` objects.
    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """