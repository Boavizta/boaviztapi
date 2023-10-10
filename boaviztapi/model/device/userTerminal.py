from abc import abstractmethod, ABC

from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_arch_value, get_user_terminal_archetype, get_arch_component
from boaviztapi.service.factor_provider import get_impact_factor


class EndUserDevice(Device):
    NAME = None

    def __init__(self, archetype=None, **kwargs):
        super().__init__(archetype=archetype, **kwargs)

    @property
    def usage(self) -> ModelUsage:
        if self._usage is None:
            self._usage = ModelUsage(archetype=get_arch_component(self.archetype, "USAGE"))
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value

    @abstractmethod
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = float(get_impact_factor(item=self.NAME, impact_type=impact_type)["impact"])
        min_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)["impact"])
        max_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)["impact"])

        warnings = ["Generic data used for impact calculation."]

        return impact, min_impacts, max_impacts, warnings

    @abstractmethod
    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        impact_factor = self.usage.elec_factors[impact_type]
        impact = impact_factor.value * (self.usage.avg_power.value / 1000) * self.usage.use_time_ratio.value * duration
        min_impact = impact_factor.min * (self.usage.avg_power.min / 1000) * self.usage.use_time_ratio.min * duration
        max_impact = impact_factor.max * (self.usage.avg_power.max / 1000) * self.usage.use_time_ratio.max * duration

        return impact, min_impact, max_impact, []

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class DeviceLaptop(EndUserDevice, ABC):
    NAME = "LAPTOP"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_laptop"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.type = Boattribute(
            default=get_arch_value(archetype, 'type', 'default'),
            min=get_arch_value(archetype, 'type', 'min'),
            max=get_arch_value(archetype, 'type', 'max')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        min_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        max_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])

        warnings = ["Generic data used for impact calculation."]

        return impact, min_impacts, max_impacts, warnings


class DeviceDesktop(EndUserDevice, ABC):
    NAME = "DESKTOP"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_desktop"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.type = Boattribute(
            default=get_arch_value(archetype, 'type', 'default'),
            min=get_arch_value(archetype, 'type', 'min'),
            max=get_arch_value(archetype, 'type', 'max')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        min_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        max_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])

        warnings = ["Generic data used for impact calculation."]

        return impact, min_impacts, max_impacts, warnings


class DeviceTablet(EndUserDevice, ABC):
    NAME = "TABLET"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_tablet"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceSmartphone(EndUserDevice, ABC):
    NAME = "SMARTPHONE"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_smartphone"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceTelevision(EndUserDevice, ABC):
    NAME = "TELEVISION"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_television"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.type = Boattribute(
            default=get_arch_value(archetype, 'type', 'default'),
            min=get_arch_value(archetype, 'type', 'min'),
            max=get_arch_value(archetype, 'type', 'max')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        min_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])
        max_impacts = float(get_impact_factor(item=self.NAME, impact_type=impact_type)[self.type.value]["impact"])

        warnings = ["Generic data used for impact calculation."]

        return impact, min_impacts, max_impacts, warnings


class DeviceSmartWatch(EndUserDevice, ABC):
    NAME = "SMARTWATCH"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_smartwatch"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceBox(EndUserDevice, ABC):
    NAME = "BOX"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_box"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceUsbStick(EndUserDevice, ABC):
    NAME = "USB_STICK"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_usb_stick"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceExternalSSD(EndUserDevice, ABC):
    NAME = "EXTERNAL_SSD"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_external_ssd"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceExternalHDD(EndUserDevice, ABC):
    NAME = "EXTERNAL_HDD"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_external_hdd"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)


class DeviceMonitor(EndUserDevice, ABC):
    NAME = "MONITOR"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_monitor"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
