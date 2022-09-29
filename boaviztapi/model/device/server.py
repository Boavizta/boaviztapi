import copy
from abc import ABC
from typing import List, Union

from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device, NumberSignificantFigures
from boaviztapi.model.usage import ModelUsageServer, ModelUsageCloud
import boaviztapi.utils.roundit as rd


class DeviceServer(Device):
    DEFAULT_COMPONENT_CPU = ComponentCPU()
    DEFAULT_NUMBER_CPU = 2

    DEFAULT_COMPONENT_RAM = ComponentRAM()
    DEFAULT_NUMBER_RAM = 24

    DEFAULT_COMPONENT_DISK = ComponentSSD()
    DEFAULT_NUMBER_DISK = 1

    DEFAULT_COMPONENT_POWER_SUPPLY = ComponentPowerSupply()
    DEFAULT_NUMBER_POWER_SUPPLY = 2

    DEFAULT_COMPONENT_CASE = ComponentCase()
    DEFAULT_COMPONENT_MOTHERBOARD = ComponentMotherboard()
    DEFAULT_COMPONENT_ASSEMBLY = ComponentAssembly()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            self._cpu = copy.deepcopy(self.DEFAULT_COMPONENT_CPU)
            self._cpu.units = self.DEFAULT_NUMBER_CPU
        return self._cpu

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self._cpu = value

    @property
    def ram(self) -> List[ComponentRAM]:
        if self._ram_list is None:
            self.DEFAULT_COMPONENT_RAM.units = copy.deepcopy(self.DEFAULT_NUMBER_RAM)
            self._ram_list = [self.DEFAULT_COMPONENT_RAM]
        return self._ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self._ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        if self._disk_list is None:
            self.DEFAULT_COMPONENT_DISK.units = self.DEFAULT_NUMBER_DISK
            self._disk_list = [copy.deepcopy(self.DEFAULT_COMPONENT_DISK)]
        return self._disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self._disk_list = value

    @property
    def power_supply(self) -> ComponentPowerSupply:
        if self._power_supply is None:
            self._power_supply = copy.deepcopy(self.DEFAULT_COMPONENT_POWER_SUPPLY)
            self._power_supply.units = self.DEFAULT_NUMBER_POWER_SUPPLY
        return self._power_supply

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self._power_supply = value

    @property
    def case(self) -> ComponentCase:
        if self._case is None:
            self._case = copy.deepcopy(self.DEFAULT_COMPONENT_CASE)
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
            self._motherboard = copy.deepcopy(self.DEFAULT_COMPONENT_MOTHERBOARD)
        return self._motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self._motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        if self._assembly is None:
            self._assembly = copy.deepcopy(self.DEFAULT_COMPONENT_ASSEMBLY)
        return self._assembly

    @assembly.setter
    def assembly(self, value: ComponentAssembly) -> None:
        self._assembly = value

    @property
    def usage(self) -> ModelUsageServer:
        if self._usage is None:
            self._usage = ModelUsageServer()
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageServer) -> None:
        self._usage = value

    @property
    def components(self) -> List[Component]:
        return [self.assembly] + [self.cpu] + self.ram + self.disk + [self.power_supply] + [self.case] + [
            self.motherboard]

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        impacts = []
        significant_figures = []
        for component in self.components:
            impact, sign_fig = getattr(component, f'impact_manufacture_{impact_type}')()
            impacts.append(impact*component.units)
            significant_figures.append(sign_fig)
        return sum(impacts), min(significant_figures)

    def __impact_usage(self, impact_type: str) -> NumberSignificantFigures:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')
        if not self.usage.hours_electrical_consumption.is_set():
            self.usage.hours_electrical_consumption.value = self.model_power_consumption()
            self.usage.hours_electrical_consumption.status = Status.COMPLETED

        impacts = impact_factor.value * (self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value
        sig_fig = self.__compute_significant_numbers(impact_factor.value)
        return impacts, sig_fig

    def model_power_consumption(self):
        conso_cpu = self.cpu.model_power_consumption()*self.cpu.units
        conso_ram = 0
        for ram_unit in self.ram:
            conso_ram += ram_unit.model_power_consumption()*ram_unit.units
        return (conso_cpu + conso_ram) * (1 + self.usage.other_consumption_ratio.value)

    def __compute_significant_numbers(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value, impact_factor)

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> NumberSignificantFigures:
        return self.__impact_usage('gwp')

    def impact_use_pe(self) -> NumberSignificantFigures:
        return self.__impact_usage('pe')

    def impact_use_adp(self) -> NumberSignificantFigures:
        return self.__impact_usage('adp')


class DeviceCloudInstance(DeviceServer, ABC):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def usage(self) -> ModelUsageCloud:
        if self._usage is None:
            self._usage = ModelUsageCloud()
        return self._usage

    @usage.setter
    def usage(self, value: ModelUsageCloud) -> None:
        self._usage = value

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_manufacture_gwp()
        return (impact / self.usage.instance_per_server.value), sign_fig

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_manufacture_pe()
        return (impact / self.usage.instance_per_server.value), sign_fig

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_manufacture_adp()
        return (impact / self.usage.instance_per_server.value), sign_fig

    def impact_use_gwp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_gwp()
        return (impact / self.usage.instance_per_server.value), sign_fig

    def impact_use_pe(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_pe()
        return (impact / self.usage.instance_per_server.value), sign_fig

    def impact_use_adp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_adp()
        return (impact / self.usage.instance_per_server.value), sign_fig
