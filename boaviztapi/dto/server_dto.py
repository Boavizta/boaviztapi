from pydantic import BaseModel
from typing import Optional, List

from boaviztapi.dto.components import CPU, RAM, Disk, PowerSupply
from boaviztapi.dto.usage_dto import UsageServerDTO, UsageCloudDTO
from boaviztapi.dto import BaseDTO


class ConfigurationServer(BaseDTO):
    cpu: Optional[CPU] = None
    ram: Optional[List[RAM]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None


class ModelServer(BaseDTO):
    manufacturer: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None
    archetype: Optional[str] = None


class ServerDTO(BaseDTO):
    model: Optional[ModelServer] = None
    configuration: Optional[ConfigurationServer] = None
    usage: Optional[UsageServerDTO] = None


class CloudDTO(ServerDTO):
    usage: Optional[UsageCloudDTO] = None
