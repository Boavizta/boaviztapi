from abc import ABC
from typing import List, Union

from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.model.usage import ModelUsageServer, ModelUsageCloud
import boaviztapi.utils.roundit as rd
from boaviztapi.service.archetype import get_server_archetype, get_arch_component, get_cloud_instance_archetype
from boaviztapi.service.factor_provider import get_impact_factor


class DeviceServer(Device):
    NAME = "SERVER"

    def __init__(self, archetype=get_server_archetype(config["default_server"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self._cpu = None
        self._ram_list = None
        self._disk_list = None
        self._power_supply = None
        self._case = None
        self._motherboard = None
        self._assembly = None
        self._usage = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def cpu(self) -> ComponentCPU:
        if self._cpu is None:
            self._cpu = ComponentCPU(archetype=get_arch_component(self.archetype, "CPU"))
        return self._cpu

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self._cpu = value

    @property
    def ram(self) -> List[ComponentRAM]:
        if self._ram_list is None:
            self._ram_list = [ComponentRAM(archetype=get_arch_component(self.archetype, "RAM"))]
        return self._ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self._ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        if self._disk_list is None:
            self._disk_list = [ComponentSSD(archetype=get_arch_component(self.archetype, "SSD"))]
        return self._disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self._disk_list = value

    @property
    def power_supply(self) -> ComponentPowerSupply:
        if self._power_supply is None:
            self._power_supply = ComponentPowerSupply(archetype=get_arch_component(self.archetype, "POWER_SUPPLY"))
        return self._power_supply

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self._power_supply = value

    @property
    def case(self) -> ComponentCase:
        if self._case is None:
            self._case = ComponentCase(archetype=get_arch_component(self.archetype, "CASE"))
        return self._case

    @case.setter
    def case(self, value: ComponentCase) -> None:
        self._case = value

    @property
    def case_type(self) -> str:
        return self.case.case_type

    @case_type.setter
    def case_type(self, value: str) -> None:
        self.case.case_type = value

    @property
    def motherboard(self) -> ComponentMotherboard:
        if self._motherboard is None:
            self._motherboard = ComponentMotherboard(archetype=get_arch_component(self.archetype, "MOTHERBOARD"))
        return self._motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self._motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        if self._assembly is None:
            self._assembly = ComponentAssembly(archetype=get_arch_component(self.archetype, "ASSEMBLY"))
        return self._assembly

    @assembly.setter
    def assembly(self, value: ComponentAssembly) -> None:
        self._assembly = value

    @property
    def usage(self) -> ModelUsageServer:
        if self._usage is None:
            self._usage = ModelUsageServer(archetype=get_arch_component(self.archetype, "USAGE"))
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageServer) -> None:
        self._usage = value

    @property
    def components(self) -> List[Component]:
        return [self.assembly] + [self.cpu] + self.ram + self.disk + [self.power_supply] + [self.case] + [
            self.motherboard]

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impacts = []
        min_impacts = []
        max_impacts = []
        warnings = []

        try:
            for component in self.components:
                impact, min_impact, max_impact, c_warning = getattr(component, f'impact_embedded')(impact_type)

                impacts.append(impact * component.units.value)
                min_impacts.append(min_impact * component.units.min)
                max_impacts.append(max_impact * component.units.max)
                warnings = warnings + c_warning

            return sum(impacts), sum(min_impacts), sum(max_impacts), warnings

        except NotImplementedError:
            impact = get_impact_factor(item='SERVER', impact_type=impact_type)["impact"]
            min_impacts = get_impact_factor(item='SERVER', impact_type=impact_type)["impact"]
            max_impacts = get_impact_factor(item='SERVER', impact_type=impact_type)["impact"]

            warnings = ["Generic data used for impact calculation."]

            return impact, min_impacts, max_impacts, warnings

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        impact_factor = self.usage.elec_factors[impact_type]

        if not self.usage.avg_power.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.avg_power.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max
            )

        impact = impact_factor.value * (self.usage.avg_power.value / 1000) * self.usage.use_time_ratio.value * duration
        min_impact = impact_factor.min * (self.usage.avg_power.min / 1000) * self.usage.use_time_ratio.min * duration
        max_impact = impact_factor.max * (self.usage.avg_power.max / 1000) * self.usage.use_time_ratio.max * duration

        return impact, min_impact, max_impact, []

    def model_power_consumption(self):
        conso_cpu = ImpactFactor(
            value=self.cpu.model_power_consumption().value * self.cpu.units.value,
            min=self.cpu.model_power_consumption().min * self.cpu.units.min,
            max=self.cpu.model_power_consumption().max * self.cpu.units.max,
        )
        conso_ram = ImpactFactor(
            value=0,
            min=0,
            max=0
        )
        for ram_unit in self.ram:
            conso_ram.value = conso_ram.value + ram_unit.model_power_consumption().value * ram_unit.units.value
            conso_ram.min = conso_ram.min + ram_unit.model_power_consumption().min * ram_unit.units.min
            conso_ram.max = conso_ram.max + ram_unit.model_power_consumption().max * ram_unit.units.max

        return ImpactFactor(
            value=(conso_cpu.value + conso_ram.value) * (1 + self.usage.other_consumption_ratio.value),
            min=(conso_cpu.min + conso_ram.min) * (1 + self.usage.other_consumption_ratio.min),
            max=(conso_cpu.max + conso_ram.max) * (1 + self.usage.other_consumption_ratio.max)
        )

class DeviceCloudInstance(DeviceServer, ABC):

    def __init__(self,
                 archetype=get_cloud_instance_archetype(config["default_cloud"], config["default_cloud_provider"]),
                 **kwargs):
        super().__init__(**kwargs, archetype=archetype)

    @property
    def usage(self) -> ModelUsageCloud:
        if self._usage is None:
            self._usage = ModelUsageCloud(archetype=get_arch_component(self.archetype, "USAGE"))
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageCloud) -> None:
        self._usage = value

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact, min_impact, max_impact, c_warning = super().impact_embedded(impact_type)
        return (
            (impact / self.usage.instance_per_server.value),
            (min_impact / self.usage.instance_per_server.min),
            (max_impact / self.usage.instance_per_server.max),
            c_warning
        )

    def impact_use(self, impact_type: str, duration: int) -> ComputedImpacts:
        impact, min_impact, max_impact, c_warning = super().impact_use(impact_type, duration)
        return (
            (impact / self.usage.instance_per_server.value),
            (min_impact / self.usage.instance_per_server.min),
            (max_impact / self.usage.instance_per_server.max),
            c_warning
        )
