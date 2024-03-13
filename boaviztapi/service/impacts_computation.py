from typing import Tuple, Union, Optional

from boaviztapi import config
from boaviztapi.dto.component import Motherboard
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.model.services.cloud_instance import Service, ServiceCloudInstance
from boaviztapi.model.component import ComponentCPU, ComponentCase, ComponentPowerSupply, ComponentRAM, Component, \
    ComponentAssembly, ComponentHDD, ComponentSSD
from boaviztapi.model.component.functional_block import ComponentFunctionalBlock
from boaviztapi.model.device import Device
from boaviztapi.model.device.iot import DeviceIoT
from boaviztapi.model.impact import ImpactFactor, IMPACT_PHASES, IMPACT_CRITERIAS, Impact, USE
from boaviztapi.service.factor_provider import get_impact_factor, get_iot_impact_factor


def compute_single_impact(model: Union[Component, Device, Service],
                          phase: str,
                          criteria: str,
                          duration: Union[int, str] = config["default_duration"],
                          allocation: float = 1) -> Optional[Impact]:
    try:
        impact_function = get_impact_function(model, phase)

        impact, min_impact, max_impact, warnings = impact_function(criteria, duration, model)

        result = Impact(
            value=impact * model.units.value * allocation,
            min=min_impact * model.units.min * allocation,
            max=max_impact * model.units.max * allocation,
            warnings=list(set(warnings))
        )

        model.add_impacts(result, criteria, phase)

        return result
    except (AttributeError, NotImplementedError):
        model.add_impacts(None, criteria, phase)
        return None


def compute_impacts(model: Union[Component, Device, Service], selected_criteria=config["default_criteria"],
                    duration=config["default_duration"]) -> dict:
    for c in IMPACT_CRITERIAS.keys():
        criteria = IMPACT_CRITERIAS[c]
        if "all" not in selected_criteria:
            if criteria.name not in selected_criteria:
                continue
        for phase in IMPACT_PHASES:
            compute_single_impact(model, phase, criteria.name, duration)

    return model.get_impacts(selected_criteria)


def get_impact_function(model: Union[Component, Device, Service], phase: str):
    return impacts_functions[model.NAME][phase]


def not_implemented_function(impact_type: str, duration: int, model: Union[Component, Device, Service]):
    raise NotImplementedError


def simple_impact_use(impact_type: str, duration: int, model: Union[Component, Device, Service]) -> ComputedImpacts:
    if not model.usage.avg_power.has_value():
        raise NotImplementedError

    impact_factor = model.usage.elec_factors[impact_type]

    impacts = impact_factor.value * (model.usage.avg_power.value / 1000) * model.usage.use_time_ratio.value * duration
    max_impact = impact_factor.max * (model.usage.avg_power.max / 1000) * model.usage.use_time_ratio.min * duration
    min_impact = impact_factor.min * (model.usage.avg_power.min / 1000) * model.usage.use_time_ratio.max * duration

    return impacts, min_impact, max_impact, []


def simple_embedded(impact_type: str, duration: int, model: [Device, Component, Service]) -> ComputedImpacts:
    if hasattr(model, 'type') and model.type is not None:
        impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)[model.type.value]["impact"])
        min_impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)[model.type.value]["impact"])
        max_impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)[model.type.value]["impact"])

    else:
        impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)["impact"])
        min_impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)["impact"])
        max_impact = float(get_impact_factor(item=model.NAME, impact_type=impact_type)["impact"])

    warnings = ["Generic data used for impact calculation."]

    return impact, min_impact, max_impact, warnings


def cpu_impact_use(impact_type: str, duration: int, cpu: ComponentCPU) -> ComputedImpacts:
    impact_factor = cpu.usage.elec_factors[impact_type]

    if not cpu.usage.avg_power.is_set():
        modeled_consumption = cpu.model_power_consumption()
        cpu.usage.avg_power.set_completed(
            modeled_consumption.value,
            min=modeled_consumption.min,
            max=modeled_consumption.max
        )

    impact = Impact(
        value=impact_factor.value * (
                cpu.usage.avg_power.value / 1000) * cpu.usage.use_time_ratio.value * duration,
        min=impact_factor.min * (
                cpu.usage.avg_power.min / 1000) * cpu.usage.use_time_ratio.min * duration,
        max=impact_factor.max * (
                cpu.usage.avg_power.max / 1000) * cpu.usage.use_time_ratio.max * duration
    )

    return impact.value, impact.min, impact.max, []


