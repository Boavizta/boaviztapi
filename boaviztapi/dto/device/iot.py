from typing import Optional, List

from boaviztapi.dto.component.other import FunctionalBlock
from boaviztapi.dto.device import DeviceDTO
from boaviztapi.dto.usage import Usage
from boaviztapi.dto.usage.usage import mapper_usage
from boaviztapi.model.component.functional_block import get_functional_block
from boaviztapi.model.device.iot import DeviceIoT, ComponentFunctionalBlock
from boaviztapi.service.archetype import get_arch_component


class IoT(DeviceDTO):
    functional_blocks: Optional[List[FunctionalBlock]] = []
    usage: Optional[Usage] = None


def mapper_iot_device(dto_iot: IoT, archetype):
    model = DeviceIoT(archetype=archetype)

    for functional_block in dto_iot.functional_blocks:
        class_functional_block = get_functional_block(functional_block.type.upper())
        model_functional_block = class_functional_block(archetype=get_arch_component(archetype, class_functional_block.NAME))
        model_functional_block.hsl_level.set_input(functional_block.hsl_level)
        model.add_functional_block(model_functional_block)

    if dto_iot.usage is not None:
        model.usage = mapper_usage(dto_iot.usage, archetype=get_arch_component(archetype, "USAGE"))

    return model
