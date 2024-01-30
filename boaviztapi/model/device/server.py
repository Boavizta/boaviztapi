from typing import List, Union

from boaviztapi import config
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.model.usage import ModelUsageServer
from boaviztapi.service.archetype import get_server_archetype, get_arch_component


class DeviceServer(Device):
    NAME = "SERVER"

    def __init__(self, archetype=get_server_archetype(config["default_server"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self._cpu = None
        self._ram_list = None
        self._disk_list = []
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
        if not self._disk_list:
            if get_arch_component(self.archetype, "SSD")["units"] not in [{}, {'default':0}]:
                self._disk_list.append(ComponentSSD(archetype=get_arch_component(self.archetype, "SSD")))
            if get_arch_component(self.archetype, "HDD")["units"] not in [{}, {'default':0}]:
                self._disk_list.append(ComponentHDD(archetype=get_arch_component(self.archetype, "HDD")))

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

    def model_power_consumption(self):
        conso_cpu = ImpactFactor(
            value=self.cpu.model_power_consumption().value,
            min=self.cpu.model_power_consumption().min,
            max=self.cpu.model_power_consumption().max,
        )
        self.cpu.usage.avg_power.set_completed(value=conso_cpu.value,
                                               min=conso_cpu.min,
                                               max=conso_cpu.max)

        conso_ram = ImpactFactor(
            value=0,
            min=0,
            max=0
        )
        for ram_unit in self.ram:
            conso_ram.value = conso_ram.value + ram_unit.model_power_consumption().value
            conso_ram.min = conso_ram.min + ram_unit.model_power_consumption().min
            conso_ram.max = conso_ram.max + ram_unit.model_power_consumption().max
            ram_unit.usage.avg_power.set_completed(value=conso_ram.value,
                                                   min=conso_ram.min,
                                                   max=conso_ram.max)

        return ImpactFactor(
            value=(conso_cpu.value + conso_ram.value) * (1 + self.usage.other_consumption_ratio.value),
            min=(conso_cpu.min + conso_ram.min) * (1 + self.usage.other_consumption_ratio.min),
            max=(conso_cpu.max + conso_ram.max) * (1 + self.usage.other_consumption_ratio.max)
        )

    def get_total_memory(self):
        memory = 0
        for ram_strip in self.ram:
            memory += ram_strip.capacity.value * ram_strip.units.value
        return memory

    def get_total_disk_capacity(self, disk_type):
        capacity = 0
        for disk in self.disk:
            if disk.NAME == disk_type or disk_type == "all":
                if disk.units.has_value():
                    capacity += disk.capacity.value * disk.units.value
        return capacity

    def get_total_vcpu(self):
        return self.cpu.threads.value * self.cpu.units.value
