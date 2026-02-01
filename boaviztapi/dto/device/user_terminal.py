from typing import Optional

from boaviztapi.dto.device import DeviceDTO
from boaviztapi.dto.usage import Usage
from boaviztapi.dto.usage.usage import mapper_usage
from boaviztapi.model.device import Device
from boaviztapi.model.device.userTerminal import (
    DeviceLaptop,
    DeviceDesktop,
    DeviceTablet,
    DeviceSmartphone,
    DeviceTelevision,
    DeviceBox,
    DeviceUsbStick,
    DeviceSmartWatch,
    DeviceExternalHDD,
    DeviceMonitor,
    DeviceExternalSSD,
    DeviceVrController,
    DeviceVrHeadset,
)
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


class VrHeadset(UserTerminal):
    type: Optional[str] = None


class VrController(UserTerminal):
    pass


def mapper_user_terminal(user_terminal_dto: UserTerminal, archetype) -> Device:
    if type(user_terminal_dto) is Laptop:
        model = DeviceLaptop(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) is Desktop:
        model = DeviceDesktop(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) is Tablet:
        model = DeviceTablet(archetype=archetype)
    elif type(user_terminal_dto) is Smartphone:
        model = DeviceSmartphone(archetype=archetype)
    elif type(user_terminal_dto) is Television:
        model = DeviceTelevision(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    elif type(user_terminal_dto) is Smartwatch:
        model = DeviceSmartWatch(archetype=archetype)
    elif type(user_terminal_dto) is Box:
        model = DeviceBox(archetype=archetype)
    elif type(user_terminal_dto) is UsbStick:
        model = DeviceUsbStick(archetype=archetype)
    elif type(user_terminal_dto) is ExternalHDD:
        model = DeviceExternalHDD(archetype=archetype)
    elif type(user_terminal_dto) is ExternalSSD:
        model = DeviceExternalSSD(archetype=archetype)
    elif type(user_terminal_dto) is Monitor:
        model = DeviceMonitor(archetype=archetype)
    elif type(user_terminal_dto) is VrController:
        model = DeviceVrController(archetype=archetype)
    elif type(user_terminal_dto) is VrHeadset:
        model = DeviceVrHeadset(archetype=archetype)
        model.type.set_input(user_terminal_dto.type)
    else:
        raise Exception("User Terminal Type not found")

    if user_terminal_dto.usage is not None:
        model.usage = mapper_usage(
            user_terminal_dto.usage, archetype=get_arch_component(archetype, "USAGE")
        )

    return model
