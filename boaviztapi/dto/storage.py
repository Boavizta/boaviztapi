from typing import Annotated, Literal, Optional

from pydantic import Field, field_validator

from boaviztapi.data.archetype import get_arch_component
from boaviztapi.dto import BaseDTO
from boaviztapi.dto.usage import UsageStorage
from boaviztapi.dto.usage.usage import mapper_usage
from boaviztapi.models.services.storage import ServiceStorage


class ConfigurationStorage(BaseDTO):
    type: Literal["SSD", "HDD"] = "SSD"
    capacity: Optional[float] = Field(
        default=None, gt=0, description="Reference disk capacity in GB"
    )
    manufacturer: Optional[str] = None
    replication: Annotated[Optional[int], Field(ge=1)] = None

    @field_validator("type", mode="before")
    @classmethod
    def upper_type(cls, value):
        return value.upper() if isinstance(value, str) else value


class Storage(BaseDTO):
    configuration: ConfigurationStorage = ConfigurationStorage()
    usage: UsageStorage


def mapper_storage(storage_dto: Storage) -> ServiceStorage:
    conf = storage_dto.configuration
    model = ServiceStorage(storage_type=conf.type)

    model.storage.set_input(storage_dto.usage.storage)
    if conf.capacity is not None:
        model.capacity.set_input(conf.capacity)
    if conf.manufacturer is not None:
        model.manufacturer.set_input(conf.manufacturer)
    if conf.replication is not None:
        model.replication.set_input(conf.replication)

    usage = storage_dto.usage
    if usage.use_time_ratio is None and usage.hours_electrical_consumption is not None:
        usage.use_time_ratio = usage.hours_electrical_consumption / 24
    model.usage = mapper_usage(
        usage, archetype=get_arch_component(model.archetype, "USAGE")
    )
    return model
