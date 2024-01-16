from abc import ABC

from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.device import Device
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_arch_value, get_user_terminal_archetype, get_arch_component


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

class DeviceDesktop(EndUserDevice, ABC):
    NAME = "DESKTOP"

    def __init__(self, archetype=get_user_terminal_archetype(config["default_desktop"]), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.type = Boattribute(
            default=get_arch_value(archetype, 'type', 'default'),
            min=get_arch_value(archetype, 'type', 'min'),
            max=get_arch_value(archetype, 'type', 'max')
        )

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
