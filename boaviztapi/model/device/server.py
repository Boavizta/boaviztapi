import itertools
from itertools import chain
from typing import List, Union, Any

from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM, ComponentSSD, ComponentHDD, \
    ComponentPowerSupply, ComponentCase, ComponentMotherboard, ComponentAssembly
from boaviztapi.model.device.device import Device, NumberSignificantFigures
from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.device import Server, Cloud


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
        self.__name = None                  # TODO: Set default name
        self.__manufacturer = None          # TODO: Set default manufacturer
        self.__manufacture_year = None      # TODO: Set default manufacture year
        self.__cpu_list = [self.DEFAULT_COMPONENT_CPU] * self.DEFAULT_NUMBER_CPU
        self.__ram_list = [self.DEFAULT_COMPONENT_RAM] * self.DEFAULT_NUMBER_RAM
        self.__disk_list = [self.DEFAULT_COMPONENT_DISK] * self.DEFAULT_NUMBER_DISK
        self.__power_supply_list = [self.DEFAULT_COMPONENT_POWER_SUPPLY] * self.DEFAULT_NUMBER_POWER_SUPPLY
        self.__case = self.DEFAULT_COMPONENT_CASE
        self.__motherboard = self.DEFAULT_COMPONENT_MOTHERBOARD
        self.__assembly = self.DEFAULT_COMPONENT_ASSEMBLY

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def manufacturer(self) -> str:
        return self.__manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str) -> None:
        self.__manufacturer = value

    @property
    def manufacture_year(self) -> str:
        return self.__manufacture_year

    @manufacture_year.setter
    def manufacture_year(self, value: str) -> None:
        self.__manufacture_year = value

    @property
    def cpu(self) -> List[ComponentCPU]:
        return self.__cpu_list

    @cpu.setter
    def cpu(self, value: List[ComponentCPU]) -> None:
        self.__cpu_list = value

    @property
    def ram(self) -> List[ComponentRAM]:
        return self.__ram_list

    @ram.setter
    def ram(self, value: List[ComponentRAM]) -> None:
        self.__ram_list = value

    @property
    def disk(self) -> List[Union[ComponentSSD, ComponentHDD]]:
        return self.__disk_list

    @disk.setter
    def disk(self, value: List[Union[ComponentSSD, ComponentHDD]]) -> None:
        self.__disk_list = value

    @property
    def power_supply(self) -> List[ComponentPowerSupply]:
        return self.__power_supply_list

    @power_supply.setter
    def power_supply(self, value: List[ComponentPowerSupply]) -> None:
        self.__power_supply_list = value

    @property
    def case(self) -> ComponentCase:
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
        return self.__motherboard

    @motherboard.setter
    def motherboard(self, value: ComponentMotherboard) -> None:
        self.__motherboard = value

    @property
    def assembly(self) -> ComponentAssembly:
        return self.__assembly

    @assembly.setter
    def assembly(self, value: ComponentAssembly) -> None:
        self.__assembly = value

    @property
    def components(self) -> List[Component]:
        return self.cpu + self.ram + self.disk + self.power_supply + [self.case] + [self.motherboard] + [self.assembly]

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        impacts = []
        significant_figures = [None]
        for component in self.components:
            impact, sign_fig = getattr(component, f'impact_manufacture_{impact_type}')()
            impacts.append(impact)
            significant_figures.append(sign_fig)
        return sum(impacts), min(significant_figures)

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

    @classmethod
    def from_dto(cls, server: Server) -> 'DeviceServer':
        cpu_list = cls.duplicate_component_on_units(server.configuration.cpu)
        ram_list = cls.duplicate_component_on_units(server.configuration.ram)
        disk_list = cls.duplicate_component_on_units(server.configuration.disk)
        power_supply_list = cls.duplicate_component_on_units(server.configuration.power_supply)
        return cls(
            name=server.model.name,
            manufacturer=server.model.manufacturer,
            manufacture_year=server.model.year,
            cpu=cpu_list,
            ram=ram_list,
            disk=disk_list,
            power_supply=power_supply_list,
            case_type=server.model.type
        )

    @staticmethod
    def duplicate_component_on_units(component_dto: Union[ComponentDTO, List[ComponentDTO]]) -> List[ComponentDTO]:
        if not isinstance(component_dto, list):
            component_dto = [component_dto]
        res = []
        for component_unit in component_dto:
            units = getattr(component_unit, 'units') or 1
            for _ in range(units):
                res.append(component_unit)
        return res


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
