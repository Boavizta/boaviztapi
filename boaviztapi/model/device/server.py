from abc import ABC
from typing import List, Union

from boaviztapi.dto.component import CPU, RAM, Disk, PowerSupply
from boaviztapi.dto.usage import UsageServer, UsageCloud
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device, NumberSignificantFigures
from boaviztapi.dto.device.device import Server, Cloud, ConfigurationServer, ModelServer
from boaviztapi.model.usage import ModelUsageServer, ModelUsageCloud


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

    def __init__(self, /, **kwargs):
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
            self._cpu = self.DEFAULT_COMPONENT_CPU
            self._cpu.units = self.DEFAULT_NUMBER_CPU
        return self._cpu

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self._cpu = value

    @property
    def ram(self) -> List[ComponentRAM]:
        if self._ram_list is None:
            self._ram_list = [self.DEFAULT_COMPONENT_RAM] * self.DEFAULT_NUMBER_RAM
        return self._ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self._ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        if self._disk_list is None:
            self._disk_list = [self.DEFAULT_COMPONENT_DISK] * self.DEFAULT_NUMBER_DISK
        return self._disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self._disk_list = value

    @property
    def power_supply(self) -> ComponentPowerSupply:
        if self._power_supply is None:
            self._power_supply = self.DEFAULT_COMPONENT_POWER_SUPPLY
            self._power_supply.units = self.DEFAULT_NUMBER_POWER_SUPPLY
        return self._power_supply

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self._power_supply = value

    @property
    def case(self) -> ComponentCase:
        if self._case is None:
            self._case = self.DEFAULT_COMPONENT_CASE
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
            self._motherboard = self.DEFAULT_COMPONENT_MOTHERBOARD
        return self._motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self._motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        if self._assembly is None:
            self._assembly = self.DEFAULT_COMPONENT_ASSEMBLY
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
            impacts.append(impact)
            significant_figures.append(sign_fig)
        return sum(impacts), min(significant_figures)

    def __impact_usage(self, impact_type: str) -> NumberSignificantFigures:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')
        impacts = impact_factor * (self.usage.hours_electrical_consumption / 1000) \
                  * self.usage.use_time

        return impacts, 1

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

    @classmethod
    def from_dto(cls, server_complete: Server, server_input: Server) -> 'DeviceServer':
        cpu, ram_list, disk_list, power_supply, case, usage = None, None, None, None, None, None

        if server_complete.configuration is not None:
            if server_input.configuration is None:
                server_input.configuration = ConfigurationServer()

            if server_complete.configuration.cpu is not None:
                cpu = ComponentCPU.from_dto(server_complete.configuration.cpu, server_input.configuration.cpu or CPU())

            if server_complete.configuration.ram is not None:
                ram_list = []
                for complete_ram, input_ram in zip(server_complete.configuration.ram,
                                                   server_input.configuration.ram or [RAM()] * len(
                                                       server_complete.configuration.ram)):
                    ram_list.append(ComponentRAM.from_dto(complete_ram, input_ram))

            if server_complete.configuration.disk is not None:
                disk_list = []
                for complete_disk, input_disk in zip(server_complete.configuration.disk,
                                                     server_input.configuration.disk or [Disk()] * len(
                                                         server_complete.configuration.ram)):
                    if complete_disk.type.lower() == "ssd":
                        disk_list.append(ComponentSSD.from_dto(complete_disk, input_disk))
                    elif complete_disk.type.lower() == "hdd":
                        disk_list.append(ComponentHDD.from_dto(complete_disk, input_disk))

            if server_complete.configuration.power_supply is not None:
                power_supply = ComponentPowerSupply.from_dto(server_complete.configuration.power_supply,
                                                             server_input.configuration.power_supply or PowerSupply())
        if server_complete.model is not None and server_complete.model.type is not None:
            if server_input.model is None:
                server_input.model = ModelServer()
            case = ComponentCase.from_dto(server_complete.model.type, server_input.model.type or None)

        if server_complete.usage is not None:
            usage = ModelUsageServer().from_dto(server_complete.usage, server_input.usage or UsageServer())

        serv = cls(
            cpu=cpu,
            ram=ram_list,
            disk=disk_list,
            power_supply=power_supply,
            case=case,
            usage=usage
        )

        serv._set_states_from_input(server_input)

        return serv


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
        return (impact / self.usage.instance_per_server), sign_fig

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_manufacture_pe()
        return (impact / self.usage.instance_per_server), sign_fig

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_manufacture_adp()
        return (impact / self.usage.instance_per_server), sign_fig

    def impact_use_gwp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_gwp()
        return (impact / self.usage.instance_per_server), sign_fig

    def impact_use_pe(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_pe()
        return (impact / self.usage.instance_per_server), sign_fig

    def impact_use_adp(self) -> NumberSignificantFigures:
        impact, sign_fig = super().impact_use_adp()
        return (impact / self.usage.instance_per_server), sign_fig

    @classmethod
    def from_dto(cls, instance_complete: Cloud, instance_input: Cloud) -> 'DeviceCloudInstance':
        server = super().from_dto(instance_complete, instance_input)
        usage = None
        if instance_complete.usage is not None:
            usage = ModelUsageCloud().from_dto(instance_complete.usage, instance_input.usage or UsageCloud())

        cloud_instance = cls(
            cpu=server.cpu,
            ram=server.ram,
            disk=server.disk,
            power_supply=server.power_supply,
            case=server.case,
            usage=usage
        )

        return cloud_instance
