from typing import Tuple

import boaviztapi.utils.roundit as rd
from boaviztapi.model.component.component import Component, NumberSignificantFigures
from boaviztapi.dto.component import CPU
from boaviztapi.model.boattribute import Boattribute, Status


class ComponentCPU(Component):
    DEFAULT_CPU_DIE_SIZE_PER_CORE = 0.245
    DEFAULT_CPU_CORE_UNITS = 24
    DEFAULT_CPU_MANUFACTURER = 'Intel'
    DEFAULT_CPU_FAMILY = 'Skylake'
    DEFAULT_MODEL_RANGE = 'Xeon Platinum'

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 1.97,
            'impact': 9.14
        },
        'pe': {
            'die_impact': 26.50,
            'impact': 156.00
        },
        'adp': {
            'die_impact': 5.80E-07,
            'impact': 2.04E-02
        },
        'constant_core_impact': 0.491
    }

    def __init__(self, /, **kwargs):
        super().__init__(**kwargs)

        self.__core_units = Boattribute(value=None, status=Status.NONE, unit="none")
        self.__die_size_per_core = Boattribute(value=None, status=Status.NONE, unit="mm2")
        self.__model_range = Boattribute(value=None, status=Status.NONE, unit="none")
        self.__manufacturer = Boattribute(value=None, status=Status.NONE, unit="..")
        self.__model_range = Boattribute(value=None, status=Status.NONE, unit="none")
        self.__family = Boattribute(value=None, status=Status.NONE, unit="none")

        for attr, val in kwargs.items():
            if val is not None and hasattr(self, f'_ComponentCPU__{attr}'):
                self.__setattr__(attr, val)

    @property
    def core_units(self) -> int:
        if self.__core_units.value is None:
            self.__core_units.value = self.DEFAULT_CPU_CORE_UNITS
            self.__core_units.status = Status.DEFAULT
        return self.__core_units.value

    @core_units.setter
    def core_units(self, value: int) -> None:
        self.__core_units.value = value

    @property
    def die_size_per_core(self) -> float:
        if self.__die_size_per_core.value is None:
            self.__die_size_per_core.value = self.DEFAULT_CPU_DIE_SIZE_PER_CORE
            self.__die_size_per_core.status = Status.DEFAULT
        return self.__die_size_per_core.value

    @die_size_per_core.setter
    def die_size_per_core(self, value: float) -> None:
        self.__die_size_per_core.value = value

    @property
    def die_size(self) -> float:
        return self.die_size_per_core * self.core_units

    @die_size.setter
    def die_size(self, value: float) -> None:
        self.__die_size_per_core.value = value / self.core_units

    @property
    def manufacturer(self) -> str:
        if self.__manufacturer.value is None:
            self.__manufacturer.value = self.DEFAULT_CPU_MANUFACTURER
            self.__manufacturer.status = Status.DEFAULT
        return self.__manufacturer.value

    @manufacturer.setter
    def manufacturer(self, value: str) -> None:
        self.__manufacturer.value = value

    @property
    def family(self) -> str:
        return self.__family.value

    @family.setter
    def family(self, value: str) -> None:
        self.__family.value = value

    @property
    def model_range(self) -> str:
        if self.__model_range.value is None:
            self.__model_range.value = self.DEFAULT_MODEL_RANGE
            self.__model_range.status = Status.DEFAULT
        return self.__model_range.value

    @model_range.setter
    def model_range(self, value: str) -> None:
        self.__model_range.value = value

    # @property
    # def name(self):
    #     # TODO: Maybe we don't need this getter?
    #     raise NotImplementedError
    #
    # @name.setter
    # def name(self, value: str) -> None:
    #     # TODO: Implement cpu name parser into (manufacture, family, model_range)
    #     raise NotImplementedError

    def impact_manufacture_gwp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> NumberSignificantFigures:
        core_impact, cpu_die_impact, cpu_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(core_impact, cpu_die_impact, cpu_impact)
        impact = self.__compute_impact_manufacture(core_impact, cpu_die_impact, cpu_impact)
        return impact, sign_figures

    def __get_impact_constants(self, impact_type: str) -> Tuple[float, float, float]:
        core_impact = self.IMPACT_FACTOR['constant_core_impact']
        cpu_die_impact = self.IMPACT_FACTOR[impact_type]['die_impact']
        cpu_impact = self.IMPACT_FACTOR[impact_type]['impact']
        return core_impact, cpu_die_impact, cpu_impact

    def __compute_significant_numbers(self, core_impact: float, cpu_die_impact: float, cpu_impact: float) -> int:
        return rd.min_significant_figures(self.die_size_per_core, core_impact, cpu_die_impact, cpu_impact)

    def __compute_impact_manufacture(self, core_impact: float, cpu_die_impact: float, cpu_impact: float) -> float:
        return (self.core_units * self.die_size_per_core + core_impact) * cpu_die_impact + cpu_impact

    def impact_manufacture_pe(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> NumberSignificantFigures:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_pe(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def impact_use_adp(self) -> NumberSignificantFigures:
        raise NotImplementedError

    def to_dto(self, original_cpu: CPU) -> CPU:
        cpu = CPU()
        for attr, val in original_cpu.dict().items():
            if hasattr(self, f'_ComponentCPU__{attr}'):
                cpu.__setattr__(attr, self.__getattribute__(attr))
            else:
                cpu.__setattr__(attr, original_cpu.__getattribute__(attr))
        return cpu