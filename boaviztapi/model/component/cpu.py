import os
from typing import Tuple

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi import config, data_dir
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.service.factor_provider import get_impact_factor
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf, fuzzymatch_attr_from_cpu_name

_cpu_specs = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/cpu_specs.csv'))
_family_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/cpu_manufacture.csv'))


def attributes_from_cpu_name(cpu_name: str):
    return fuzzymatch_attr_from_cpu_name(cpu_name, _cpu_specs)


class ComponentCPU(Component):
    NAME = "CPU"
    name_completion = False

    def __init__(self, archetype=get_component_archetype(config["default_cpu"], "cpu"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
        self.core_units = Boattribute(
            complete_function=self._complete_from_name,
            default=get_arch_value(archetype, 'core_units', 'default'),
            min=get_arch_value(archetype, 'core_units', 'min'),
            max=get_arch_value(archetype, 'core_units', 'max')
        )
        self.die_size_per_core = Boattribute(
            complete_function=self._complete_die_size_per_core,
            unit="cm2",
            default=get_arch_value(archetype, 'die_size_per_core', 'default'),
            min=get_arch_value(archetype, 'die_size_per_core', 'min'),
            max=get_arch_value(archetype, 'die_size_per_core', 'max')
        )
        self.die_size = Boattribute(
            complete_function=self._complete_from_name,
            unit="cm2",
            default=get_arch_value(archetype, 'die_size', 'default'),
            min=get_arch_value(archetype, 'die_size', 'min'),
            max=get_arch_value(archetype, 'die_size', 'max')
        )
        self.model_range = Boattribute(
            default=get_arch_value(archetype, 'model_range', 'default'),
            min=get_arch_value(archetype, 'model_range', 'min'),
            max=get_arch_value(archetype, 'model_range', 'max')
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
        self.usage.avg_power.add_warning("value for one cpu unit")

    # IMPACT COMPUTATION
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        core_impact, cpu_die_impact, cpu_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(core_impact.value, cpu_die_impact.value, cpu_impact.value)
        impact = self.__compute_impact_manufacture(core_impact, cpu_die_impact, cpu_impact)

        return impact.value, sign_figures, impact.min, impact.max, ["End of life is not included in the calculation"]

    def impact_use(self, impact_type: str, duration: float) -> ComputedImpacts:
        impact_factor = self.usage.elec_factors[impact_type]

        if not self.usage.avg_power.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.avg_power.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max
            )

        impact = ImpactFactor(
            value=impact_factor.value * (
                    self.usage.avg_power.value / 1000) * self.usage.use_time_ratio.value * duration,
            min=impact_factor.min * (
                    self.usage.avg_power.min / 1000) * self.usage.use_time_ratio.min * duration,
            max=impact_factor.max * (
                    self.usage.avg_power.max / 1000) * self.usage.use_time_ratio.max * duration
        )

        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impact.value, sig_fig, impact.min, impact.max, []

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.avg_power.value, self.usage.use_time_ratio.value, impact_factor)

    # TODO: compute min & max
    def model_power_consumption(self) -> ImpactFactor:
        self.usage.consumption_profile = CPUConsumptionProfileModel()

        self.usage.consumption_profile.compute_consumption_profile_model(cpu_manufacturer=self.manufacturer.value,
                                                                         cpu_model_range=self.model_range.value,
                                                                         cpu_tdp=self.tdp.value)
        if type(self.usage.time_workload.value) in (float, int):
            self.usage.avg_power.set_completed(self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.avg_power.set_completed(self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return ImpactFactor(
                value=rd.round_to_sigfig(self.usage.avg_power.value, 5),
                min=rd.round_to_sigfig(self.usage.avg_power.value, 5),
                max=rd.round_to_sigfig(self.usage.avg_power.value, 5)
        )

    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor, ImpactFactor]:
        core_impact = ImpactFactor(
            value=get_impact_factor(item='cpu', impact_type=impact_type)['constant_core_impact'],
            min=get_impact_factor(item='cpu', impact_type=impact_type)['constant_core_impact'],
            max=get_impact_factor(item='cpu', impact_type=impact_type)['constant_core_impact']
        )
        cpu_die_impact = ImpactFactor(
            value=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact'],
            min=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact'],
            max=get_impact_factor(item='cpu', impact_type=impact_type)['die_impact']
        )
        cpu_impact = ImpactFactor(
            value=get_impact_factor(item='cpu', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='cpu', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='cpu', impact_type=impact_type)['impact']
        )

        return core_impact, cpu_die_impact, cpu_impact

    def __compute_significant_numbers(self, core_impact: float, cpu_die_impact: float, cpu_impact: float) -> int:
        return rd.min_significant_figures(self.die_size_per_core.value, core_impact, cpu_die_impact, cpu_impact)

    def __compute_impact_manufacture(self, core_impact: ImpactFactor, cpu_die_impact: ImpactFactor, cpu_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(self.core_units.value * self.die_size_per_core.value + core_impact.value) * cpu_die_impact.value + cpu_impact.value,
            min=(self.core_units.min * self.die_size_per_core.min + core_impact.min) * cpu_die_impact.min + cpu_impact.min,
            max=(self.core_units.max * self.die_size_per_core.max + core_impact.max) * cpu_die_impact.max + cpu_impact.max
        )

    # COMPLETION
    def _complete_die_size_per_core(self):
        self._complete_from_name()
        corrected_family = None
        # If we can have a die_size and core_units, we can compute the die_size_per_core
        if self.die_size.has_value() and self.core_units.has_value():
            self.die_size_per_core.set_completed(value=float(self.die_size.value/self.core_units.value), source="die_size/core_units")
            return None

        sub = _family_df.copy()
        # If we don't have a family, we use the die_size_per_core from the archetype
        if self.die_size_per_core.has_value() and not self.family.has_value():
            return None

        if self.family.has_value():
            # Check if the family matches one of the families in the database and correct it if necessary
            corrected_family = fuzzymatch_attr_from_pdf(self.family.value, "family", sub)
            if corrected_family != self.family.value and corrected_family is not None:
                self.family.set_changed(corrected_family)

            tmp = sub[sub['family'] == corrected_family]

            if len(tmp) > 0:
                sub = tmp.copy()

            if self.core_units.has_value() and corrected_family is not None:
                # Find the closest line to the number of cores provided by the user
                sub['core_dif'] = sub[['core_units']].apply(lambda x: abs(x[0] - self.core_units.value), axis=1)
                sub = sub.sort_values(by='core_dif', ascending=True)
                row = sub.iloc[0]

                # If we have only one row but the number of cores is different, we use the max and min values of the dataframe
                if row['core_dif'] != 0 and len(sub) == 1:
                    self.die_size_per_core.set_completed(float(row['die_size_per_core']), source=row['Source'])
                    self.die_size_per_core.min = float(float(_family_df['die_size_per_core'].min()))
                    self.die_size_per_core.max = float(float(_family_df['die_size_per_core'].max()))
                    return

                row2 = sub.iloc[1]
                self.die_size_per_core.set_completed(float(row['die_size_per_core']), source=row['Source'])

                if row['core_dif'] == 0:
                    self.die_size_per_core.min = float(row['die_size_per_core'])
                    self.die_size_per_core.max = float(row['die_size_per_core'])

                elif float(row2['die_size_per_core']) > float(row['die_size_per_core']):
                    self.die_size_per_core.min = float(row['die_size_per_core'])
                    self.die_size_per_core.max = float(row2['die_size_per_core'])

                else:
                    self.die_size_per_core.min = float(row2['die_size_per_core'])
                    self.die_size_per_core.max = float(row['die_size_per_core'])

                return

        source_family = self.family.value if corrected_family is not None else "all families"

        # If we don't have a number of cores, we use the average die size per core for a given family (if provided)
        self.die_size_per_core.set_completed(float(sub['die_size_per_core'].mean()), source=f"Average for {source_family}")
        self.die_size_per_core.min = float(float(sub['die_size_per_core'].min()))
        self.die_size_per_core.max = float(float(sub['die_size_per_core'].max()))

    def _complete_from_name(self):
        if self.name.has_value() and not self.name_completion:
            compute_min_max = False
            if self.name.min != self.name.value or self.name.max != self.name.value:
                compute_min_max = True

            name, manufacturer, family, model_range, tdp, cores, die_size, die_size_source, source  = attributes_from_cpu_name(self.name.value)

            if compute_min_max:
                name_min, manufacturer_min, family_min, model_range_min, tdp_min, cores_min, die_size_min, die_size_source_min, source_min  = attributes_from_cpu_name(self.name.min)
                name_max, manufacturer_max, family_max, model_range_max, tdp_max, cores_max, die_size_max, die_size_source_max, source_max  = attributes_from_cpu_name(self.name.max)
            else:
                name_min, manufacturer_min, family_min, model_range_min, tdp_min, cores_min, die_size_min, die_size_source_min, source_min  = name, manufacturer, family, model_range, tdp, cores, die_size, die_size_source, source
                name_max, manufacturer_max, family_max, model_range_max, tdp_max, cores_max, die_size_max, die_size_source_max, source_max  = name, manufacturer, family, model_range, tdp, cores, die_size, die_size_source, source

            if name is not None:
                self.name.set_completed(name, min=name_min, max=name_max, source="fuzzy match")
            if manufacturer is not None:
                self.manufacturer.set_completed(manufacturer, min=manufacturer_min, max=manufacturer_max, source=f"Completed from name name based on {source}.")
            if family is not None:
                self.family.set_completed(family, min=family_min, max=family_max, source=f"Completed from name name based on {source}.")
            if model_range is not None:
                self.model_range.set_completed(model_range, min=model_range_min, max=model_range_max, source=f"Completed from name name based on {source}.")
            if tdp is not None:
                self.tdp.set_completed(tdp, min=tdp_min, max=tdp_max, source=f"Completed from name name based on {source}.")
            if cores is not None:
                self.core_units.set_completed(cores, min=cores_min, max=cores_max, source=f"Completed from name name based on {source}.")
            if die_size is not None:
                # divide by 100 to convert mm2 into cm2
                self.die_size.set_completed(die_size/100, min=die_size_min/100, max=die_size_max/100, source=f"{die_size_source} : Completed from name name based on {source}.")
            self.name_completion = True
