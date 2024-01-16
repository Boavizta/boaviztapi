from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.impact import Assessable
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_arch_value, get_arch_component


class Component(Assessable):
    NAME = "COMPONENT"

    def __init__(self, archetype=None, **kwargs):
        super().__init__(**kwargs)
        self.impact_factor = {}
        self.archetype = archetype
        self.units = Boattribute(
            default=get_arch_value(archetype, 'units', 'default', default=1),
            min=get_arch_value(archetype, 'units', 'min'),
            max=get_arch_value(archetype, 'units', 'max')
        )
        self._usage = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    @property
    def usage(self) -> ModelUsage:
        if self._usage is None:
            self._usage = ModelUsage(archetype=get_arch_component(self.archetype, "USAGE"))
        return self._usage

    @usage.setter
    def usage(self, value: int) -> None:
        self._usage = value
