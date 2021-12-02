import json
from pydantic import BaseModel
from typing import Optional, List


class ModelServer(BaseModel):
    manufacturer: Optional[str] = None 
    name: Optional[str] = None 
    type_: Optional[str] = None 
    year: Optional[str] = None


class PowerSupply(BaseModel):
    units: Optional[str] = None
    unit_weight: Optional[str] = None


class Disk(BaseModel):
    units: Optional[str] = None
    type_: Optional[str] = None
    capacity: Optional[str] = None
    density: Optional[str] = None
    manufacturer: Optional[str] = None
    manuf_date: Optional[str] = None
    model: Optional[str] = None


class Ram(BaseModel):
    units: Optional[str] = None
    capacity: Optional[str] = None
    density: Optional[str] = None
    manufacturer: Optional[str] = None
    manuf_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None


class Cpu(BaseModel):
    units: Optional[str] = None
    core_units: Optional[str] = None
    die_size: Optional[str] = None
    manufacturer: Optional[str] = None
    manuf_date: Optional[str] = None
    model: Optional[str] = None
    cpu_family: Optional[str] = None


class ConfigurationServer(BaseModel):
    cpu: Optional[Cpu] = None
    ram: Optional[List[Ram]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None


class Server(BaseModel):
    model: ModelServer
    configuration: ConfigurationServer

    add_method: Optional[str] = None
    add_date: Optional[str] = None
