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


class DeviceServer(Device):

    def __init__(self, default_config=config['SERVER'],**kwargs):
        super().__init__(**kwargs)
        self.default_config = default_config
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
            self._cpu = ComponentCPU(archetype=self.default_config['CPU'])
        return self._cpu

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self._cpu = value

    @property
    def ram(self) -> List[ComponentRAM]:
        if self._ram_list is None:
            self._ram_list = [ComponentRAM(archetype=self.default_config['RAM'])]
        return self._ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self._ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        if self._disk_list is None:
            self._disk_list = [ComponentSSD(archetype=self.default_config['SSD'])]
        return self._disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self._disk_list = value

    @property
    def power_supply(self) -> ComponentPowerSupply:
        if self._power_supply is None:
            self._power_supply = ComponentPowerSupply(archetype=self.default_config['POWER_SUPPLY'])
        return self._power_supply

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self._power_supply = value

    @property
    def case(self) -> ComponentCase:
        if self._case is None:
            self._case = ComponentCase(archetype=self.default_config['CASE'])
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
            self._motherboard = ComponentMotherboard(archetype=self.default_config['MOTHERBOARD'])
        return self._motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self._motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        if self._assembly is None:
            self._assembly = ComponentAssembly(archetype=self.default_config['ASSEMBLY'])
        return self._assembly

    @assembly.setter
    def assembly(self, value: ComponentAssembly) -> None:
        self._assembly = value

    @property
    def usage(self) -> ModelUsageServer:
        if self._usage is None:
            self._usage = ModelUsageServer(archetype=self.default_config['USAGE'])
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageServer) -> None:
        self._usage = value

    @property
    def components(self) -> List[Component]:
        return [self.assembly] + [self.cpu] + self.ram + self.disk + [self.power_supply] + [self.case] + [
            self.motherboard]

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        impacts = []
        min_impacts = []
        max_impacts = []
        significant_figures = []
        warnings = []

        for component in self.components:
            impact, sign_fig, min_impact, max_impact, c_warning = getattr(component, f'impact_manufacture_{impact_type}')()
            impacts.append(impact*component.units.value)
            min_impacts.append(min_impact*component.units.min)
            max_impacts.append(max_impact*component.units.max)

            significant_figures.append(sign_fig)
            warnings = warnings + c_warning
        return sum(impacts), min(significant_figures), sum(min_impacts), sum(max_impacts), warnings

    def __impact_usage(self, impact_type: str) -> ComputedImpacts:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')
        if not self.usage.hours_electrical_consumption.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.hours_electrical_consumption.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max
            )

        impact = impact_factor.value * (self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value
        min_impact = impact_factor.min * (self.usage.hours_electrical_consumption.min / 1000) * self.usage.use_time.min
        max_impact = impact_factor.max * (self.usage.hours_electrical_consumption.max / 1000) * self.usage.use_time.max

        sig_fig = self.__compute_significant_numbers(impact_factor.value)
        return impact, sig_fig, min_impact, max_impact, []

    def model_power_consumption(self):
        conso_cpu = ImpactFactor(
            value=self.cpu.model_power_consumption().value*self.cpu.units.value,
            min=self.cpu.model_power_consumption().min*self.cpu.units.min,
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


    def __compute_significant_numbers(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value, impact_factor)

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> ComputedImpacts:
        return self.__impact_usage('gwp')

    def impact_use_pe(self) -> ComputedImpacts:
        return self.__impact_usage('pe')

    def impact_use_adp(self) -> ComputedImpacts:
        return self.__impact_usage('adp')


class DeviceCloudInstance(DeviceServer, ABC):

    def __init__(self, default_config=config['CLOUD'], **kwargs):
        super().__init__(**kwargs, default_config=default_config)

    @property
    def usage(self) -> ModelUsageCloud:
        if self._usage is None:
            self._usage = ModelUsageCloud(archetype=self.default_config['USAGE'])
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageCloud) -> None:
        self._usage = value

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_manufacture_gwp()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning

    def impact_manufacture_pe(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_manufacture_pe()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning

    def impact_manufacture_adp(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_manufacture_adp()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning

    def impact_use_gwp(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_use_gwp()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning

    def impact_use_pe(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_use_pe()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning

    def impact_use_adp(self) -> ComputedImpacts:
        impact, sign_fig, min_impact, max_impact, c_warning = super().impact_use_adp()
        return (impact / self.usage.instance_per_server.value), sign_fig, min_impact, max_impact, c_warning
