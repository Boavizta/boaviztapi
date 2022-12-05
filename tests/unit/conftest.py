import os

import pandas as pd
import pytest

from boaviztapi.dto.component import CPU, RAM, Disk, Case, Motherboard, PowerSupply
from boaviztapi.dto.device import Server
from boaviztapi.dto.usage import UsageServer
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, ComponentCase, \
    ComponentMotherboard, ComponentPowerSupply, ComponentAssembly
from boaviztapi.model.device import DeviceServer
from boaviztapi.model.usage import ModelUsageServer
from tests.unit import data_dir


# MODEL

@pytest.fixture(scope="function")
def dell_r740_model(rack_case_model, complete_cpu_model, complete_ram_model, complete_ssd_model,
                    complete_power_supply_model):
    server = DeviceServer()

    server.case = rack_case_model
    server.cpu = complete_cpu_model
    server.ram = [complete_ram_model]
    server.disk = [complete_ssd_model]
    server.power_supply = complete_power_supply_model
    server.usage = ModelUsageServer()

    return server


@pytest.fixture(scope="function")
def empty_server_model():
    return DeviceServer()


@pytest.fixture(scope="function")
def incomplete_server_model(rack_case_model, complete_ram_model_2, complete_ssd_model):
    server = DeviceServer()

    server.case = rack_case_model
    server.ram = [complete_ram_model_2]
    server.disk = [complete_ssd_model]
    server.usage = ModelUsageServer()

    return server


@pytest.fixture(scope="function")
def completed_server_with_dellr740_model(rack_case_model, complete_cpu_model, complete_ram_model_2,
                                         complete_ssd_model_2, complete_power_supply_model):
    server = DeviceServer()

    server.case = rack_case_model
    server.cpu = complete_cpu_model
    server.ram = [complete_ram_model_2]
    server.disk = [complete_ssd_model_2]
    server.power_supply = complete_power_supply_model
    server.usage = ModelUsageServer()

    return server


@pytest.fixture(scope="function")
def complete_cpu_model():
    cpu = ComponentCPU()

    cpu.units = 2

    cpu.core_units.value = 24
    cpu.core_units.status = Status.INPUT

    cpu.die_size_per_core.value = 0.245
    cpu.die_size_per_core.status = Status.INPUT

    return cpu


@pytest.fixture(scope="function")
def empty_cpu_model():
    return ComponentCPU()


@pytest.fixture(scope="function")
def incomplete_cpu_model():
    cpu = ComponentCPU()

    cpu.core_units.value = 12
    cpu.core_units.status = Status.INPUT

    cpu.family.value = "Skylake"
    cpu.family.status = Status.INPUT

    cpu.die_size_per_core.value = 0.404
    cpu.die_size_per_core.status = Status.COMPLETED

    return cpu


@pytest.fixture(scope="function")
def complete_ram_model():
    ram = ComponentRAM()

    ram.units = 12
    ram.capacity.value = 32
    ram.capacity.status = Status.INPUT

    ram.density.value = 1.79
    ram.density.status = Status.INPUT

    return ram


@pytest.fixture(scope="function")
def empty_ram_model():
    return ComponentRAM()


@pytest.fixture(scope="function")
def incomplete_ram_model():
    ram = ComponentRAM()

    ram.units = 12
    ram.manufacturer.value = "Samsung"
    ram.manufacturer.status = Status.INPUT

    ram.process.value = 30
    ram.process.status = Status.INPUT

    ram.density.value = 0.625
    ram.density.status = Status.COMPLETED

    return ram


@pytest.fixture(scope="function")
def complete_ram_model_2():
    ram = ComponentRAM()

    ram.units = 24
    ram.capacity.value = 32
    ram.capacity.status = Status.INPUT

    ram.density.value = 1.79
    ram.density.status = Status.INPUT

    return ram


@pytest.fixture(scope="function")
def complete_ssd_model():
    ssd = ComponentSSD()

    ssd.capacity.value = 400
    ssd.capacity.status = Status.INPUT

    ssd.density.value = 50.6
    ssd.density.status = Status.INPUT

    return ssd


@pytest.fixture(scope="function")
def complete_ssd_model_2():
    ssd = ComponentSSD()
    ssd.units = 2
    ssd.capacity.value = 400
    ssd.capacity.status = Status.INPUT

    ssd.density.value = 50.6
    ssd.density.status = Status.INPUT

    return ssd


@pytest.fixture(scope="function")
def empty_ssd_model():
    return ComponentSSD()


@pytest.fixture(scope="function")
def incomplete_ssd_model():
    ssd = ComponentSSD()

    ssd.manufacturer.value = "Samsung"
    ssd.manufacturer.status = Status.INPUT

    ssd.density.value = 53.6
    ssd.density.status = Status.COMPLETED

    return ssd


@pytest.fixture(scope="function")
def hdd_model():
    return ComponentHDD()


@pytest.fixture(scope="function")
def empty_case_model():
    return ComponentCase()


