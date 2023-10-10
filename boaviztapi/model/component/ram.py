import os
from typing import Tuple

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.consumption_profile.consumption_profile import RAMConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_arch_value, get_component_archetype
from boaviztapi.service.factor_provider import get_impact_factor
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
        self.usage.avg_power.add_warning("value for one ram strip")

    # IMPACT COMPUTATION
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        ram_die_impact, ram_impact = self.__get_impact_constants(impact_type)

        impact = self.__compute_impact_manufacture(ram_die_impact, ram_impact)

        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        impact_factor = self.usage.elec_factors[impact_type]

        if not self.usage.avg_power.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.avg_power.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max,
            )

        impact = ImpactFactor(
            value=impact_factor.value * (
                    self.usage.avg_power.value / 1000) * self.usage.use_time_ratio.value * duration,
            min=impact_factor.min * (
                    self.usage.avg_power.min / 1000) * self.usage.use_time_ratio.min * duration,
            max=impact_factor.max * (
                    self.usage.avg_power.max / 1000) * self.usage.use_time_ratio.max * duration
        )

        return impact.value, impact.min, impact.max, []

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
            value=rd.round_to_sigfig(self.usage.avg_power.value, 5),
            min=rd.round_to_sigfig(self.usage.avg_power.value, 5),
            max=rd.round_to_sigfig(self.usage.avg_power.value, 5)
        )

    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        ram_die_impact = ImpactFactor(
            value=get_impact_factor(item='ram', impact_type=impact_type)['die_impact'],
            min=get_impact_factor(item='ram', impact_type=impact_type)['die_impact'],
            max=get_impact_factor(item='ram', impact_type=impact_type)['die_impact']
        )
        ram_impact = ImpactFactor(
            value=get_impact_factor(item='ram', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='ram', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='ram', impact_type=impact_type)['impact']
        )
        return ram_die_impact, ram_impact

    def __compute_impact_manufacture(self, ram_die_impact: ImpactFactor, ram_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(self.capacity.value / self.density.value) * ram_die_impact.value + ram_impact.value,
            min=(self.capacity.min / self.density.max) * ram_die_impact.min + ram_impact.min,
            max=(self.capacity.max / self.density.min) * ram_die_impact.max + ram_impact.max
        )

    # COMPLETION
    def _complete_density(self):
        sub = self._ram_df

        if self.manufacturer.has_value():
            corrected_manufacturer = fuzzymatch_attr_from_pdf(self.manufacturer.value, "manufacturer", sub)
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
