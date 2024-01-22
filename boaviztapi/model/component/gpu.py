import os

import pandas as pd

from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_gpu_name

_gpu_specs = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/gpu_specs.csv'))


class ComponentGPU(Component):
    NAME = "GPU"
    name_completion = False

    def __init__(self, archetype=get_component_archetype(config["default_gpu"], "gpu"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.name = Boattribute(
            default=get_arch_value(archetype, 'name', 'default'),
            min=get_arch_value(archetype, 'name', 'min'),
            max=get_arch_value(archetype, 'name', 'max')
        )
        self.gpu_die_size = Boattribute(
            complete_function=self._complete_from_name,
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
            default=get_arch_value(archetype, 'name', 'default'),
            min=get_arch_value(archetype, 'name', 'min'),
            max=get_arch_value(archetype, 'name', 'max')
        )
        self.gpu_variant = Boattribute(
            default=get_arch_value(archetype, 'variant', 'default'),
            min=get_arch_value(archetype, 'variant', 'min'),
            max=get_arch_value(archetype, 'variant', 'max')
        )
        self.gpu_architecture = Boattribute(
            default=get_arch_value(archetype, 'architecture', 'default'),
            min=get_arch_value(archetype, 'architecture', 'min'),
            max=get_arch_value(archetype, 'architecture', 'max')
        )
        self.vram_capacity = Boattribute(
            complete_function=self._complete_from_name,
            unit="GB",
            default=get_arch_value(archetype, 'vram_capacity', 'default'),
            min=get_arch_value(archetype, 'vram_capacity', 'min'),
            max=get_arch_value(archetype, 'vram_capacity', 'max')
        )
        self.vram_density = Boattribute(
            complete_function=self._complete_density,
            unit="GB/mm2",
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
            default=get_arch_value(archetype, 'family', 'default'),
            min=get_arch_value(archetype, 'family', 'min'),
            max=get_arch_value(archetype, 'family', 'max')
        )
        self.tdp = Boattribute(
            complete_function=self._complete_from_name,
            unit="W",
            default=get_arch_value(archetype, 'tdp', 'default'),
            min=get_arch_value(archetype, 'tdp', 'min'),
            max=get_arch_value(archetype, 'tdp', 'max')
        )
        self.pcb_size = Boattribute(
            complete_function=self._complete_from_name,
            default=get_arch_value(archetype, 'pcb_size', 'default'),
            min=get_arch_value(archetype, 'pcb_size', 'min'),
            max=get_arch_value(archetype, 'pcb_size', 'max')
        )
        self.pcie = Boattribute(
            default=get_arch_value(archetype, 'pcie', 'default'),
            min=get_arch_value(archetype, 'pcie', 'min'),
            max=get_arch_value(archetype, 'pcie', 'max')
        )

    def _complete_from_name(self) -> None:
        attr = fuzzymatch_attr_from_gpu_name(self.name.value, _gpu_specs)
        self.tdp.set_completed(attr[1])
        self.gpu_die_size.set_completed(attr[2])
        self.vram_capacity.set_completed(attr[3])
        self.pcb_size.set_completed(attr[4])

    def _complete_density(self) -> None:
        self.vram_density.set_completed(value=0.01625)
