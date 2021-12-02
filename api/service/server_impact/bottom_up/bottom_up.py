import pandas as pd

from api.model.impacts import Impact, Impacts
from .impact_factor import impact_factor

_default_impacts_code = {"gwp", "pe", "adp"}

# Data
_cpu_df = pd.read_csv('cpu.csv')
_ram_df = pd.read_csv('ram.csv')
_ssd_df = pd.read_csv('ssd.csv')


def bottom_up_server(server, impact_codes=None):
    if impact_codes is None:
        impact_codes = _default_impacts_code
    # init impacts object
    impacts_list = {}
    for impact_code in impact_codes:
        impacts_list[impact_code] = Impact()

    cpu = manufacture_CPU(server, impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(cpu.get(impact_code))

    ram = manufacture_RAM(server, impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(ram.get(impact_code))

    ssd = manufacture_SSD(server, impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(ssd.get(impact_code))

    hdd = manufacture_HDD(server, impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(hdd.get(impact_code))

    motherboard = manufacture_motherboard(impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(motherboard.get(impact_code))

    power_supply = manufacture_power_supply(server, impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(power_supply.get(impact_code))

    server_assembly = manufacture_server_assembly(impact_codes)
    for impact_code in impact_codes:
        impacts_list[impact_code].add_total(server_assembly.get(impact_code))

    if server.type == "rack":
        rack = manufacture_rack(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(rack.get(impact_code))
    elif server.type == "blade":
        blade = manufacture_blade(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(blade.get(impact_code))
    # Default blade
    else:
        blade = manufacture_blade(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(blade.get(impact_code))

    return Impacts(impacts_list, hypothesis="not implemented")


def manufacture_CPU(server, impact_codes):
    cpu_core_number = server.cpu_number if server.cpu_number is not None else get_cpu_core_number(server)
    die_size_per_core = server.cpu_die if server.cpu_die is not None else get_cpu_die(server)
    cpu_number = server.cpu_number if server.cpu_number is not None else get_cpu_number(server)
    manufacture_cpu_impact = {}

    for impact_code in impact_codes:
        cpu_die_impact = impact_factor["cpu"][impact_code]["die_impact"]
        cpu_impact = impact_factor["cpu"][impact_code]["impact"]

        impact_manufacture_cpu = \
            cpu_number * ((cpu_core_number * die_size_per_core + 0.491) * cpu_die_impact + cpu_impact)

        manufacture_cpu_impact[impact_code] = impact_manufacture_cpu

    return manufacture_cpu_impact


def get_cpu_die(server):
    # TODO bring intelligence
    # default value from the methodology
    return 0.245


def get_cpu_core_number(server):
    # TODO bring intelligence
    # Mean from the dataset
    return 13


def get_cpu_number(server):
    # TODO bring intelligence
    # Randomly chosen
    return 2


def manufacture_RAM(server, impact_codes):
    ram_strip_quantity = server.ram_strip_quantity if server.cpu_number is not None else get_ram_strip_quantity(server)
    ram_storage_density = server.cpu_die if server.cpu_die is not None else get_ram_storage_density(server)
    ram_capacity = server.ram_capacity if server.cpu_number is not None else get_ram_capacity(server)

    manufacture_ram_impact = {}

    for impact_code in impact_codes:
        ram_die_impact = impact_factor["ram"][impact_code]["die_impact"]
        ram_impact = impact_factor["ram"][impact_code]["impact"]

        impact_manufacture_ram = \
            ram_strip_quantity * ((ram_capacity / ram_storage_density) * ram_die_impact + ram_impact)

        manufacture_ram_impact[impact_code] = impact_manufacture_ram

    return manufacture_ram_impact


def get_ram_strip_quantity(server):
    # TODO bring intelligence
    # Randomly chosen
    return 2


def get_ram_storage_density(server):
    # TODO bring intelligence
    # Default value from the methodology
    return 1.79


def get_ram_capacity(server):
    # TODO bring intelligence
    # Randomly chosen
    return 32


def manufacture_SSD(server, impact_codes):
    ssd_capacity = server.ssd_capacity if server.cpu_number is not None else get_ssd_strip_quantity(server)
    ssd_storage_density = server.ssd_die if server.cpu_die is not None else get_ssd_storage_density(server)
    ssd_number = server.ssd_quantity if server.cpu_number is not None else get_ssd_capacity(server)

    manufacture_ssd_impacts = {}

    for impact_code in impact_codes:
        ssd_die_impact = impact_factor["ssd"][impact_code]["die_impact"]
        ssd_disk_impact = impact_factor["ssd"][impact_code]["impact"]

        impact_manufacture_ssd = \
            ssd_number * ((ssd_capacity / ssd_storage_density) * ssd_die_impact + ssd_disk_impact)

        manufacture_ssd_impacts[impact_code] = impact_manufacture_ssd

    return manufacture_ssd_impacts


def get_ssd_strip_quantity(server):
    # TODO bring intelligence
    # Randomly chosen
    return 2


def get_ssd_storage_density(server):
    # TODO bring intelligence
    # Default value from the methodology
    return 50.6


def get_ssd_capacity(server):
    # TODO bring intelligence
    # Randomly chosen
    return 1000


def manufacture_HDD(server, impact_codes):
    hdd_drive_number = server.hdd_number if server.hdd_number is not None else get_hdd_number(server)

    manufacture_hdd_impacts = {}

    for impact_code in impact_codes:
        hdd_disk_impact = impact_factor["hdd"][impact_code]["impact"]
        impact_manufacture_hdd = hdd_drive_number * hdd_disk_impact
        manufacture_hdd_impacts[impact_code] = impact_manufacture_hdd

    return manufacture_hdd_impacts


def get_hdd_number(server):
    return 2


def manufacture_motherboard(impact_codes):
    manufacture_motherboard_impacts = {}

    for impact_code in impact_codes:
        motherboard_impact = impact_factor["motherboard"][impact_code]["impact"]
        manufacture_motherboard_impacts[impact_code] = motherboard_impact

    return manufacture_motherboard_impacts


def manufacture_power_supply(server, impact_codes):
    power_supply_number = server.power_supply_number if server.power_supply_number is not None else \
        get_power_supply_number(server)
    power_supply_weight = server.power_supply_weight if server.power_supply_number is not None else \
        get_power_supply_weight(server)

    manufacture_power_supply_impacts = {}

    for impact_code in impact_codes:
        power_supply_impact = impact_factor["power_supply_unit"][impact_code]["impact"]
        manufacture_power_supply_gwp = power_supply_number * power_supply_weight * power_supply_impact
        manufacture_power_supply_impacts[impact_code] = manufacture_power_supply_gwp

    return manufacture_power_supply_impacts


def get_power_supply_number(server):
    # TODO bring intelligence
    # Randomly chosen
    return 2


def get_power_supply_weight(server):
    return 20


def manufacture_server_assembly(impact_codes):

    server_assembly_impacts = {}

    for impact_code in impact_codes:
        server_assembly_gwp_impact = impact_factor["power_supply_unit"][impact_code]["impact"]
        server_assembly_impacts[impact_code] = server_assembly_gwp_impact

    return server_assembly_impacts


def manufacture_rack(impact_codes):

    rack_impacts = {}

    for impact_code in impact_codes:
        manufacture_rack_impact = impact_factor["rack_server"][impact_code]["impact"]
        rack_impacts[impact_code] = manufacture_rack_impact

    return rack_impacts


def manufacture_blade(impact_codes):

    blade_impacts = {}

    for impact_code in impact_codes:
        blade_slots_impact = impact_factor["blade_16_slots"][impact_code]["impact"]
        blade_impact = impact_factor["blade_server"][impact_code]["impact"]
        manufacture_blade_gwp_impact = (1 / 16) * blade_slots_impact + blade_impact
        blade_impacts[impact_code] = manufacture_blade_gwp_impact

    return blade_impacts
