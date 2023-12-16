from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_arch_value, get_component_archetype


class ComponentCase(Component):
    AVAILABLE_CASE_TYPE = ['blade', 'rack']
    NAME = "CASE"

    def __init__(self, archetype=get_component_archetype(config["default_case"], "case"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.case_type = Boattribute(
            default=get_arch_value(archetype, 'case_type', 'default'),
            min=get_arch_value(archetype, 'case_type', 'min'),
            max=get_arch_value(archetype, 'case_type', 'max')
        )