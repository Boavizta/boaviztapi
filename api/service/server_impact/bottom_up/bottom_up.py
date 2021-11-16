from api.model.impacts import Impact
from impact_factor import impact_factor


def bottom_up_server(server):
    # TODO construct impacts object
    gwp = Impact()
    adp = Impact()
    ep = Impact()

    cpu = manufacture_CPU(server)
    gwp.add_total(cpu.get("gwp"))
    adp.add_total(cpu.get("adp"))
    ep.add_total(cpu.get("ep"))

    ram = manufacture_RAM(server)
    gwp.add_total(ram.get("gwp"))
    adp.add_total(ram.get("adp"))
    ep.add_total(ram.get("ep"))

    ssd = manufacture_SSD(server)
    gwp.add_total(ssd.get("gwp"))
    adp.add_total(ssd.get("adp"))
    ep.add_total(ssd.get("ep"))

    hdd = manufacture_HDD(server)
    gwp.add_total(hdd.get("gwp"))
    adp.add_total(hdd.get("adp"))
    ep.add_total(hdd.get("ep"))

    motherboard = manufacture_motherboard(server)
    manufacture_power_supply(server)
    server_assembly(server)

    if server.type == "rack":
        manufacture_rack(server)
    elif server.type == "blade":
        manufacture_blade(server)
    # Default blade
    else:
        manufacture_blade(server)
    pass


def manufacture_CPU(server):
    cpu_core_number = server.cpu_number if server.cpu_number is not None else get_cpu_core_number(server)
    die_size_per_core = server.cpu_die if server.cpu_die is not None else get_cpu_die(server)
    cpu_number = server.cpu_number if server.cpu_number is not None else get_cpu_number(server)

    cpu_die_gwp_impact = impact_factor["cpu"]["gwp"]["die_impact"]
    cpu_gwp_impact = impact_factor["cpu"]["gwp"]["impact"]

    cpu_die_pe_impact = impact_factor["cpu"]["pe"]["die_impact"]
    cpu_pe_impact = impact_factor["cpu"]["pe"]["impact"]

    cpu_die_adp_impact = impact_factor["cpu"]["adp"]["die_impact"]
    cpu_adp_impact = impact_factor["cpu"]["adp"]["impact"]

    gwp_manufacture_cpu = \
        cpu_number * ((cpu_core_number * die_size_per_core + 0.491) * cpu_die_gwp_impact + cpu_gwp_impact)
    pe_manufacture_cpu = \
        cpu_number * ((cpu_core_number * die_size_per_core + 0.491) * cpu_die_pe_impact + cpu_pe_impact)
    adp_manufacture_cpu = \
        cpu_number * ((cpu_core_number * die_size_per_core + 0.491) * cpu_die_adp_impact + cpu_adp_impact)

    manufacture_cpu_impact = {"gwp": gwp_manufacture_cpu, "pe": pe_manufacture_cpu, "adp": adp_manufacture_cpu}

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


def manufacture_RAM(server):
    ram_strip_quantity = server.ram_strip_quantity if server.cpu_number is not None else get_ram_strip_quantity(server)
    ram_storage_density = server.cpu_die if server.cpu_die is not None else get_ram_storage_density(server)
    ram_capacity = server.ram_capacity if server.cpu_number is not None else get_ram_capacity(server)

    ram_die_gwp_impact = impact_factor["ram"]["gwp"]["die_impact"]
    ram_gwp_impact = impact_factor["ram"]["gwp"]["impact"]

    ram_die_pe_impact = impact_factor["ram"]["pe"]["die_impact"]
    ram_pe_impact = impact_factor["ram"]["pe"]["impact"]

    ram_die_adp_impact = impact_factor["ram"]["adp"]["die_impact"]
    ram_adp_impact = impact_factor["ram"]["adp"]["impact"]

    gwp_manufacture_ram = \
        ram_strip_quantity * ((ram_capacity / ram_storage_density) * ram_die_gwp_impact + ram_gwp_impact)
    pe_manufacture_ram = \
        ram_strip_quantity * ((ram_capacity / ram_storage_density) * ram_die_pe_impact + ram_pe_impact)
    adp_manufacture_ram = \
        ram_strip_quantity * ((ram_capacity / ram_storage_density) * ram_die_adp_impact + ram_adp_impact)

    manufacture_ram_impact = {"gwp": gwp_manufacture_ram, "pe": pe_manufacture_ram, "adp": adp_manufacture_ram}

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


def manufacture_SSD(server):
    ssd_capacity = server.ssd_capacity if server.cpu_number is not None else get_ssd_strip_quantity(server)
    ssd_storage_density = server.ssd if server.cpu_die is not None else get_ssd_storage_density(server)
    ssd_number = server.ram_capacity if server.cpu_number is not None else get_ssd_capacity(server)

    ssd_die_gwp_impact = impact_factor["ssd"]["gwp"]["die_impact"]
    ssd_disk_gwp_impact = impact_factor["ssd"]["gwp"]["impact"]

    ssd_die_pe_impact = impact_factor["ssd"]["pe"]["die_impact"]
    ssd_pe_impact = impact_factor["ssd"]["pe"]["impact"]

    ssd_die_adp_impact = impact_factor["ssd"]["adp"]["die_impact"]
    ssd_adp_impact = impact_factor["ssd"]["adp"]["impact"]

    gwp_manufacture_ssd = \
        ssd_number * ((ssd_capacity / ssd_storage_density) * ssd_die_gwp_impact + ssd_disk_gwp_impact)
    pe_manufacture_ssd = \
        ssd_number * ((ssd_capacity / ssd_storage_density) * ssd_die_pe_impact + ssd_pe_impact)
    adp_manufacture_ssd = \
        ssd_number * ((ssd_capacity / ssd_storage_density) * ssd_die_adp_impact + ssd_adp_impact)

    manufacture_ssd_impacts = {"gwp": gwp_manufacture_ssd, "pe": pe_manufacture_ssd, "adp": adp_manufacture_ssd}

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


