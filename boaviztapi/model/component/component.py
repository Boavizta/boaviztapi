from abc import abstractmethod

from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.usage import ModelUsage
from boaviztapi.service.archetype import get_arch_value, get_arch_component


class Component:
    NAME = "COMPONENT"

    def __init__(self, archetype=None, **kwargs):
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

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        if not self.usage.avg_power.is_set():
            raise NotImplementedError
        impact_factor = self.usage.elec_factors[impact_type]

        impacts = impact_factor.value * (self.usage.avg_power.value / 1000) * self.usage.use_time_ratio.value * duration

        max_impact = impact_factor.max * (self.usage.avg_power.max / 1000) * self.usage.use_time_ratio.min * duration
        min_impact = impact_factor.min * (self.usage.avg_power.min / 1000) * self.usage.use_time_ratio.max * duration

        return impacts, min_impact, max_impact, []

    @abstractmethod
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        raise NotImplementedError
