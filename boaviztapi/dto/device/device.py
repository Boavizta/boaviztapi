from typing import Optional, List

from fastapi import HTTPException

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
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.services.cloud_instance import ServiceCloudInstance
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_server_archetype, get_arch_component, get_cloud_instance_archetype, \
    get_arch_value


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
    complete_components_usage(server_model, server_model.usage)

    return server_model


def complete_components_usage(model: DeviceServer, usage: ModelUsage):
    complete_usage(model.cpu.usage, usage)
    complete_usage(model.case.usage, usage)
    for ram_unit in model.ram:
        complete_usage(ram_unit.usage, usage)
    for disk_unit in model.disk:
        complete_usage(disk_unit.usage, usage)


def complete_usage(usage_component, usage_device):
    if usage_device.avg_power.is_set():
        return
    for attr, val in usage_component.__iter__():
        if isinstance(val, Boattribute) and not val.is_set() and usage_device.__getattribute__(attr).is_set():
            usage_component.__setattr__(attr, usage_device.__getattribute__(attr))


class Cloud(Server):
    provider: Optional[str] = None
    instance_type: Optional[str] = None
    usage: Optional[UsageCloud] = None


def mapper_cloud_instance(cloud_dto: Cloud, archetype=get_cloud_instance_archetype(config["default_cloud_instance"], config["default_cloud_provider"])) -> ServiceCloudInstance:
    if get_server_archetype(archetype_name=get_arch_value(archetype, 'platform', 'default')) is False:
        raise HTTPException(status_code=404, detail=f"Cloud platform {get_arch_value(archetype, 'platform', 'default')} not found. Please add it to the server archetypes. For more information, please check the documentation https://doc.api.boavizta.org/contributing/server/.")

    model_cloud_instance = ServiceCloudInstance(archetype=archetype)

    model_cloud_instance.usage = mapper_usage_cloud(cloud_dto.usage or UsageCloud(), archetype=get_arch_component(model_cloud_instance.archetype, "USAGE"))

    complete_components_usage(model_cloud_instance.platform, model_cloud_instance.usage)
    complete_usage(model_cloud_instance.platform.usage, model_cloud_instance.usage)

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