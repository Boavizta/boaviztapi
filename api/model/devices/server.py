from pydantic import BaseModel
from typing import Optional, List

from api.model.components.component import (
    ComponentCPU,
    ComponentRAM,
    ComponentSSD,
    ComponentHDD,
    ComponentPowerSupply,
    ComponentMotherBoard,
    ComponentAssembly,
    ComponentRack,
    ComponentBlade,
    Component
)

POWER_SUPPLY_NUMBER = 2
CPU_NUMBER = 2
SSD_NUMBER = 1
RAM_NUMBER = 24


class ModelServer(BaseModel):
    manufacturer: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None


class PowerSupply(BaseModel):
    units: Optional[int] = None
    unit_weight: Optional[float] = None


class Disk(BaseModel):
    units: Optional[int] = None
    type: Optional[str] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None


class Ram(BaseModel):
    units: Optional[int] = None
    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None


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


class ConfigurationServer(BaseModel):
    cpu: Optional[Cpu] = None
    ram: Optional[List[Ram]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None


def get_default_cpu() -> List[Component]:

    return [ComponentCPU() for _ in range(CPU_NUMBER)]


def get_default_ssd() -> List[Component]:

    return [ComponentSSD() for _ in range(SSD_NUMBER)]


def get_default_ram() -> List[Component]:

    return [ComponentRAM() for _ in range(RAM_NUMBER)]


def get_default_power_supply() -> List[Component]:

    return [ComponentPowerSupply() for _ in range(POWER_SUPPLY_NUMBER)]


def get_default_configuration_component_list() -> List[Component]:

    components = [*get_default_cpu(), *get_default_ssd(), *get_default_ram(), *get_default_power_supply()]
    return components


class Server(BaseModel):
    model: Optional[ModelServer] = None
    configuration: Optional[ConfigurationServer] = None

    add_method: Optional[str] = None
    add_date: Optional[str] = None

    def get_component_list(self) -> List[Component]:
        components = []
        if self.configuration:
            if self.configuration.cpu:
                components += [ComponentCPU(**self.configuration.cpu.dict())
                               for _ in range(self.configuration.cpu.units)]
            else:
                components += [*get_default_cpu()]

            if self.configuration.ram:
                for ram in self.configuration.ram:
                    for _ in range(ram.units):
                        components.append(ComponentRAM(**ram.dict()))
            else:
                components += [*get_default_ram()]

            if self.configuration.disk:
                for disk in self.configuration.disk:
                    if disk.type == 'ssd':
                        for _ in range(disk.units):
                            components.append(ComponentSSD(**disk.dict()))
                    if disk.type == 'hdd':
                        for _ in range(disk.units):
                            components.append(ComponentHDD(**disk.dict()))
            else:
                components += [*get_default_ssd()]

            if self.configuration.power_supply:
                components += [ComponentPowerSupply(**self.configuration.power_supply.dict())
                               for _ in range(self.configuration.power_supply.units)]
            else:
                components += [*get_default_power_supply()]

        else:
            components += get_default_configuration_component_list()

        if self.model:
            if self.model.type == "blade":
                components.append(ComponentBlade())
            else:
                components.append(ComponentRack())
        else:
            components.append(ComponentRack())

        components.append(ComponentMotherBoard())
        components.append(ComponentAssembly())

        return components


if __name__ == '__main__':
    print(Server.schema_json(indent=2))
