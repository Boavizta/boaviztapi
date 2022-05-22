from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from boaviztapi.model.usage.usage import Usage, UsageServer, UsageCloud
from boaviztapi.model.components.component import Component, ComponentCPU, ComponentSSD, ComponentRAM, \
    ComponentPowerSupply, ComponentMotherBoard, ComponentAssembly, ComponentCase

DEFAULT_SIG_FIGURES: int = 3


class Model(BaseModel):
    archetype: str = None
    name: str = None
    manufacturer: str = None
    year: int = None


class Device(BaseModel):
    config_components: List[Component] = None
    model: Model = None
    usage: Usage = None

    def get_config_components(self):
        if not self.config_components:
            self.config_components = []
        return self.config_components

    def __eq__(self, other):
        self.config_components.sort(key=lambda x: x.hash, reverse=True)
        other.config_components.sort(key=lambda x: x.hash, reverse=True)
        if self.config_components.__eq__(other.config_components) \
                and self.model.__eq__(other.model) \
                and self.usage.__eq__(other.usage):
            return True
        return False

    @abstractmethod
    def impact_manufacture_gwp(self) -> (float, int):
        pass

    @abstractmethod
    def impact_manufacture_pe(self) -> (float, int):
        pass

    @abstractmethod
    def impact_manufacture_adp(self) -> (float, int):
        pass

    @abstractmethod
    def impact_use_gwp(self) -> (float, int):
        pass

    @abstractmethod
    def impact_use_pe(self) -> (float, int):
        pass

    @abstractmethod
    def impact_use_adp(self) -> (float, int):
        pass


class Server(Device):
    _DEFAULT_POWER_SUPPLY_NUMBER = 2
    _DEFAULT_CPU_NUMBER = 2
    _DEFAULT_SSD_NUMBER = 1
    _DEFAULT_RAM_NUMBER = 24

    usage: UsageServer = UsageServer()

    def get_config_components(self):
        if not self.config_components:
            self.config_components = self.get_default_configuration_component_list()
        else:
            self.config_components.append(ComponentMotherBoard())
            self.config_components.append(ComponentAssembly())

            cpu = False
            ram = False
            ssd = False
            power_supply = False
            case = False

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
                elif type(item).__name__ == "ComponentCase":
                    case = True

            if not cpu:
                self.config_components += [*self.get_default_cpu()]
            if not ram:
                self.config_components += [*self.get_default_ram()]
            if not ssd:
                self.config_components += [*self.get_default_ssd()]
            if not power_supply:
                self.config_components += [*self.get_default_power_supply()]
            if not case:
                self.config_components += [ComponentCase()]

        return self.config_components

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
                      *self.get_default_power_supply(), ComponentMotherBoard(), ComponentAssembly(), ComponentCase()]
        return components

    def impact_manufacture_gwp(self) -> (float, int):
        impacts = [item.impact_manufacture_gwp() for item in self.config_components]
        sum_impacts = sum(item[0] for item in impacts)
        significant_figure = min(item[1] for item in impacts)
        return sum_impacts, significant_figure

    def impact_manufacture_pe(self) -> (float, int):
        impacts = [item.impact_manufacture_pe() for item in self.config_components]
        sum_impacts = sum(item[0] for item in impacts)
        significant_figure = min(item[1] for item in impacts)
        return sum_impacts, significant_figure

    def impact_manufacture_adp(self) -> (float, int):
        impacts = [item.impact_manufacture_adp() for item in self.config_components]
        sum_impacts = sum(item[0] for item in impacts)
        significant_figure = min(item[1] for item in impacts)
        return sum_impacts, significant_figure

    def impact_use_gwp(self) -> (float, int):
        return self.usage.get_hours_electrical_consumption() * self.usage.get_duration_hours() * self.usage.get_gwp_factor(), DEFAULT_SIG_FIGURES

    def impact_use_pe(self) -> (float, int):
        return self.usage.get_hours_electrical_consumption() * self.usage.get_duration_hours() * self.usage.get_pe_factor(), DEFAULT_SIG_FIGURES

    def impact_use_adp(self) -> (float, int):
        return self.usage.get_hours_electrical_consumption() * self.usage.get_duration_hours() * self.usage.get_adp_factor(), DEFAULT_SIG_FIGURES


class CloudInstance(Server):
    usage: UsageCloud = UsageCloud()

    def impact_manufacture_gwp(self) -> (float, int):
        return super().impact_manufacture_gwp()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]

    def impact_manufacture_pe(self) -> (float, int):
        return super().impact_manufacture_pe()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]

    def impact_manufacture_adp(self) -> (float, int):
        return super().impact_manufacture_adp()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]

    def impact_use_gwp(self) -> (float, int):
        return super().impact_use_gwp()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]

    def impact_use_pe(self) -> (float, int):
        return super().impact_use_pe()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]

    def impact_use_adp(self) -> (float, int):
        return super().impact_use_adp()[0] / self.usage.instance_per_server, super().impact_manufacture_gwp()[1]
