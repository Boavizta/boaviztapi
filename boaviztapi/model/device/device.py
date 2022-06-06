from abc import abstractmethod
from typing import List, Tuple

from pydantic import BaseModel

from boaviztapi.model.usage.usage import ModelUsage, ModelUsageServer, ModelUsageCloud
from boaviztapi.model.component import Component, ComponentCPU, ComponentRAM
from boaviztapi.dto.device import DeviceDTO

DEFAULT_SIG_FIGURES: int = 3

NumberSignificantFigures = Tuple[float, int]


class Device:

    def __init__(self):
        pass

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

    @classmethod
    def from_dto(cls, device: DeviceDTO) -> 'Device':
        pass


class Model(BaseModel):
    archetype: str = None
    name: str = None
    manufacturer: str = None
    year: int = None


class Device(BaseModel):
    config_components: List[Component] = None
    model: Model = None
    usage: ModelUsage = None

    class Config:
        arbitrary_types_allowed = True

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


class DeviceServer(Device):
    _DEFAULT_POWER_SUPPLY_NUMBER = 2
    _DEFAULT_CPU_NUMBER = 2
    _DEFAULT_SSD_NUMBER = 1
    _DEFAULT_RAM_NUMBER = 24
    _DEFAULT_PROFILE_NAME = "default"

    usage: ModelUsageServer = ModelUsageServer()

    profile_name: str = None

    def get_profile_name(self):
        if not self.profile_name:
            self.profile_name = self._DEFAULT_PROFILE_NAME
        return self.profile_name

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
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return self.usage.get_hours_electrical_consumption(profile) * self.usage.get_duration_hours() * self.usage.get_gwp_factor(), DEFAULT_SIG_FIGURES

    def impact_use_pe(self) -> (float, int):
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return self.usage.get_hours_electrical_consumption(profile) * self.usage.get_duration_hours() * self.usage.get_pe_factor(), DEFAULT_SIG_FIGURES

    def impact_use_adp(self) -> (float, int):
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return self.usage.get_hours_electrical_consumption(profile) * self.usage.get_duration_hours() * self.usage.get_adp_factor(), DEFAULT_SIG_FIGURES


class DeviceCloudInstance(DeviceServer):
    usage: ModelUsageCloud = ModelUsageCloud()

    _DEFAULT_PROFILE_NAME = "a1"

    def impact_manufacture_gwp(self) -> (float, int):
        return super().impact_manufacture_gwp()[0] / self.usage.get_instance_per_server(), \
               super().impact_manufacture_gwp()[1]

    def impact_manufacture_pe(self) -> (float, int):
        return super().impact_manufacture_pe()[0] / self.usage.get_instance_per_server(), \
               super().impact_manufacture_gwp()[1]

    def impact_manufacture_adp(self) -> (float, int):
        return super().impact_manufacture_adp()[0] / self.usage.get_instance_per_server(), \
               super().impact_manufacture_gwp()[1]

    def impact_use_gwp(self) -> (float, int):
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return super(profile).impact_use_gwp()[0] / self.usage.get_instance_per_server(), \
               super(profile).impact_manufacture_gwp()[1]

    def impact_use_pe(self) -> (float, int):
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return super(profile).impact_use_pe()[0] / self.usage.get_instance_per_server(), \
               super(profile).impact_manufacture_gwp()[1]

    def impact_use_adp(self) -> (float, int):
        profile = None
        if not self.usage.hours_electrical_consumption:
            profile = self.get_profile_name()
        return super(profile).impact_use_adp()[0] / self.usage.get_instance_per_server(), \
               super(profile).impact_manufacture_gwp()[1]
