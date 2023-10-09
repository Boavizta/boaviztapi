from typing import Optional

from boaviztapi.dto.device import DeviceDTO
from boaviztapi.dto.usage import Usage
from boaviztapi.dto.usage.usage import mapper_usage
from boaviztapi.model.device import Device
from boaviztapi.model.device.userTerminal import DeviceLaptop, DeviceDesktop, DeviceTablet, DeviceSmartphone, \
    DeviceTelevision, DeviceBox, DeviceUsbStick, DeviceSmartWatch, DeviceExternalHDD, DeviceMonitor, DeviceExternalSSD
from boaviztapi.service.archetype import get_arch_component


class UserTerminal(DeviceDTO):
    usage: Optional[Usage] = None


class Laptop(UserTerminal):
    type: Optional[str] = None


class Desktop(UserTerminal):
    type: Optional[str] = None


class Tablet(UserTerminal):
    pass


class Smartphone(UserTerminal):
    pass


class Television(UserTerminal):
    type: Optional[str] = None


class Smartwatch(UserTerminal):
    pass


class Box(UserTerminal):
    pass


class UsbStick(UserTerminal):
    pass


class ExternalHDD(UserTerminal):
    pass


class Monitor(UserTerminal):
    pass


class ExternalSSD(UserTerminal):
    pass


def mapper_user_terminal(user_terminal_dto: UserTerminal, archetype) -> Device:
    if type(user_terminal_dto) == Laptop:
        model = DeviceLaptop(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) == Desktop:
        model = DeviceDesktop(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) == Tablet:
        model = DeviceTablet(archetype=archetype)
    elif type(user_terminal_dto) == Smartphone:
        model = DeviceSmartphone(archetype=archetype)
    elif type(user_terminal_dto) == Television:
        model = DeviceTelevision(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) == Smartwatch:
        model = DeviceSmartWatch(archetype=archetype)
    elif type(user_terminal_dto) == Box:
        model = DeviceBox(archetype=archetype)
    elif type(user_terminal_dto) == UsbStick:
        model = DeviceUsbStick(archetype=archetype)
    elif type(user_terminal_dto) == ExternalHDD:
        model = DeviceExternalHDD(archetype=archetype)
    elif type(user_terminal_dto) == ExternalSSD:
        model = DeviceExternalSSD(archetype=archetype)
    elif type(user_terminal_dto) == Monitor:
        model = DeviceMonitor(archetype=archetype)
    else:
        raise Exception("User Terminal Type not found")

    if user_terminal_dto.usage is not None:
        model.usage = mapper_usage(user_terminal_dto.usage, archetype=get_arch_component(archetype, "USAGE"))

    return model
