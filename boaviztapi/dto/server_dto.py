from pydantic import BaseModel
from typing import Optional, List
from boaviztapi.dto.component_dto import Cpu, Ram, Disk, PowerSupply

from boaviztapi.model.components.component import (
    ComponentCPU,
    ComponentRAM,
    ComponentSSD,
    ComponentHDD,
    ComponentPowerSupply,
    ComponentRack,
    ComponentBlade,
    Component
)
from boaviztapi.model.devices.device import Model, Server
from boaviztapi.model.components.usage import UsageServer


class ConfigurationServer(BaseModel):
    cpu: Optional[Cpu] = None
    ram: Optional[List[Ram]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None


class ModelServer(BaseModel):
    manufacturer: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None
    archetype: Optional[str] = None


class ServerDTO(BaseModel):
    model: Optional[ModelServer] = None
    configuration: Optional[ConfigurationServer] = None
    usage: Optional[UsageServer] = None

    add_method: Optional[str] = None
    add_date: Optional[str] = None

    def get_component_list(self) -> List[Component]:
        components = []
        if self.configuration:
            if self.configuration.cpu:
                components += [ComponentCPU(**self.configuration.cpu.dict())
                               for _ in range(self.configuration.cpu.units)]

            if self.configuration.ram:
                for ram in self.configuration.ram:
                    for _ in range(ram.units):
                        components.append(ComponentRAM(**ram.dict()))

            if self.configuration.disk:
                for disk in self.configuration.disk:
                    if disk.type == 'ssd':
                        for _ in range(disk.units):
                            components.append(ComponentSSD(**disk.dict()))
                    if disk.type == 'hdd':
                        for _ in range(disk.units):
                            components.append(ComponentHDD(**disk.dict()))

            if self.configuration.power_supply:
                components += [ComponentPowerSupply(**self.configuration.power_supply.dict())
                               for _ in range(self.configuration.power_supply.units)]

        if self.model:
            if self.model.type == "blade":
                components.append(ComponentBlade())
            if self.model.type == "rack":
                components.append(ComponentRack())

        return components

    def get_model(self) -> Model:
        model = Model()
        if self.model:
            model.name = self.model.name
            model.year = self.model.year
            model.manufacturer = self.model.manufacturer
            model.archetype = self.model.archetype
        return model

    def get_usage(self) -> UsageServer:
        if self.usage is None:
            return UsageServer()
        else:
            return self.usage

    def to_device(self) -> Server:
        server = Server()
        server.model = self.get_model()
        server.config_components = self.get_component_list()
        server.usage = self.get_usage()
        return server


if __name__ == '__main__':
    print(Server.schema_json(indent=2))
