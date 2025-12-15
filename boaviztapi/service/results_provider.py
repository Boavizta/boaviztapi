from boaviztapi import config
from boaviztapi.dto.component import Disk, PowerSupply, RAM, CPU
from boaviztapi.dto.device.device import device_mapper, Server, ConfigurationServer, ModelServer, Cloud
from boaviztapi.dto.usage import UsageServer, UsageCloud
from boaviztapi.dto.usage.usage import WorkloadTime
from boaviztapi.model.crud_models.configuration_model import ConfigurationModel, OnPremiseConfigurationModel, \
    CloudConfigurationModel
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.service.archetype import get_server_archetype
from boaviztapi.service.costs_provider import ElectricityCostsProvider


def mapper_config_to_server(onprem: ConfigurationModel) -> Server | Cloud:
    boavizta_config = None
    if onprem.type == 'on-premise':
        boavizta_config = _map_onpremise_to_boaviztaserver(onprem)
    if onprem.type == 'cloud':
        boavizta_config = _map_cloud_to_boaviztaserver(onprem)

    if boavizta_config is None:
        raise ValueError("Invalid configuration type")


    return boavizta_config


def _map_onpremise_to_boaviztaserver(onprem : OnPremiseConfigurationModel) -> Server:
    boavizta_server = Server()

    cpu = CPU()
    cpu.units = onprem.cpu_quantity
    cpu.core_units = onprem.cpu_core_units
    cpu.family = onprem.cpu_architecture
    cpu.tdp = onprem.cpu_tdp

    ram = RAM()
    ram.units = onprem.ram_quantity
    ram.capacity = onprem.ram_capacity
    ram.manufacturer = onprem.ram_manufacturer

    ssd = Disk()
    ssd.units = onprem.ssd_quantity
    ssd.capacity = onprem.ssd_capacity
    ssd.manufacturer = onprem.ssd_manufacturer

    hdd = Disk()
    hdd.units = onprem.hdd_quantity
    hdd.capacity = onprem.ssd_capacity #FIXME: This is also the same in Boavizta... there is no setting for hdd capacity

    power_supply = PowerSupply()
    power_supply.units = onprem.psu_quantity


    model_server = ModelServer()
    model_server.name = onprem.name
    model_server.type = onprem.server_type

    boavizta_server.model = model_server
    boavizta_server.configuration = ConfigurationServer(cpu=cpu, ram=[ram], disk=[hdd, ssd], power_supply=power_supply)

    usage = UsageServer()
    usage.use_time_ratio = onprem.usage.serverLoad / 100 if onprem.usage.serverLoad is not None else 1
    usage.hours_life_time = onprem.usage.lifespan
    usage.avg_power = None  #FIXME - This is a good fix to get similar results to Boavizta, however, we should see if it can be removed altogether.

    if onprem.usage.serverLoadAdvanced is not None:
        slot1 = WorkloadTime(time_percentage=onprem.usage.serverLoadAdvanced.slot1.time,
                             load_percentage=onprem.usage.serverLoadAdvanced.slot1.load)
        slot2 = WorkloadTime(time_percentage=onprem.usage.serverLoadAdvanced.slot2.time,
                             load_percentage=onprem.usage.serverLoadAdvanced.slot2.load)
        slot3 = WorkloadTime(time_percentage=onprem.usage.serverLoadAdvanced.slot3.time,
                             load_percentage=onprem.usage.serverLoadAdvanced.slot3.load)
        usage.time_workload = [slot1, slot2, slot3]

    usage.usage_location = _get_country_alpha3_from_zone_code(onprem.usage.localisation)

    boavizta_server.usage = usage
    return boavizta_server

def _map_cloud_to_boaviztaserver(cloud : CloudConfigurationModel) -> Cloud:
    boavizta_cloud = Cloud()

    boavizta_cloud.provider = cloud.cloud_provider
    boavizta_cloud.instance_type = cloud.instance_type

    usage = UsageCloud()
    usage.use_time_ratio = cloud.usage.serverLoad / 100 if cloud.usage.serverLoad is not None else 1
    usage.hours_life_time = cloud.usage.lifespan
    if cloud.usage.serverLoadAdvanced is not None:
        slot1 = WorkloadTime(time_percentage=cloud.usage.serverLoadAdvanced.slot1.time,
                             load_percentage=cloud.usage.serverLoadAdvanced.slot1.load)
        slot2 = WorkloadTime(time_percentage=cloud.usage.serverLoadAdvanced.slot2.time,
                             load_percentage=cloud.usage.serverLoadAdvanced.slot2.load)
        slot3 = WorkloadTime(time_percentage=cloud.usage.serverLoadAdvanced.slot3.time,
                             load_percentage=cloud.usage.serverLoadAdvanced.slot3.load)
        usage.time_workload = [slot1, slot2, slot3]

    usage.usage_location = _get_country_alpha3_from_zone_code(cloud.usage.localisation)

    boavizta_cloud.usage = usage
    return boavizta_cloud

def _get_country_alpha3_from_zone_code(zone_code: str) -> str:
    supported_countries = ElectricityCostsProvider.get_eic_countries()
    for country in supported_countries:
        if country.zone_code == zone_code:
            return country.alpha_3
    return "WOR"