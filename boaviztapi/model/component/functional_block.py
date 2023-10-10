from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component import Component
from boaviztapi.service.archetype import get_arch_value
from boaviztapi.service.factor_provider import get_iot_impact_factor


class ComponentFunctionalBlock(Component):
    NAME = "FUNCTIONAL_BLOCK"
    IMPACT_KEY = None

    def __init__(self, archetype=None, **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.hsl_level = Boattribute(
            unit="none",
            default=get_arch_value(archetype, 'hsl_level', 'default'),
            min=get_arch_value(archetype, 'hsl_level', 'min'),
            max=get_arch_value(archetype, 'hsl_level', 'max')
        )

    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        impact_factors = get_iot_impact_factor(self.IMPACT_KEY, self.hsl_level.value, impact_type)
        return impact_factors, impact_factors, impact_factors, []


class ActuatorsFunctionalBlock(ComponentFunctionalBlock):
    NAME = "ACTUATORS"
    IMPACT_KEY = "actuators"


class CasingFunctionalBlock(ComponentFunctionalBlock):
    NAME = "CASING"
    IMPACT_KEY = "casing"


class ConnectivityFunctionalBlock(ComponentFunctionalBlock):
    NAME = "CONNECTIVITY"
    IMPACT_KEY = "connectivity"


class MemoryFunctionalBlock(ComponentFunctionalBlock):
    NAME = "MEMORY"
    IMPACT_KEY = "memory"


class OthersFunctionalBlock(ComponentFunctionalBlock):
    NAME = "OTHERS"
    IMPACT_KEY = "others"


class PcbFunctionalBlock(ComponentFunctionalBlock):
    NAME = "PCB"
    IMPACT_KEY = "pcb"


class PowerSupplyFunctionalBlock(ComponentFunctionalBlock):
    NAME = "POWER_SUPPLY"
    IMPACT_KEY = "power_supply"


class SecuritySupplyFunctionalBlock(ComponentFunctionalBlock):
    NAME = "SECURITY"
    IMPACT_KEY = "security"


class ProcessingSupplyFunctionalBlock(ComponentFunctionalBlock):
    NAME = "PROCESSING"
    IMPACT_KEY = "processing"


class SensingSupplyFunctionalBlock(ComponentFunctionalBlock):
    NAME = "SENSING"
    IMPACT_KEY = "sensing"


class UserInterfaceSupplyFunctionalBlock(ComponentFunctionalBlock):
    NAME = "USER_INTERFACE"
    IMPACT_KEY = "user_interface"


def get_functional_block(name):
    if name == ActuatorsFunctionalBlock.NAME:
        return ActuatorsFunctionalBlock
    elif name == CasingFunctionalBlock.NAME:
        return CasingFunctionalBlock
    elif name == ConnectivityFunctionalBlock.NAME:
        return ConnectivityFunctionalBlock
    elif name == MemoryFunctionalBlock.NAME:
        return MemoryFunctionalBlock
    elif name == OthersFunctionalBlock.NAME:
        return OthersFunctionalBlock
    elif name == PcbFunctionalBlock.NAME:
        return PcbFunctionalBlock
    elif name == PowerSupplyFunctionalBlock.NAME:
        return PowerSupplyFunctionalBlock
    elif name == SecuritySupplyFunctionalBlock.NAME:
        return SecuritySupplyFunctionalBlock
    elif name == ProcessingSupplyFunctionalBlock.NAME:
        return ProcessingSupplyFunctionalBlock
    elif name == SensingSupplyFunctionalBlock.NAME:
        return SensingSupplyFunctionalBlock
    elif name == UserInterfaceSupplyFunctionalBlock.NAME:
        return UserInterfaceSupplyFunctionalBlock
    else:
        raise ValueError("Unknown functional block name: {}".format(name))