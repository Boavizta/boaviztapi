import itertools
from itertools import chain
from typing import List, Union, Any

from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device, NumberSignificantFigures
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.device.device import Server, Cloud, ModelServer, ConfigurationServer


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
        self.__cpu = None
        self.__ram_list = None
        self.__disk_list = None
        self.__power_supply = None
        self.__case = None
        self.__motherboard = None
        self.__assembly = None

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def cpu(self) -> ComponentCPU:
        if self.__cpu is None:
            self.__cpu = self.DEFAULT_COMPONENT_CPU
            self.__cpu.units = self.DEFAULT_NUMBER_CPU
        return self.__cpu

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self.__cpu = value

    @property
    def ram(self) -> List[ComponentRAM]:
        if self.__ram_list is None:
            self.__ram_list = [self.DEFAULT_COMPONENT_RAM] * self.DEFAULT_NUMBER_RAM
        return self.__ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self.__ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        if self.__disk_list is None:
            self.__disk_list = [self.DEFAULT_COMPONENT_DISK] * self.DEFAULT_NUMBER_DISK
        return self.__disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self.__disk_list = value

    @property
    def power_supply(self) -> ComponentPowerSupply:
        if self.__power_supply is None:
            self.__power_supply = self.DEFAULT_COMPONENT_POWER_SUPPLY
            self.__power_supply.units = self.DEFAULT_NUMBER_POWER_SUPPLY
        return self.__power_supply

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self.__power_supply = value

    @property
    def case(self) -> ComponentCase:
        if self.__case is None:
            self.__case = self.DEFAULT_COMPONENT_CASE
        return self.__case

    @case.setter
    def case(self, value: ComponentCase) -> None:
        self.__case = value

    @property
    def case_type(self) -> str:
        return self.case.case_type

    @case_type.setter
    def case_type(self, value: str) -> None:
        self.case.case_type = value

    @property
    def motherboard(self) -> ComponentMotherboard:
        if self.__motherboard is None:
            self.__motherboard = self.DEFAULT_COMPONENT_MOTHERBOARD
        return self.__motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self.__motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        if self.__assembly is None:
            self.__assembly = self.DEFAULT_COMPONENT_ASSEMBLY
        return self.__assembly

    @assembly.setter
    def assembly(self, value: ComponentAssembly) -> None:
        self.__assembly = value

    @property
    def components(self) -> List[Component]:
        return [self.assembly] + [self.cpu] + self.ram + self.disk + [self.power_supply] + [self.case] + [self.motherboard]

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        impacts = []
        significant_figures = []
        for component in self.components:
            impact, sign_fig = getattr(component, f'impact_manufacture_{impact_type}')()
            impacts.append(impact)
            significant_figures.append(sign_fig)
        return sum(impacts), min(significant_figures)

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def to_dto(self, original_server: Server) -> Server:
        return Server(
            model=ModelServer(
                archetype=original_server.model.archetype
            ),
            configuration=ConfigurationServer(
                cpu=self.merge_component_units(self.cpu, original_server.configuration.cpu),
                ram=self.merge_component_units(self.ram, original_server.configuration.ram),
                disk=self.merge_component_units(self.disk, original_server.configuration.disk),
                power_supply=self.merge_component_units(self.power_supply, original_server.configuration.power_supply),
            ),
            usage=original_server.usage
        )

    @staticmethod
    def merge_component_units(components: Union[Component, List[Component]],
                              components_dto: Union[ComponentDTO, List[ComponentDTO]]) \
            -> Union[ComponentDTO, List[ComponentDTO]]:
        component_id_map = {}
        for compo in components:
            component_id_map[compo.id] = [compo] + component_id_map.get(compo.id, [])

        if isinstance(components_dto, list):
            res = []
            for compo_dto in components_dto:
                compo = component_id_map[compo_dto.__id][0]
                new_compo_dto = compo.to_dto(compo_dto)
                new_compo_dto.units = len(component_id_map[compo_dto.__id])
                res.append(new_compo_dto)
        else:
            res = components[0].to_dto(components_dto)
            res.units = len(component_id_map[components_dto.__id])
        return res

    @classmethod
    def from_dto(cls, server_complete: Server, server_input: Server) -> 'DeviceServer':
        cpu, ram_list, disk_list, power_supply, case_type = None, None, None, None, None

        if server_complete.configuration is not None:
            if server_complete.configuration.cpu is not None:
                cpu = ComponentCPU.from_dto(server_complete.configuration.cpu, server_input.configuration.cpu)

            if server_complete.configuration.ram is not None:
                ram_list = []
                for complete_ram, input_ram in zip(server_complete.configuration.ram,
                                                   server_input.configuration.ram):
                    ram_list.append(ComponentRAM.from_dto(complete_ram, input_ram))

            if server_complete.configuration.disk is not None:
                disk_list = []
                for complete_disk, input_disk in zip(server_complete.configuration.disk,
                                                     server_input.configuration.disk):
                    if input_disk.type.lower() == "ssd":
                        disk_list.append(ComponentSSD.from_dto(complete_disk, input_disk))
                    elif input_disk.type.lower() == "hdd":
                        disk_list.append(ComponentHDD.from_dto(complete_disk, input_disk))

            if server_complete.configuration.power_supply is not None:
                power_supply = ComponentPowerSupply.from_dto(server_complete.configuration.power_supply,
                                                             server_input.configuration.power_supply)
        if server_complete.model is not None and server_complete.model.type is not None:
            case_type = server_complete.model.type

        serv = cls(
            cpu=cpu,
            ram=ram_list,
            disk=disk_list,
            power_supply=power_supply,
            case_type=case_type
        )

        serv._set_states_from_input(server_input)

        return serv


class DeviceCloudInstance(DeviceServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    @classmethod
    def from_dto(cls, cloud: Cloud) -> 'DeviceCloudInstance':
        pass
