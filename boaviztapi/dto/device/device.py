from typing import Optional, List

from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply
from boaviztapi.dto.component.cpu import smart_complete_cpu
from boaviztapi.dto.component.disk import smart_complete_disk_ssd
from boaviztapi.dto.component.ram import smart_complete_ram
from boaviztapi.dto.usage import UsageServer, UsageCloud
from boaviztapi.dto import BaseDTO


class DeviceDTO(BaseDTO):
    pass


class ModelServer(BaseDTO):
    name: Optional[str] = None
    archetype: Optional[str] = None
    type: Optional[str] = None


class ConfigurationServer(BaseDTO):
    cpu: Optional[CPU] = None
    ram: Optional[List[RAM]] = None
    disk: Optional[List[Disk]] = None
    power_supply: Optional[PowerSupply] = None


class Server(DeviceDTO):
    model: Optional[ModelServer] = None
    configuration: Optional[ConfigurationServer] = None
    usage: Optional[UsageServer] = None


def smart_complete_server(server: Server):
    server_ = server.copy()

    if server_.configuration is not None:
        if server_.configuration.cpu is not None:
            server_.configuration.cpu = smart_complete_cpu(server_.configuration.cpu)
        print(server.configuration.cpu)

        if server_.configuration.ram is not None:
            complete_ram = []
            for ram_dto in server_.configuration.ram:
                complete_ram.append(smart_complete_ram(ram_dto))
            server_.configuration.ram = complete_ram

        if server_.configuration.disk is not None:
            complete_disk = []
            for disk_dto in server_.configuration.disk:
                complete_disk.append(smart_complete_disk_ssd(disk_dto))
            server_.configuration.disk = complete_disk

    return server_


class Cloud(Server):
    usage: Optional[UsageCloud] = None
