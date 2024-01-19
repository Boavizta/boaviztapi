import os

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_cpu_name, fuzzymatch_attr_from_pdf

_cpu_specs = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/cpu_specs.csv'))


def attributes_from_cpu_name(cpu_name: str):
    return fuzzymatch_attr_from_cpu_name(cpu_name, _cpu_specs)


class ComponentGPU(Component):
    NAME = "GPU"
    name_completion = False

    def __init__(self, archetype=get_component_archetype(config["default_gpu"], "gpu"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.gpu_die_size = Boattribute(
            # complete_function=self._complete_die_size,
            unit="mm2",
            default=get_arch_value(archetype, 'die_size', 'default'),
            min=get_arch_value(archetype, 'die_size', 'min'),
            max=get_arch_value(archetype, 'die_size', 'max')
        )
        self.gpu_process = Boattribute(
            unit="nm",
            default=get_arch_value(archetype, 'die_size', 'default'),
            min=get_arch_value(archetype, 'die_size', 'min'),
            max=get_arch_value(archetype, 'die_size', 'max')
        )
        self.gpu_name = Boattribute(
            # complete_function=self._complete_die_size,
            default=get_arch_value(archetype, 'name', 'default'),
            min=get_arch_value(archetype, 'name', 'min'),
            max=get_arch_value(archetype, 'name', 'max')
        )
        self.gpu_variant = Boattribute(
            # complete_function=self._complete_die_size,
            default=get_arch_value(archetype, 'variant', 'default'),
            min=get_arch_value(archetype, 'variant', 'min'),
            max=get_arch_value(archetype, 'variant', 'max')
        )
        self.gpu_architecture = Boattribute(
            # complete_function=self._complete_die_size,
            default=get_arch_value(archetype, 'architecture', 'default'),
            min=get_arch_value(archetype, 'architecture', 'min'),
            max=get_arch_value(archetype, 'architecture', 'max')
        )
        self.vram_capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'vram_capacity', 'default'),
            min=get_arch_value(archetype, 'vram_capacity', 'min'),
            max=get_arch_value(archetype, 'vram_capacity', 'max')
        )
        self.vram_density = Boattribute(
            # complete_function=self._complete_density,
            unit="GB/cm2",
            default=get_arch_value(archetype, 'vram_density', 'default'),
            min=get_arch_value(archetype, 'vram_density', 'min'),
            max=get_arch_value(archetype, 'vram_density', 'max')
        )
        self.manufacturer = Boattribute(
            default=get_arch_value(archetype, 'manufacturer', 'default'),
            min=get_arch_value(archetype, 'manufacturer', 'min'),
            max=get_arch_value(archetype, 'manufacturer', 'max')
        )
        self.family = Boattribute(
            # complete_function=self._complete_from_name,
            default=get_arch_value(archetype, 'family', 'default'),
            min=get_arch_value(archetype, 'family', 'min'),
            max=get_arch_value(archetype, 'family', 'max')
        )
        self.name = Boattribute(
            default=get_arch_value(archetype, 'name', 'default'),
            min=get_arch_value(archetype, 'name', 'min'),
            max=get_arch_value(archetype, 'name', 'max')
        )
        self.tdp = Boattribute(
            # complete_function=self._complete_from_name,
            unit="W",
            default=get_arch_value(archetype, 'tdp', 'default'),
            min=get_arch_value(archetype, 'tdp', 'min'),
            max=get_arch_value(archetype, 'tdp', 'max')
        )
        self.pcb_size = Boattribute(
            default=get_arch_value(archetype, 'pcb_size', 'default'),
            min=get_arch_value(archetype, 'pcb_size', 'min'),
            max=get_arch_value(archetype, 'pcb_size', 'max')
        )
        self.pcie = Boattribute(
            default=get_arch_value(archetype, 'pcie', 'default'),
            min=get_arch_value(archetype, 'pcie', 'min'),
            max=get_arch_value(archetype, 'pcie', 'max')
        )
