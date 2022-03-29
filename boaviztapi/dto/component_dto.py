from pydantic import BaseModel
from typing import Optional

from boaviztapi.model.components.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentMotherBoard, ComponentCase


class Model(BaseModel):
    manufacturer: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None


class PowerSupply(BaseModel):
    units: Optional[int] = None
    unit_weight: Optional[float] = None

    def to_component(self):
        return ComponentPowerSupply(**self.dict())


class Disk(BaseModel):
    units: Optional[int] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None

    def to_component(self):
        if self.type == 'ssd':
            return ComponentSSD(**self.dict())
        if self.type == 'hdd':
            return ComponentHDD(**self.dict())


class Ram(BaseModel):
    units: Optional[int] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None

    def to_component(self):
        return ComponentRAM(**self.dict())


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

    def to_component(self):
        return ComponentCPU(**self.dict())


class MotherBoard(BaseModel):
    units: Optional[int] = None

    def to_component(self):
        return ComponentMotherBoard()


class Case(BaseModel):
    units: Optional[int] = None
    case_type: str = None

    def to_component(self):
        return ComponentCase(**self.dict())
