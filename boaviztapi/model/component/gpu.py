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
            complete_function=self._complete_die_size,
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
            complete_function=self._complete_from_name,
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
            complete_function=self._complete_from_name,
            unit="W",
            default=get_arch_value(archetype, 'tdp', 'default'),
            min=get_arch_value(archetype, 'tdp', 'min'),
            max=get_arch_value(archetype, 'tdp', 'max')
        )

    def _complete_die_size(self):
        # Make sure all data have been completed from name
        if self.name.has_value():
            self._complete_from_name()

        # If the die_size_per_core have been set we have nothing to do
        if self.die_size.is_set():
            return None

        # If we have a die_size_per_core and core_units, we can compute the die_size
        elif self.die_size_per_core.is_set() and self.core_units.is_set():
            self.die_size.set_completed(value=float(self.die_size_per_core.value * self.core_units.value),
                                        source="die_size_per_core*core_units")
            return None

        # If we cannot have a family, but we have a default die_size we use it
        elif self.die_size.has_value() and not self.family.has_value():
            self.die_size.set_archetype(self.die_size.default)
            return None

        # If the above completion strategies cannot be applied, we use our cpu specs file
        else:
            self._complete_die_size_from_cpu_specs()

    def _complete_from_name(self):
        if self.name.has_value() and not self.name_completion:
            compute_min_max = False
            if self.name.min != self.name.value or self.name.max != self.name.value:
                compute_min_max = True

            cpu_attributes = attributes_from_cpu_name(self.name.value)
            name, manufacturer, family, model_range, tdp, cores, threads, die_size, die_size_source, source = cpu_attributes if (
                    cpu_attributes is not None) else (None, None, None, None, None, None, None, None, None)

            if compute_min_max:
                cpu_attributes_min = attributes_from_cpu_name(self.name.min)
                cpu_attributes_max = attributes_from_cpu_name(self.name.max)
                name_min, manufacturer_min, family_min, model_range_min, tdp_min, cores_min, threads_min, die_size_min, die_size_source_min, source_min = cpu_attributes_min if (
                        cpu_attributes_min is not None) else (None, None, None, None, None, None, None, None, None)
                name_max, manufacturer_max, family_max, model_range_max, tdp_max, cores_max, threads_max, die_size_max, die_size_source_max, source_max = cpu_attributes_max if (
                        cpu_attributes_max is not None) else (None, None, None, None, None, None, None, None, None)
            else:
                name_min, manufacturer_min, family_min, model_range_min, tdp_min, cores_min, threads_min, die_size_min, die_size_source_min, source_min = name, manufacturer, family, model_range, tdp, cores, threads, die_size, die_size_source, source
                name_max, manufacturer_max, family_max, model_range_max, tdp_max, cores_max, threads_max, die_size_max, die_size_source_max, source_max = name, manufacturer, family, model_range, tdp, cores, threads, die_size, die_size_source, source

            if name is not None:
                self.name.set_completed(name, min=name_min, max=name_max, source="fuzzy match")
            if manufacturer is not None:
                self.manufacturer.set_completed(manufacturer, min=manufacturer_min, max=manufacturer_max,
                                                source=f"Completed from name name based on {source}.")
            if family is not None:
                self.family.set_completed(family, min=family_min, max=family_max,
                                          source=f"Completed from name name based on {source}.")
            if model_range is not None:
                self.model_range.set_completed(model_range, min=model_range_min, max=model_range_max,
                                               source=f"Completed from name name based on {source}.")
            if tdp is not None:
                self.tdp.set_completed(tdp, min=tdp_min, max=tdp_max,
                                       source=f"Completed from name name based on {source}.")
            if cores is not None:
                self.core_units.set_completed(cores, min=cores_min, max=cores_max,
                                              source=f"Completed from name name based on {source}.")
            if threads is not None:
                self.threads.set_completed(threads, min=threads_min, max=threads_max,
                                           source=f"Completed from name name based on {source}.")
            if die_size is not None:
                self.die_size.set_completed(die_size, min=die_size_min, max=die_size_max,
                                            source=f"{die_size_source} : Completed from name name based on {source}.")