def manufacture_HDD(server):
    hdd_drive_number = server.hdd_number if server.hdd_number is not None else get_hdd_number(server)

    hdd_gwp_impact = impact_factor["hdd"]["gwp"]["impact"]
    hdd_pe_impact = impact_factor["hdd"]["pe"]["impact"]
    hdd_adp_impact = impact_factor["hdd"]["adp"]["impact"]

    manufacture_hdd_gwp = hdd_drive_number * hdd_gwp_impact
    manufacture_hdd_pe = hdd_drive_number * hdd_pe_impact
    manufacture_hdd_adp = hdd_drive_number * hdd_adp_impact

    manufacture_hdd_impacts = {"gwp": manufacture_hdd_gwp, "pe": manufacture_hdd_pe, "adp": manufacture_hdd_adp}

    return manufacture_hdd_impacts


def get_hdd_number(server):
    return 2


def manufacture_motherboard(server):
    motherboard_gwp_impact = impact_factor["motherboard"]["gwp"]["impact"]
    motherboard_pe_impact = impact_factor["motherboard"]["pe"]["impact"]
    motherboard_adp_impact = impact_factor["motherboard"]["adp"]["impact"]

    manufacture_motherboard_impacts = {"gwp": motherboard_gwp_impact, "pe": motherboard_pe_impact,
                                       "adp": motherboard_adp_impact}

    return manufacture_motherboard_impacts


def manufacture_power_supply(server):
    power_supply_number = server.power_supply_number if server.power_supply_number is not None else \
        get_power_supply_number(server)
    power_supply_weight = server.power_supply_weight

    power_supply_gwp_impact = impact_factor["power_supply_unit"]["gwp"]["impact"]
    power_supply_pe_impact = impact_factor["power_supply_unit"]["pe"]["impact"]
    power_supply_adp_impact = impact_factor["power_supply_unit"]["adp"]["impact"]

    manufacture_power_supply_gwp = power_supply_number * power_supply_weight * power_supply_gwp_impact
    manufacture_power_supply_pe = power_supply_number * power_supply_weight * power_supply_pe_impact
    manufacture_power_supply_adp = power_supply_number * power_supply_weight * power_supply_adp_impact

    manufacture_power_supply_impacts = {"gwp": manufacture_power_supply_gwp, "pe": manufacture_power_supply_pe,
                                        "adp": manufacture_power_supply_adp}

    return manufacture_power_supply_impacts


def get_power_supply_number(server):
    # TODO bring intelligence
    # Randomly chosen
    return 2


def server_assembly():
    server_assembly_gwp_impact = impact_factor["power_supply_unit"]["gwp"]["impact"]
    server_assembly_pe_impact = impact_factor["power_supply_unit"]["pe"]["impact"]
    server_assembly_adp_impact = impact_factor["power_supply_unit"]["adp"]["impact"]

    server_assembly_impacts = {"gwp": server_assembly_gwp_impact, "pe": server_assembly_pe_impact,
                               "adp": server_assembly_adp_impact}

    return server_assembly_impacts


def manufacture_rack():
    manufacture_rack_gwp_impact = impact_factor["rack_server"]["gwp"]["impact"]
    manufacture_rack_pe_impact = impact_factor["rack_server"]["pe"]["impact"]
    manufacture_rack_adp_impact = impact_factor["rack_server"]["adp"]["impact"]

    rack_impacts = {"gwp": manufacture_rack_gwp_impact, "pe": manufacture_rack_pe_impact,
                    "adp": manufacture_rack_adp_impact}

    return rack_impacts


def manufacture_blade():
    blade_slots_gwp_impact = impact_factor["blade_16_slots"]["gwp"]["impact"]
    blade_slots_pe_impact = impact_factor["blade_16_slots"]["pe"]["impact"]
    blade_slots_adp_impact = impact_factor["blade_16_slots"]["adp"]["impact"]

    blade_gwp_impact = impact_factor["blade_server"]["gwp"]["impact"]
    blade_pe_impact = impact_factor["blade_server"]["pe"]["impact"]
    blade_adp_impact = impact_factor["blade_server"]["adp"]["impact"]

    manufacture_blade_gwp_impact = (1 / 16) * blade_slots_gwp_impact + blade_gwp_impact
    manufacture_blade_pe_impact = (1 / 16) * blade_slots_pe_impact + blade_pe_impact
    manufacture_blade_adp_impact = (1 / 16) * blade_slots_adp_impact + blade_adp_impact

    rack_impacts = {"gwp": manufacture_blade_gwp_impact, "pe": manufacture_blade_pe_impact,
                    "adp": manufacture_blade_adp_impact}

    return rack_impacts
