import os

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.consumption_profile.consumption_profile import RAMConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_arch_value, get_component_archetype
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf


class ComponentRAM(Component):
    NAME = "RAM"

    _ram_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/ram_manufacture.csv'))

    def __init__(self, archetype=get_component_archetype(config["default_ram"], "ram"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)

        self.process = Boattribute(
            default=get_arch_value(archetype, 'process', 'default'),
            min=get_arch_value(archetype, 'process', 'min'),
            max=get_arch_value(archetype, 'process', 'max')
        )
        self.manufacturer = Boattribute(
            default=get_arch_value(archetype, 'manufacturer', 'default'),
            min=get_arch_value(archetype, 'manufacturer', 'min'),
            max=get_arch_value(archetype, 'manufacturer', 'max')
        )
        self.capacity = Boattribute(
            unit="GB",
            default=get_arch_value(archetype, 'capacity', 'default'),
            min=get_arch_value(archetype, 'capacity', 'min'),
            max=get_arch_value(archetype, 'capacity', 'max')
        )
        self.density = Boattribute(
            complete_function=self._complete_density,
            unit="GB/cm2",
            default=get_arch_value(archetype, 'density', 'default'),
            min=get_arch_value(archetype, 'density', 'min'),
            max=get_arch_value(archetype, 'density', 'max')
        )

    # IMPACT COMPUTATION

    def model_power_consumption(self, ) -> ImpactFactor:
        self.usage.consumption_profile = RAMConsumptionProfileModel()
        self.usage.consumption_profile.compute_consumption_profile_model(ram_capacity=self.capacity.value)

        if type(self.usage.time_workload.value) in (float, int):
            self.usage.avg_power.set_completed(
                self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.avg_power.set_completed(
                self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return ImpactFactor(
            value=rd.round_to_sigfig(self.usage.avg_power.value, 5)*self.units.value,
            min=rd.round_to_sigfig(self.usage.avg_power.value, 5)*self.units.min,
            max=rd.round_to_sigfig(self.usage.avg_power.value, 5)*self.units.max
        )

    # COMPLETION
    def _complete_density(self):
        sub = self._ram_df

        if self.manufacturer.has_value():
            corrected_manufacturer = fuzzymatch_attr_from_pdf(self.manufacturer.value, "manufacturer", sub)
            if corrected_manufacturer is not None:
                sub = sub[sub['manufacturer'] == corrected_manufacturer]
                if corrected_manufacturer != self.manufacturer.value:
                    self.manufacturer.set_changed(corrected_manufacturer)

        if self.process.has_value():
            sub = sub[sub['process'] == self.process.value]

        if len(sub) == 1:
            self.density.set_completed(
                float(sub['density']),
                source=str(sub['manufacturer'].iloc[0]),
                min=float(sub['density']),
                max=float(sub['density'])
            )

        elif (len(sub) == 0 or len(sub) == len(self._ram_df)) and self.density.has_value():
            return

        else:
            self.density.set_completed(
                float(sub['density'].mean()),
                source="Average of " + str(len(sub)) + " rows",
                min=float(sub['density'].min()),
                max=float(sub['density'].max())
            )
