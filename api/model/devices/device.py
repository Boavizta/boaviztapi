from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from api.model.components.usage import Usage
from api.model.components.component import Component, ComponentCPU, ComponentSSD, ComponentRAM, ComponentPowerSupply, \
    ComponentMotherBoard, ComponentAssembly, ComponentRack, ComponentBlade


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
        print("IN SMART COMPLETE DATA")

        self.usage.smart_complete_data()

        if not self.config_components:
            print("not self.config_components")
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
                if type(item) == type(ComponentCPU):
                    print("type: {} res: {}".format(type(item), ComponentCPU))
                    cpu = True
                elif type(item) == type(ComponentRAM):
                    print("type: {} res: {}".format(type(item), ComponentRAM))
                    ram = True
                elif type(item) == type(ComponentSSD):
                    print("type: {} res: {}".format(type(item), ComponentSSD))
                    ssd = True
                elif type(item) == type(ComponentPowerSupply):
                    print("type: {} res: {}".format(type(item), ComponentPowerSupply))
                    power_supply = True
                elif type(item) == type(ComponentRack) or type(item) == type(ComponentBlade):
                    print("type: {} res: {}".format(type(item), ComponentRack))
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
