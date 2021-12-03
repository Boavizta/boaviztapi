import json
from pydantic import BaseModel
from typing import Optional, List

from api.model.impacts import Impact


class ModelServer(BaseModel):
    manufacturer: Optional[str] = None 
    name: Optional[str] = None 
    type: Optional[str] = None
    year: Optional[str] = None


class PowerSupply(BaseModel):
    units: Optional[int] = None
    unit_weight: Optional[float] = None
    _impacts: List[Impact] = None


class Disk(BaseModel):
    units: Optional[int] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    _impacts: List[Impact] = None


class Ram(BaseModel):
    units: Optional[int] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None
    _impacts: List[Impact] = None


class Cpu(BaseModel):
    units: Optional[int] = None
    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    family: Optional[str] = None
    _impacts: List[Impact] = None


class MotherBoard(BaseModel):
    _impacts: List[Impact] = None


class ConfigurationServer(BaseModel):
    cpu: Optional[Cpu] = None
    ram: Optional[List[Ram]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None
    _motherboard: [MotherBoard] = None


class Server(BaseModel):
    model: Optional[ModelServer] = None
    configuration: Optional[ConfigurationServer] = None
    _impact_assembly: List[Impact] = None
    _impact_server_type: List[Impact] = None

    add_method: Optional[str] = None
    add_date: Optional[str] = None

    def iter_components(self) -> List[BaseModel]:
        components = []
        components.append(self.configuration.cpu)
        components += self.configuration.ram
        components += self.configuration.disk
        components.append(self.configuration.power_supply)
        components.append(self.configuration._motherboard)
        return components


if __name__ == '__main__':
    print(Server.schema_json(indent=2))
