import os

from typing import Set

import pandas as pd

from api.model.impacts import Impact, Impacts
from api.model.server import Server, Cpu, Ram, Disk
from .impact_factor import impact_factor

_default_impacts_code = {"gwp", "pe", "adp"}

# Data
_cpu_df = pd.read_csv('./api/service/server_impact/bottom_up/cpu.csv')
_ram_df = pd.read_csv('./api/service/server_impact/bottom_up/ram.csv')
_ssd_df = pd.read_csv('./api/service/server_impact/bottom_up/ssd.csv')


# Constants
DEFAULT_CPU_UNITS = 2
DEFAULT_CPU_DIE_SIZE_PER_CORE = 0.245
DEFAULT_CPU_CORE_UNITS = 24

DEFAULT_RAM_UNITS = 2
DEFAULT_RAM_CAPACITY = 32
DEFAULT_RAM_DENSITY = 0.625

DEFAULT_SSD_UNITS = 2
DEFAULT_SSD_CAPACITY = 1000
DEFAULT_SSD_DENSITY = 48.5

DEFAULT_POWER_SUPPLY_NUMBER = 2
DEFAULT_POWER_SUPPLY_WEIGHT = 2.99


def bottom_up_server(server, impact_codes=None):
    if impact_codes is None:
        impact_codes = _default_impacts_code
    # init impacts object
    impacts_list = {}
    for impact_code in impact_codes:
        impacts_list[impact_code] = Impact()

    if server.configuration:
        if server.configuration.cpu:
            cpu = manufacture_cpu(server, impact_codes)
            for impact_code in impact_codes:
                impacts_list[impact_code].add_total(cpu.get(impact_code))
        if server.configuration.ram:
            ram = manufacture_ram(server, impact_codes)
            for impact_code in impact_codes:
                impacts_list[impact_code].add_total(ram.get(impact_code))

        if server.configuration.disk:
            ssd = manufacture_ssd(server, impact_codes)
            for impact_code in impact_codes:
                impacts_list[impact_code].add_total(ssd.get(impact_code))

            hdd = manufacture_hdd(server, impact_codes)
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

    if server.model.type == "rack":
        rack = manufacture_rack(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(rack.get(impact_code))

    elif server.model.type == "blade":
        blade = manufacture_blade(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(blade.get(impact_code))
    # Default blade
    else:
        blade = manufacture_blade(impact_codes)
        for impact_code in impact_codes:
            impacts_list[impact_code].add_total(blade.get(impact_code))

    return Impacts(impacts_list, hypothesis="not implemented")


def smart_complete_data_cpu(cpu: Cpu) -> Cpu:
    # We have all the data required
    if cpu.die_size_per_core and cpu.core_units:
        return cpu

    elif cpu.die_size and cpu.core_units:
        cpu.die_size_per_core = cpu.die_size / cpu.core_units
        return cpu

    # Let's infer the data
    else:
        sub = _cpu_df

        if cpu.manufacturer:
            sub = sub[sub['manufacturer'] == cpu.manufacturer]

        if cpu.family:
            sub = sub[sub['family'] == cpu.family]

        if cpu.manufacture_date:
            sub = sub[sub['manufacture_date'] == cpu.manufacture_date]

        if cpu.process:
            sub = sub[sub['process'] == cpu.process]

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            return Cpu(
                units=DEFAULT_CPU_UNITS,
                die_size_per_core=DEFAULT_CPU_DIE_SIZE_PER_CORE,
                core_units=DEFAULT_CPU_CORE_UNITS
            )
        elif len(sub) == 1:
            return Cpu(
                units=cpu.units if cpu.units else DEFAULT_CPU_UNITS,
                die_size_per_core=float(sub['die_size_per_core']),
                core_units=int(sub['core_units'])
            )
        else:
            sub['_scope3'] = sub[['core_units', 'die_size_per_core']].apply(lambda x: x[0] * x[1])
            sub = sub.sort_values(by='_scope3', ascending=False)
            row = sub.iloc[0]
            die_size_per_core = float(row['die_size_per_core'])
            core_units = int(row['core_units'])
            return Cpu(
                units=cpu.units if cpu.units else DEFAULT_CPU_UNITS,
                die_size_per_core=die_size_per_core,
                core_units=core_units
            )


def manufacture_cpu(server: Server, impact_codes: Set[str]) -> dict:
    cpu_corrected = smart_complete_data_cpu(server.configuration.cpu)
    server.configuration.cpu = cpu_corrected

    manufacture_cpu_impact = dict()
    for impact_code in impact_codes:
        cpu_die_impact = impact_factor["cpu"][impact_code]["die_impact"]
        cpu_impact = impact_factor["cpu"][impact_code]["impact"]

        impact_manufacture_cpu = cpu_corrected.units \
            * ((cpu_corrected.core_units * cpu_corrected.die_size_per_core + 0.491) * cpu_die_impact + cpu_impact)

        manufacture_cpu_impact[impact_code] = impact_manufacture_cpu
    return manufacture_cpu_impact


def smart_complete_data_ram(ram: Ram) -> Ram:
    if ram.capacity and ram.density:
        return ram
    else:
        sub = _ram_df

        if ram.manufacturer:
            sub = sub[sub['manufacturer'] == ram.manufacturer]

        if ram.process:
            sub = sub[sub['process'] == ram.process]

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            return Ram(
                units=ram.units if ram.units else DEFAULT_RAM_UNITS,
                capacity=ram.capacity if ram.capacity else DEFAULT_RAM_CAPACITY,
                density=DEFAULT_RAM_DENSITY
            )
        elif len(sub) == 1:
            return Ram(
                units=ram.units if ram.units else DEFAULT_RAM_UNITS,
                capacity=ram.capacity if ram.capacity else DEFAULT_RAM_CAPACITY,
                density=float(sub['density'])
            )
        else:
            capacity = ram.capacity if ram.capacity else DEFAULT_RAM_CAPACITY
            sub['_scope3'] = sub['density'].apply(lambda x: capacity / x)
            sub = sub.sort_values(by='_scope3', ascending=False)
            density = float(sub.iloc[0].density)
            return Ram(
                units=ram.units if ram.units else DEFAULT_RAM_UNITS,
                capacity=capacity,
                density=density
            )


def manufacture_ram(server: Server, impact_codes: Set[str]) -> dict:
    ram_corrected = []
    for ram_obj in server.configuration.ram:
        ram_corrected.append(smart_complete_data_ram(ram_obj))
    server.configuration.ram = ram_corrected

    manufacture_ram_impact = {}
    for ram_obj in ram_corrected:
        for impact_code in impact_codes:
            ram_die_impact = impact_factor["ram"][impact_code]["die_impact"]
            ram_impact = impact_factor["ram"][impact_code]["impact"]

            impact_manufacture_ram = \
                ram_obj.units * ((ram_obj.capacity / ram_obj.density) * ram_die_impact + ram_impact)

            manufacture_ram_impact[impact_code] = manufacture_ram_impact.get(impact_code, 0) + impact_manufacture_ram

    return manufacture_ram_impact


def smart_complete_data_ssd(ssd: Disk) -> Disk:
    if ssd.capacity and ssd.density:
        return ssd
    else:
        sub = _ssd_df

        if ssd.manufacturer:
            sub = sub[sub['manufacturer'] == ssd.manufacturer]

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            return Disk(
                units=ssd.units if ssd.units else DEFAULT_SSD_UNITS,
                type='ssd',
                capacity=ssd.capacity if ssd.capacity else DEFAULT_SSD_CAPACITY,
                density=ssd.density if ssd.density else DEFAULT_RAM_DENSITY
            )
        elif len(sub) == 1:
            return Disk(
                units=ssd.units if ssd.units else DEFAULT_SSD_UNITS,
                type='ssd',
                capacity=ssd.capacity if ssd.capacity else DEFAULT_SSD_CAPACITY,
                density=float(sub['density'])
            )
        else:
            capacity = ssd.capacity if ssd.capacity else DEFAULT_SSD_CAPACITY
            sub['_scope3'] = sub['density'].apply(lambda x: capacity / x)
            sub = sub.sort_values(by='_scope3', ascending=False)
            density = float(sub.iloc[0].density)
            return Disk(
                units=ssd.units if ssd.units else DEFAULT_RAM_UNITS,
                type='ssd',
                capacity=capacity,
                density=density
            )


def manufacture_ssd(server: Server, impact_codes: Set[str]) -> dict:
    disk_ids = []
    ssd_corrected = []
    for i, disk in enumerate(server.configuration.disk):
        if disk.type.lower() == 'ssd':
            ssd_corrected.append(smart_complete_data_ssd(disk))
            disk_ids.append(i)

    # Replace SSDs
    for i in sorted(disk_ids, reverse=True):
        del server.configuration.disk[i]
    server.configuration.disk += ssd_corrected

    manufacture_ssd_impacts = {}
    for ssd in ssd_corrected:
        for impact_code in impact_codes:
            ssd_die_impact = impact_factor["ssd"][impact_code]["die_impact"]
            ssd_disk_impact = impact_factor["ssd"][impact_code]["impact"]

            impact_manufacture_ssd = \
                ssd.units * ((ssd.capacity / ssd.density) * ssd_die_impact + ssd_disk_impact)

            manufacture_ssd_impacts[impact_code] = impact_manufacture_ssd
    return manufacture_ssd_impacts


def manufacture_hdd(server: Server, impact_codes: Set[str]) -> dict:
    hdd_drive_number = sum([1 for disk in server.configuration.disk if disk.type.lower() == 'hdd'])

    manufacture_hdd_impacts = {}
    for impact_code in impact_codes:
        hdd_disk_impact = impact_factor["hdd"][impact_code]["impact"]
        impact_manufacture_hdd = hdd_drive_number * hdd_disk_impact
        manufacture_hdd_impacts[impact_code] = impact_manufacture_hdd

    return manufacture_hdd_impacts


def manufacture_motherboard(impact_codes: Set[str]) -> dict:
    manufacture_motherboard_impacts = {}

    for impact_code in impact_codes:
        motherboard_impact = impact_factor["motherboard"][impact_code]["impact"]
        manufacture_motherboard_impacts[impact_code] = motherboard_impact

    return manufacture_motherboard_impacts


def manufacture_power_supply(server: Server, impact_codes: Set[str]):
    power_supply_number = server.configuration.power_supply.units \
        if server.configuration.power_supply.units is not None else \
        DEFAULT_POWER_SUPPLY_NUMBER

    power_supply_weight = server.configuration.power_supply.unit_weight \
        if server.configuration.power_supply.unit_weight is not None else \
        DEFAULT_POWER_SUPPLY_WEIGHT

    manufacture_power_supply_impacts = {}
    for impact_code in impact_codes:
        power_supply_impact = impact_factor["power_supply_unit"][impact_code]["impact"]
        manufacture_power_supply_gwp = power_supply_number * power_supply_weight * power_supply_impact
        manufacture_power_supply_impacts[impact_code] = manufacture_power_supply_gwp

    return manufacture_power_supply_impacts


def manufacture_server_assembly(impact_codes: Set[str]):

    server_assembly_impacts = {}

    for impact_code in impact_codes:
        server_assembly_gwp_impact = impact_factor["power_supply_unit"][impact_code]["impact"]
        server_assembly_impacts[impact_code] = server_assembly_gwp_impact

    return server_assembly_impacts


def manufacture_rack(impact_codes: Set[str]):

    rack_impacts = {}

    for impact_code in impact_codes:
        manufacture_rack_impact = impact_factor["rack_server"][impact_code]["impact"]
        rack_impacts[impact_code] = manufacture_rack_impact

    return rack_impacts


def manufacture_blade(impact_codes: Set[str]):

    blade_impacts = {}

    for impact_code in impact_codes:
        blade_slots_impact = impact_factor["blade_16_slots"][impact_code]["impact"]
        blade_impact = impact_factor["blade_server"][impact_code]["impact"]
        manufacture_blade_gwp_impact = (1 / 16) * blade_slots_impact + blade_impact
        blade_impacts[impact_code] = manufacture_blade_gwp_impact

    return blade_impacts
