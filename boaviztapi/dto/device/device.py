from typing import Optional, List

from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply
from boaviztapi.dto.component.cpu import smart_mapper_cpu
from boaviztapi.dto.component.disk import smart_mapper_ssd, mapper_hdd
from boaviztapi.dto.component.other import mapper_power_supply
from boaviztapi.dto.component.ram import smart_mapper_ram
from boaviztapi.dto.usage import UsageServer, UsageCloud
from boaviztapi.dto import BaseDTO
from boaviztapi.dto.usage.usage import smart_mapper_usage_server
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.component import ComponentCase
from boaviztapi.model.device import DeviceServer


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


def smart_mapper_server(server_dto: Server) -> DeviceServer:
    server_model = DeviceServer()

    if server_dto.configuration is not None:
        if server_dto.configuration.cpu is not None:
            server_model.cpu = smart_mapper_cpu(server_dto.configuration.cpu)

        if server_dto.configuration.ram is not None:
            complete_ram = []
            for ram_dto in server_dto.configuration.ram:
                complete_ram.append(smart_mapper_ram(ram_dto))
            server_model.ram = complete_ram
        if server_dto.configuration.disk is not None:
            complete_disk = []
            for disk_dto in server_dto.configuration.disk:
                if disk_dto.type is None:
                    disk_dto.type = "ssd"
                if disk_dto.type.lower() == "ssd":
                    complete_disk.append(smart_mapper_ssd(disk_dto))
                elif disk_dto.type.lower() == "hdd":
                    complete_disk.append(mapper_hdd(disk_dto))
            server_model.disk = complete_disk
        if server_dto.configuration.power_supply is not None:
            server_model.power_supply = mapper_power_supply(server_dto.configuration.power_supply)

    if server_dto.model is not None and server_dto.model.type is not None:
        server_model.case = ComponentCase()
        if server_dto.model.type == "rack" or server_dto.model.type == "blade":
            server_model.case.case_type.value = server_dto.model.type
            server_model.case.case_type.status = Status.INPUT

    server_model.usage = smart_mapper_usage_server(server_dto.usage or UsageServer())
    complete_components_usage(server_model)

    return server_model


def complete_components_usage(server_model: DeviceServer):
    complete_component_usage(server_model.cpu.usage, server_model.usage)
    complete_component_usage(server_model.case.usage, server_model.usage)
    for ram_unit in server_model.ram:
        complete_component_usage(ram_unit.usage, server_model.usage)
    for disk_unit in server_model.disk:
        complete_component_usage(disk_unit.usage, server_model.usage)


def complete_component_usage(usage_component, usage_device):
    for attr, val in usage_component.__iter__():
        if isinstance(val, Boattribute) and not val.is_set() and usage_device.__getattribute__(attr).is_set():
            usage_component.__setattr__(attr, usage_device.__getattribute__(attr))


class Cloud(Server):
    usage: Optional[UsageCloud] = None