@pytest.fixture(scope="function")
def blade_case_model():
    case = ComponentCase()

    case.case_type.value = "blade"
    case.case_type.status = Status.INPUT

    return case


@pytest.fixture(scope="function")
def rack_case_model():
    case = ComponentCase()

    case.case_type.value = "rack"
    case.case_type.value = Status.INPUT

    return case


@pytest.fixture(scope="function")
def motherboard_model():
    return ComponentMotherboard()


@pytest.fixture(scope="function")
def empty_power_supply_model():
    return ComponentPowerSupply()


@pytest.fixture(scope="function")
def complete_power_supply_model():
    power_supply = ComponentPowerSupply()

    power_supply.units = 2

    power_supply.unit_weight.value = 2.99
    power_supply.unit_weight.status = Status.INPUT

    return power_supply


@pytest.fixture(scope="function")
def assembly_model():
    return ComponentAssembly()


# DTO

@pytest.fixture(scope="function")
def dell_r740_dto():
    return Server.parse_obj(Server.parse_file(data_dir + "/devices/server/dellR740.json"))


@pytest.fixture(scope="function")
def empty_server_dto():
    return Server.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_server_dto():
    return Server.parse_file(data_dir + "/devices/server/incomplete.json")


@pytest.fixture(scope="function")
def completed_server_with_dellr740_dto():
    return Server.parse_file(data_dir + "/devices/server/completed_server_with_dellr740.json")


@pytest.fixture(scope="function")
def complete_cpu_dto():
    return CPU.parse_obj({
        "units": 2,
        "core_units": 24,
        "die_size_per_core": 0.245
    })


@pytest.fixture(scope="function")
def empty_cpu_dto():
    return CPU.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_cpu_dto():
    return CPU.parse_obj({
        "core_units": 12,
        "family": "Skylake",
        "manufacture_date": 2017
    })


@pytest.fixture(scope="function")
def complete_ram_dto():
    return RAM.parse_obj({
        "units": 12,
        "capacity": 32,
        "density": 1.79
    })


@pytest.fixture(scope="function")
def empty_ram_dto():
    return RAM.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_ram():
    return RAM.parse_obj({
        "manufacturer": "Samsung",
        "process": 30
    })


@pytest.fixture(scope="function")
def complete_ssd_dto():
    return Disk.parse_obj({
        "capacity": 400,
        "density": 50.6,
        "type": "ssd"
    })


@pytest.fixture(scope="function")
def empty_ssd_dto():
    return Disk.parse_obj({"type": "ssd"})


@pytest.fixture(scope="function")
def incomplete_ssd_dto():
    return Disk.parse_obj({
        "manufacturer": "Samsung",
        "type": "ssd"
    })


@pytest.fixture(scope="function")
def hdd():
    return Disk.parse_obj({"type": "hdd"})


@pytest.fixture(scope="function")
def empty_case_dto():
    return Case.parse_obj({})


@pytest.fixture(scope="function")
def blade_case_dto():
    case = Case.parse_obj({})
    case.case_type = "blade"
    return case


@pytest.fixture(scope="function")
def motherboard_dto():
    return Motherboard.parse_obj({})


@pytest.fixture(scope="function")
def empty_power_supply_dto():
    return PowerSupply.parse_obj({})


@pytest.fixture(scope="function")
def complete_power_supply_dto():
    return PowerSupply.parse_obj({
        "unit": 2,
        "unit_weight": 2.99
    })


@pytest.fixture(scope="function")
def cloud_instance_1_dto():
    cloud_server = Server.parse_file(data_dir + "/devices/cloud/cloud_instance_1.json")
    return cloud_server


@pytest.fixture(scope="function")
def incomplete_usage_dto():
    incomplete_usage = Server.parse_file(data_dir + "/devices/cloud/incomplete_usage.json")
    return incomplete_usage


@pytest.fixture(scope="function")
def complete_usage_dto():
    complete_usage = Server.parse_file(data_dir + "/devices/cloud/complete_usage.json")
    return complete_usage


@pytest.fixture(scope="function")
def cloud_instance_1_completed_dto():
    cloud_instance_1_completed = \
        Server.parse_file(data_dir + "/devices/cloud/cloud_instance_1_completed.json")
    return cloud_instance_1_completed


@pytest.fixture(scope="function")
def french_mix_1_kw_dto():
    return UsageServer.parse_obj({
        "usage_location": "FRA",
        "hours_electrical_consumption": 1
    })


@pytest.fixture(scope="function")
def empty_usage_dto():
    return UsageServer.parse_obj({
    })


@pytest.fixture(scope="function")
def cpu_dataframe():
    return pd.read_csv(data_dir + "/csv_components/cpu_manufacture.csv")


@pytest.fixture(scope="function")
def ram_dataframe():
    return pd.read_csv(data_dir + "/csv_components/ram_manufacture.csv")


@pytest.fixture(scope="function")
def ssd_dataframe():
    return pd.read_csv(data_dir + "/csv_components/ssd_manufacture.csv")