def cpu_impact_embedded(impact_type: str, duration: int, cpu: ComponentCPU) -> ComputedImpacts:
    cpu_die_impact = Impact(
        value=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact'],
        min=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact'],
        max=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact']
    )
    cpu_impact = Impact(
        value=get_impact_factor(item='cpu', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='cpu', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='cpu', impact_type=impact_type)['impact']
    )

    impact = Impact(
        value=cpu.die_size.value * cpu_die_impact.value + cpu_impact.value,
        min=cpu.die_size.min * cpu_die_impact.min + cpu_impact.min,
        max=cpu.die_size.max * cpu_die_impact.max + cpu_impact.max)

    impact.allocate(duration, cpu.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def assembly_impact_embedded(impact_type: str, duration: int, model: ComponentAssembly) -> ComputedImpacts:
    impact = Impact(
        value=get_impact_factor(item='assembly', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='assembly', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='assembly', impact_type=impact_type)['impact']
    )

    impact.allocate(duration, model.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def casing_impact_embedded(impact_type: str, duration: int, case: ComponentCase) -> ComputedImpacts:
    if case.case_type.value == 'rack':
        computed_impact = impact_manufacture_rack(impact_type, case)
    elif case.case_type.value == 'blade':
        computed_impact = impact_manufacture_blade(impact_type, case)
    else:
        computed_impact = impact_manufacture_rack(impact_type, case)

    impact = Impact(
        value=computed_impact[0],
        min=computed_impact[1],
        max=computed_impact[2]
    )

    impact.allocate(duration, case.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def impact_manufacture_rack(impact_type: str, case: ComponentCase) -> ComputedImpacts:
    impact_factor = Impact(
        value=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact'],
        min=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact'],
        max=get_impact_factor(item='case', impact_type=impact_type)['rack']['impact']
    )

    if case.case_type.is_archetype() and case.case_type.value == 'rack':
        blade_impact = impact_manufacture_blade(impact_type, case)
        if blade_impact[0] > impact_factor.value:
            return impact_factor.value, impact_factor.min, blade_impact[2], [
                "End of life is not included in the calculation"]
        else:
            return impact_factor.value, blade_impact[1], impact_factor.max, [
                "End of life is not included in the calculation"]
    return impact_factor.value, impact_factor.min, impact_factor.max, ["End of life is not included in the calculation"]


def impact_manufacture_blade(impact_type: str, case: ComponentCase) -> ComputedImpacts:
    impact_blade_server, impact_blade_16_slots = get_impact_constants_blade(impact_type)

    impact = compute_impact_manufacture_blade(impact_blade_server, impact_blade_16_slots)

    if case.case_type.is_archetype() and case.case_type.value == 'blade':
        rack_impact = impact_manufacture_rack(impact_type, case)
        if rack_impact[0] > impact.value:
            return impact.value, impact.min, rack_impact[2], ["End of life is not included in the calculation"]
        else:
            return impact.value, rack_impact[1], impact.max, ["End of life is not included in the calculation"]

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def get_impact_constants_blade(impact_type: str) -> Tuple[Impact, Impact]:
    impact_blade_server = Impact(
        value=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
        min=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
        max=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_server'],
    )
    impact_blade_16_slots = Impact(
        value=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
        min=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
        max=get_impact_factor(item='case', impact_type=impact_type)['blade']['impact_blade_16_slots'],
    )

    return impact_blade_server, impact_blade_16_slots


def compute_impact_manufacture_blade(impact_blade_server: Impact,
                                     impact_blade_16_slots: Impact) -> ImpactFactor:
    return ImpactFactor(
        value=(impact_blade_16_slots.value / 16) + impact_blade_server.value,
        min=(impact_blade_16_slots.min / 16) + impact_blade_server.min,
        max=(impact_blade_16_slots.max / 16) + impact_blade_server.max
    )


def iot_functional_blocks_impact_embedded(impact_type: str, duration: int,
                                          function_blocks: ComponentFunctionalBlock) -> ComputedImpacts:
    impact = Impact(
        value=get_iot_impact_factor(function_blocks.IMPACT_KEY, function_blocks.hsl_level.value, impact_type),
        min=get_iot_impact_factor(function_blocks.IMPACT_KEY, function_blocks.hsl_level.value, impact_type),
        max=get_iot_impact_factor(function_blocks.IMPACT_KEY, function_blocks.hsl_level.value, impact_type)
    )

    impact.allocate(duration, function_blocks.usage.hours_life_time)

    return impact.value, impact.min, impact.max, []


def hdd_impact_embedded(impact_type: str, duration: int, hdd: ComponentHDD) -> ComputedImpacts:
    impact = Impact(
        value=get_impact_factor(item='hdd', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='hdd', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='hdd', impact_type=impact_type)['impact']
    )

    impact.allocate(duration, hdd.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def motherboard_impact_embedded(impact_type: str, duration: int, motherboard: Motherboard) -> ComputedImpacts:
    impact = Impact(
        value=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='motherboard', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='motherboard', impact_type=impact_type)['impact']
    )

    impact.allocate(duration, motherboard.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def power_supply_impact_embedded(impact_type: str, duration: int,
                                 power_supply: Component) -> ComputedImpacts:
    if isinstance(power_supply, ComponentFunctionalBlock):
        return iot_functional_blocks_impact_embedded(impact_type, duration, power_supply)
    elif isinstance(power_supply, ComponentPowerSupply):
        return server_power_supply_impact_embedded(impact_type, duration, power_supply)
    else:
        raise NotImplementedError


def server_power_supply_impact_embedded(impact_type: str, duration: int,
                                        power_supply: ComponentPowerSupply) -> ComputedImpacts:
    impact_factor = Impact(
        value=get_impact_factor(item='power_supply', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='power_supply', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='power_supply', impact_type=impact_type)['impact']
    )

    impact = Impact(
        value=power_supply.unit_weight.value * impact_factor.value,
        min=power_supply.unit_weight.min * impact_factor.min,
        max=power_supply.unit_weight.max * impact_factor.max
    )

    impact.allocate(duration, power_supply.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def ram_impact_embedded(impact_type: str, duration: int, ram: ComponentRAM) -> ComputedImpacts:
    ram_die_impact = Impact(
        value=get_impact_factor(item='ram', impact_type=impact_type)['die_impact'],
        min=get_impact_factor(item='ram', impact_type=impact_type)['die_impact'],
        max=get_impact_factor(item='ram', impact_type=impact_type)['die_impact']
    )

    ram_impact = Impact(
        value=get_impact_factor(item='ram', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='ram', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='ram', impact_type=impact_type)['impact']
    )

    impact = Impact(
        value=(ram.capacity.value / ram.density.value) * ram_die_impact.value + ram_impact.value,
        min=(ram.capacity.min / ram.density.max) * ram_die_impact.min + ram_impact.min,
        max=(ram.capacity.max / ram.density.min) * ram_die_impact.max + ram_impact.max
    )

    impact.allocate(duration, ram.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def ram_impact_use(impact_type: str, duration: int, ram: ComponentRAM) -> ComputedImpacts:
    impact_factor = ram.usage.elec_factors[impact_type]

    if not ram.usage.avg_power.is_set():
        modeled_consumption = ram.model_power_consumption()
        ram.usage.avg_power.set_completed(
            modeled_consumption.value,
            min=modeled_consumption.min,
            max=modeled_consumption.max,
        )

    impact = ImpactFactor(
        value=impact_factor.value * (
                ram.usage.avg_power.value / 1000) * ram.usage.use_time_ratio.value * duration,
        min=impact_factor.min * (
                ram.usage.avg_power.min / 1000) * ram.usage.use_time_ratio.min * duration,
        max=impact_factor.max * (
                ram.usage.avg_power.max / 1000) * ram.usage.use_time_ratio.max * duration
    )

    return impact.value, impact.min, impact.max, []


def ssd_impact_embedded(impact_type: str, duration: int, ssd: ComponentSSD) -> ComputedImpacts:
    ssd_die_impact = Impact(
        value=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact'],
        min=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact'],
        max=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact']
    )
    ssd_impact = Impact(
        value=get_impact_factor(item='ssd', impact_type=impact_type)['impact'],
        min=get_impact_factor(item='ssd', impact_type=impact_type)['impact'],
        max=get_impact_factor(item='ssd', impact_type=impact_type)['impact']
    )

    impact = Impact(
        value=(ssd.capacity.value / ssd.density.value) * ssd_die_impact.value + ssd_impact.value,
        min=(ssd.capacity.min / ssd.density.max) * ssd_die_impact.min + ssd_impact.min,
        max=(ssd.capacity.max / ssd.density.min) * ssd_die_impact.max + ssd_impact.max
    )

    impact.allocate(duration, ssd.usage.hours_life_time)

    return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


def iot_impact_embedded(impact_type: str, duration: int, iot_device: DeviceIoT) -> ComputedImpacts:
    impacts = []
    min_impacts = []
    max_impacts = []
    warnings = iot_device.WARNINGS

    for component in iot_device.components:
        single_impact = compute_single_impact(component, "embedded", impact_type, duration)
        impacts.append(single_impact.value)
        min_impacts.append(single_impact.min)
        max_impacts.append(single_impact.max)
        warnings = warnings + single_impact.warnings

    return sum(impacts), sum(min_impacts), sum(max_impacts), warnings


def iot_impact_use(impact_type: str, duration: int, iot_device: DeviceIoT) -> ComputedImpacts:
    if iot_device.usage.avg_power.value is None:
        raise NotImplementedError

    impact_factor = iot_device.usage.elec_factors[impact_type]
    impact = impact_factor.value * (
            iot_device.usage.avg_power.value / 1000) * iot_device.usage.use_time_ratio.value * duration
    min_impact = impact_factor.min * (
            iot_device.usage.avg_power.min / 1000) * iot_device.usage.use_time_ratio.min * duration
    max_impact = impact_factor.max * (
            iot_device.usage.avg_power.max / 1000) * iot_device.usage.use_time_ratio.max * duration

    return impact, min_impact, max_impact, []


def server_impact_embedded(impact_type: str, duration: int, server: DeviceServer) -> ComputedImpacts:
    impacts = []
    min_impacts = []
    max_impacts = []
    warnings = []

    try:
        for component in server.components:
            component.usage.hours_life_time = server.usage.hours_life_time
            single_impact = compute_single_impact(component, "embedded", impact_type, duration)

            if single_impact is None:
                raise NotImplementedError

            impacts.append(single_impact.value)
            min_impacts.append(single_impact.min)
            max_impacts.append(single_impact.max)
            warnings = warnings + single_impact.warnings

        return sum(impacts), sum(min_impacts), sum(max_impacts), warnings

    except NotImplementedError:
        impact = Impact(value=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"],
                        min=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"],
                        max=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"])

        warnings = ["Generic data used for impact calculation."]

        impact.allocate(duration, server.usage.hours_life_time)

        return impact.value, impact.min, impact.max, warnings


def server_impact_use(impact_type: str, duration: int, server: DeviceServer) -> ComputedImpacts:
    impact_factor = server.usage.elec_factors[impact_type]

    if not server.usage.avg_power.is_set():
        modeled_consumption = server.model_power_consumption()
        server.usage.avg_power.set_completed(
            modeled_consumption.value,
            min=modeled_consumption.min,
            max=modeled_consumption.max
        )

    # Compute impacts at component level
    compute_single_impact(server.cpu, USE, impact_type, duration)
    for ram in server.ram:
        compute_single_impact(ram, USE, impact_type, duration)

    impact = impact_factor.value * (server.usage.avg_power.value / 1000) * server.usage.use_time_ratio.value * duration
    min_impact = impact_factor.min * (server.usage.avg_power.min / 1000) * server.usage.use_time_ratio.min * duration
    max_impact = impact_factor.max * (server.usage.avg_power.max / 1000) * server.usage.use_time_ratio.max * duration

    return impact, min_impact, max_impact, []


def cloud_impact_embedded(impact_type: str, duration: int, cloud_instance: ServiceCloudInstance) -> ComputedImpacts:
    impacts = []
    min_impacts = []
    max_impacts = []
    warnings = []
    default_allocation = cloud_instance.vcpu.value / cloud_instance.platform.get_total_vcpu()

    try:
        for component in cloud_instance.platform.components:
            component.usage.hours_life_time = cloud_instance.platform.usage.hours_life_time
            allocation = default_allocation
            if component.NAME == "RAM":
                allocation = cloud_instance.memory.value / cloud_instance.platform.get_total_memory()
            if component.NAME == "SSD":
                if cloud_instance.ssd_storage.has_value():
                    allocation = cloud_instance.ssd_storage.value / cloud_instance.platform.get_total_disk_capacity("SSD")
                else:
                    continue
            if component.NAME == "HDD":
                if cloud_instance.hdd_storage.has_value():
                    allocation = cloud_instance.hdd_storage.value / cloud_instance.platform.get_total_disk_capacity("HDD")
                else:
                    continue

            single_impact = compute_single_impact(component, "embedded", impact_type, duration, allocation)

            if single_impact is None:
                raise NotImplementedError

            impacts.append(single_impact.value)
            min_impacts.append(single_impact.min)
            max_impacts.append(single_impact.max)
            warnings = warnings + single_impact.warnings
        return sum(impacts), sum(min_impacts), sum(max_impacts), warnings

    except NotImplementedError:
        impact = Impact(value=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"],
                        min=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"],
                        max=get_impact_factor(item='SERVER', impact_type=impact_type)["impact"])

        warnings = ["Generic data used for impact calculation."]

        impact.allocate(duration, cloud_instance.platform.usage.hours_life_time)

        return impact.value * default_allocation, impact.min * default_allocation, impact.max * default_allocation, warnings


def cloud_impact_use(impact_type: str, duration: int, cloud_instance: ServiceCloudInstance) -> ComputedImpacts:
    platform = cloud_instance.platform
    impact_factor = platform.usage.elec_factors[impact_type]

    if not cloud_instance.usage.avg_power.is_set():
        modeled_consumption = cloud_instance.model_power_consumption()
        cloud_instance.usage.avg_power.set_completed(
            value=modeled_consumption.value,
            min=modeled_consumption.min,
            max=modeled_consumption.max
        )

    # Compute impacts at component level
    compute_single_impact(platform.cpu, USE, impact_type, duration)
    for ram in platform.ram:
        compute_single_impact(ram, USE, impact_type, duration)

    impact = impact_factor.value * (cloud_instance.usage.avg_power.value / 1000) * platform.usage.use_time_ratio.value * duration
    min_impact = impact_factor.min * (cloud_instance.usage.avg_power.min / 1000) * platform.usage.use_time_ratio.min * duration
    max_impact = impact_factor.max * (cloud_instance.usage.avg_power.max / 1000) * platform.usage.use_time_ratio.max * duration

    return impact, min_impact, max_impact, []


impacts_functions = {
    "CPU": {
        "use": cpu_impact_use,
        "embedded": cpu_impact_embedded
    },
    "RAM": {
        "use": ram_impact_use,
        "embedded": ram_impact_embedded
    },
    "SSD": {
        "use": simple_impact_use,
        "embedded": ssd_impact_embedded
    },
    "HDD": {
        "use": simple_impact_use,
        "embedded": hdd_impact_embedded
    },
    "POWER_SUPPLY": {
        "use": not_implemented_function,
        "embedded": power_supply_impact_embedded
    },
    "ASSEMBLY": {
        "use": not_implemented_function,
        "embedded": assembly_impact_embedded
    },
    "CASE": {
        "use": simple_impact_use,
        "embedded": casing_impact_embedded
    },
    "MOTHERBOARD": {
        "use": simple_impact_use,
        "embedded": motherboard_impact_embedded
    },
    "SERVER": {
        "use": server_impact_use,
        "embedded": server_impact_embedded
    },
    "IOT_DEVICE": {
        "use": iot_impact_use,
        "embedded": iot_impact_embedded
    },
    "LAPTOP": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "DESKTOP": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "TABLET": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "SMARTPHONE": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "TELEVISION": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "SMARTWATCH": {
        "use": simple_impact_use,
        "embedded": ram_impact_embedded
    },
    "BOX": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "USB_STICK": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "EXTERNAL_SSD": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "EXTERNAL_HDD": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "MONITOR": {
        "use": simple_impact_use,
        "embedded": simple_embedded
    },
    "CLOUD_INSTANCE": {
        "use": cloud_impact_use,
        "embedded": cloud_impact_embedded
    },
    "ACTUATORS": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "CASING": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "CONNECTIVITY": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "MEMORY": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "OTHERS": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "PCB": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "SECURITY": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "PROCESSING": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "SENSING": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
    "USER_INTERFACE": {
        "use": simple_impact_use,
        "embedded": iot_functional_blocks_impact_embedded
    },
}
