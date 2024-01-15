from typing import List

from boaviztapi import config
from boaviztapi.model.component.functional_block import ComponentFunctionalBlock, get_functional_block
from boaviztapi.model.device import Device
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_arch_component, get_iot_device_archetype


class DeviceIoT(Device):
    NAME = "IOT_DEVICE"
    WARNINGS = ["Connected object, not including associated digital services (use of network, datacenter, "
                "virtual machines or other terminals not included)", "Do not include the impact of distribution"]

    def __init__(self, archetype=get_iot_device_archetype(config["default_iot_device"]),
                 functional_block: List[ComponentFunctionalBlock] = None):
        super().__init__(archetype=archetype)

        if functional_block is None:
            functional_block = []

        self._functional_block = functional_block

    @property
    def components(self) -> List[ComponentFunctionalBlock]:
        if not self._functional_block:
            for fb in self.archetype:
                if fb == "USAGE":
                    continue
                if self.archetype[fb]["hsl_level"] != {}:
                    self._functional_block.append(get_functional_block(fb)(
                        archetype=get_arch_component(self.archetype, fb)))
        return self._functional_block

    def add_functional_block(self, functional_block):
        self._functional_block.append(functional_block)

    @property
    def usage(self) -> ModelUsage:
        if self._usage is None:
            self._usage = ModelUsage(archetype=get_arch_component(self.archetype, "USAGE"))
        return self._usage

    @usage.setter
    def usage(self, value):
        self._usage = value