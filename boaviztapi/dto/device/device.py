from typing import Optional, List

from boaviztapi import config
from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply
from boaviztapi.dto.component.cpu import mapper_cpu
from boaviztapi.dto.component.disk import mapper_ssd, mapper_hdd
from boaviztapi.dto.component.other import mapper_power_supply
from boaviztapi.dto.component.ram import mapper_ram
from boaviztapi.dto.usage import UsageServer, UsageCloud
from boaviztapi.dto import BaseDTO
from boaviztapi.dto.usage.usage import mapper_usage_server, mapper_usage_cloud
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.component import ComponentCase
from boaviztapi.model.device import DeviceServer, DeviceCloudInstance
from boaviztapi.service.archetype import get_server_archetype, get_arch_component, get_cloud_instance_archetype


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


def mapper_server(server_dto: Server, archetype=get_server_archetype(config["default_server"])) -> DeviceServer:
    server_model = DeviceServer(archetype=archetype)

    server_model = device_mapper(server_dto, server_model)

    server_model.usage = mapper_usage_server(server_dto.usage or UsageServer(), archetype=get_arch_component(server_model.archetype,"USAGE"))
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
    if usage_device.avg_power.is_set():
        return
    for attr, val in usage_component.__iter__():
        if isinstance(val, Boattribute) and not val.is_set() and usage_device.__getattribute__(attr).is_set():
            usage_component.__setattr__(attr, usage_device.__getattribute__(attr))

class Cloud(Server):
    provider: Optional[str] = None
    instance_type: Optional[str] = None
    usage: Optional[UsageCloud] = None

def mapper_cloud_instance(cloud_dto: Cloud, archetype=get_cloud_instance_archetype(config["default_cloud"], config["default_cloud_provider"])) -> DeviceCloudInstance:
    model_cloud_instance = DeviceCloudInstance(archetype=archetype)

    model_cloud_instance = device_mapper(cloud_dto, model_cloud_instance)

    model_cloud_instance.usage = mapper_usage_cloud(cloud_dto.usage or UsageCloud(), archetype=get_arch_component(model_cloud_instance.archetype, "USAGE"))

    complete_component_usage(model_cloud_instance.cpu.usage, model_cloud_instance.usage)
    for ram_unit in model_cloud_instance.ram:
        complete_component_usage(ram_unit.usage, model_cloud_instance.usage)

    return model_cloud_instance


def device_mapper(device_dto, device_model):
    if device_dto.configuration is not None:
        if device_dto.configuration.cpu is not None:
            device_model.cpu = mapper_cpu(device_dto.configuration.cpu, archetype=get_arch_component(device_model.archetype, "CPU"))

        if device_dto.configuration.ram is not None:
            complete_ram = []
            for ram_dto in device_dto.configuration.ram:
                complete_ram.append(mapper_ram(ram_dto, archetype=get_arch_component(device_model.archetype, "RAM")))
            device_model.ram = complete_ram
        if device_dto.configuration.disk is not None:
            complete_disk = []
            for disk_dto in device_dto.configuration.disk:
                if disk_dto.type is None:
                    disk_dto.type = "ssd"
                if disk_dto.type.lower() == "ssd":
                    complete_disk.append(mapper_ssd(disk_dto, archetype=get_arch_component(device_model.archetype, "SSD")))
                elif disk_dto.type.lower() == "hdd":
                    complete_disk.append(mapper_hdd(disk_dto, archetype=get_arch_component(device_model.archetype, "HDD")))
            device_model.disk = complete_disk
        if device_dto.configuration.power_supply is not None:
            device_model.power_supply = mapper_power_supply(device_dto.configuration.power_supply, archetype=get_arch_component(device_model.archetype, "POWER_SUPPLY"))

    if device_dto.model is not None and device_dto.model.type is not None:
        device_model.case = ComponentCase(archetype=get_arch_component(device_model.archetype, "CASE"))
        if device_dto.model.type == "rack" or device_dto.model.type == "blade":
            device_model.case.case_type.value = device_dto.model.type
            device_model.case.case_type.status = Status.INPUT

    return device_model