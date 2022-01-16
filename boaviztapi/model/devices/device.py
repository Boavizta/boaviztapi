from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from boaviztapi.model.components.usage import Usage
from boaviztapi.model.components.component import Component, ComponentCPU, ComponentSSD, ComponentRAM, ComponentPowerSupply, \
    ComponentMotherBoard, ComponentAssembly, ComponentRack


class Model(BaseModel):

    archetype: str = None
    name: str = None
    manufacturer: str = None
    year: int = None


class Device(BaseModel):
    config_components: List[Component] = None
    model: Model = None
    usage: Usage = None

    @abstractmethod
    def impact_manufacture_gwp(self) -> float:
        pass

    @abstractmethod
    def impact_manufacture_pe(self) -> float:
        pass

    @abstractmethod
    def impact_manufacture_adp(self) -> float:
        pass

    @abstractmethod
    def impact_use_gwp(self) -> float:
        pass

    @abstractmethod
    def impact_use_pe(self) -> float:
        pass

    @abstractmethod
    def impact_use_adp(self) -> float:
        pass

    @abstractmethod
    def smart_complete_data(self):
        pass


class Server(Device):

    _DEFAULT_POWER_SUPPLY_NUMBER = 2
    _DEFAULT_CPU_NUMBER = 2
    _DEFAULT_SSD_NUMBER = 1
    _DEFAULT_RAM_NUMBER = 24

    def impact_manufacture_gwp(self) -> float:
        return sum([item.impact_gwp() for item in self.config_components])

    def impact_manufacture_pe(self) -> float:
        return sum([item.impact_pe() for item in self.config_components])

    def impact_manufacture_adp(self) -> float:
        return sum([item.impact_adp() for item in self.config_components])

    def impact_use_gwp(self) -> float:
        return self.usage.impact_gwp()

    def impact_use_pe(self) -> float:
        return self.usage.impact_pe()

    def impact_use_adp(self) -> float:
        return self.usage.impact_adp()

    def smart_complete_data(self):

        if self.usage is not None:
            self.usage.smart_complete_data()

        if not self.config_components:
            self.config_components = self.get_default_configuration_component_list()
        else:
            self.config_components.append(ComponentMotherBoard())
            self.config_components.append(ComponentAssembly())

            cpu = False
            ram = False
            ssd = False
            power_supply = False
            rack_blade = False

            for item in self.config_components:
                if type(item).__name__ == "ComponentCPU":
                    cpu = True
                elif type(item).__name__ == "ComponentRAM":
                    ram = True
                elif type(item).__name__ == "ComponentSSD":
                    # TODO: SSD OR HDD
                    ssd = True
                elif type(item).__name__ == "ComponentPowerSupply":
                    power_supply = True
                elif type(item).__name__ == "ComponentRack" or type(item).__name__ == "ComponentBlade":
                    rack_blade = True

            if not cpu:
                self.config_components += [*self.get_default_cpu()]
            if not ram:
                self.config_components += [*self.get_default_ram()]
            if not ssd:
                self.config_components += [*self.get_default_ssd()]
            if not power_supply:
                self.config_components += [*self.get_default_power_supply()]
            if not rack_blade:
                self.config_components += [ComponentRack()]

        for item in self.config_components:
            item.smart_complete_data()

    def get_default_cpu(self) -> List[Component]:
        return [ComponentCPU() for _ in range(self._DEFAULT_CPU_NUMBER)]

    def get_default_ram(self) -> List[Component]:
        return [ComponentRAM() for _ in range(self._DEFAULT_RAM_NUMBER)]

    def get_default_ssd(self) -> List[Component]:
        return [ComponentSSD() for _ in range(self._DEFAULT_SSD_NUMBER)]

    def get_default_power_supply(self) -> List[Component]:
        return [ComponentPowerSupply() for _ in range(self._DEFAULT_POWER_SUPPLY_NUMBER)]

    def get_default_configuration_component_list(self) -> List[Component]:
        components = [*self.get_default_cpu(), *self.get_default_ssd(), *self.get_default_ram(),
                      *self.get_default_power_supply(), ComponentMotherBoard(), ComponentAssembly()]
        return components
