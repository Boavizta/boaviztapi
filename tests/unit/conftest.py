import pytest

from boaviztapi.dto.server_dto import ServerDTO, CloudDTO
from boaviztapi.model.components.component import ComponentRAM, ComponentSSD, ComponentHDD, ComponentAssembly, \
    ComponentCase, ComponentMotherBoard, ComponentPowerSupply, ComponentCPU
from tests.unit import data_dir


@pytest.fixture(scope="function")
def dell_r740():
    return ServerDTO.parse_file(data_dir + "/devices/server/dellR740.json").to_device()


@pytest.fixture(scope="function")
def empty_server():
    return ServerDTO.parse_obj({}).to_device()


@pytest.fixture(scope="function")
def incomplete_server():
    return ServerDTO.parse_file(data_dir + "/devices/server/incomplete.json").to_device()


@pytest.fixture(scope="function")
def completed_server_with_default():
    completed_server = ServerDTO.parse_file(data_dir + "/devices/server/incomplete.json").to_device()
    completed_server.smart_complete_data()
    return completed_server


@pytest.fixture(scope="function")
def completed_server_with_dellr740():
    completed_server_with_dellr740 = \
        ServerDTO.parse_file(data_dir + "/devices/server/completed_server_with_dellr740.json").to_device()
    return completed_server_with_dellr740


@pytest.fixture(scope="function")
def complete_cpu():
    return ComponentCPU.parse_obj({
        "core_units": 12,
        "die_size_per_core": 0.245
    })


@pytest.fixture(scope="function")
def empty_cpu():
    return ComponentCPU.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_cpu():
    return ComponentCPU.parse_obj({
        "core_units": 12,
        "family": "Skylake",
        "manufacture_date": 2017
    })


@pytest.fixture(scope="function")
def complete_ram():
    return ComponentRAM.parse_obj({
        "units": 12,
        "capacity": 32,
        "density": 1.79
    })


@pytest.fixture(scope="function")
def empty_ram():
    return ComponentRAM.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_ram():
    return ComponentRAM.parse_obj({
        "manufacturer": "Samsung",
        "process": 30
    })


@pytest.fixture(scope="function")
def complete_ssd():
    return ComponentSSD.parse_obj({
        "capacity": 400,
        "density": 50.6
    })


@pytest.fixture(scope="function")
def empty_ssd():
    return ComponentSSD.parse_obj({})


@pytest.fixture(scope="function")
def incomplete_ssd():
    return ComponentSSD.parse_obj({
        "manufacturer": "Samsung"
    })


@pytest.fixture(scope="function")
def hdd():
    return ComponentHDD.parse_obj({})


@pytest.fixture(scope="session")
def assembly():
    return ComponentAssembly.parse_obj({})


@pytest.fixture(scope="function")
def empty_case():
    return ComponentCase.parse_obj({})


@pytest.fixture(scope="function")
def blade_case():
    case = ComponentCase.parse_obj({})
    case.case_type = "blade"
    return case


@pytest.fixture(scope="function")
def motherboard():
    return ComponentMotherBoard.parse_obj({})


@pytest.fixture(scope="function")
def empty_power_supply():
    return ComponentPowerSupply.parse_obj({})


@pytest.fixture(scope="function")
def complete_power_supply():
    return ComponentPowerSupply.parse_obj({
        "unit_weight": 2
    })


@pytest.fixture(scope="function")
def cloud_instance_1():
    cloud_server = CloudDTO.parse_file(data_dir + "/devices/cloud/cloud_instance_1.json").to_device()
    return cloud_server


@pytest.fixture(scope="function")
def incomplete_usage():
    incomplete_usage = CloudDTO.parse_file(data_dir + "/devices/cloud/incomplete_usage.json").to_device()
    return incomplete_usage


@pytest.fixture(scope="function")
def complete_usage():
    complete_usage = CloudDTO.parse_file(data_dir + "/devices/cloud/complete_usage.json").to_device()
    complete_usage.usage
    return complete_usage


@pytest.fixture(scope="function")
def cloud_instance_1_completed():
    cloud_instance_1_completed = \
        CloudDTO.parse_file(data_dir + "/devices/cloud/cloud_instance_1_completed.json").to_device()
    return cloud_instance_1_completed
