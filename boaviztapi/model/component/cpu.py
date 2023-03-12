import os
from typing import Tuple, Optional

import numpy as np
import pandas as pd
from rapidfuzz import process, fuzz

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model import ComputedImpacts
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf

def parse(cpu_name: str) -> Tuple[str, str]:
    vendor_list = ["intel", "amd", "arm"]  # every string in lowercase
    for vendor in vendor_list:
        if vendor in cpu_name:
            cpu_name.replace(vendor, '')
            return vendor, cpu_name.replace(vendor, '')
    return None, cpu_name


def fuzzymatch(cpu_name_to_match: str, cpu_name_list: list) -> Optional[Tuple[str, float, int]]:
    foo = process.extractOne(cpu_name_to_match, cpu_name_list, scorer=fuzz.WRatio)
    if foo is not None:
        return foo if foo[1] > 88.0 else None


class ComponentCPU(Component):
    NAME = "CPU"
    _cpu_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/crowdsourcing/cpu_manufacture.csv'))
    _cpu_index = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/crowdsourcing/cpu_index.csv'))

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

    def __init__(self, default_config=config["DEFAULT"]["CPU"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)
        self.core_units = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            default=default_config['core_units']['default'],
            min=default_config['core_units']['min'],
            max=default_config['core_units']['max']
        )
        self.die_size_per_core = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            unit="mm2",
            default=default_config['die_size_per_core']['default'],
            min=default_config['die_size_per_core']['min'],
            max=default_config['die_size_per_core']['max']
        )
        self.model_range = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            default=default_config['model_range']['default'],
        )
        self.manufacturer = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            default=default_config['manufacturer']['default'],
        )
        self.family = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            default=default_config['manufacturer']['default'],
        )
        self.name = Boattribute(
            default="intel xeon gold 6134",
        )
        self.tdp = Boattribute(
            complete_function=self._complete_from_crowdsourcing,
            unit="W",
            default=default_config['tdp']['default'],
            min=default_config['tdp']['min'],
            max=default_config['tdp']['max']
        )
        self.usage.hours_electrical_consumption.add_warning("value for one cpu unit")

    # IMPACT COMPUTATION
    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        core_impact, cpu_die_impact, cpu_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(core_impact.value, cpu_die_impact.value, cpu_impact.value)
        impact = self.__compute_impact_manufacture(core_impact, cpu_die_impact, cpu_impact)

        return impact.value, sign_figures, impact.min, impact.max, []

    def __impact_usage(self, impact_type: str) -> ComputedImpacts:
        impact_factor = getattr(self.usage, f'{impact_type}_factor')

        if not self.usage.hours_electrical_consumption.is_set():
            modeled_consumption = self.model_power_consumption()
            self.usage.hours_electrical_consumption.set_completed(
                modeled_consumption.value,
                min=modeled_consumption.min,
                max=modeled_consumption.max
            )

        impact = ImpactFactor(
            value=impact_factor.value * (
                self.usage.hours_electrical_consumption.value / 1000) * self.usage.use_time.value,
            min=impact_factor.min * (
                self.usage.hours_electrical_consumption.min / 1000) * self.usage.use_time.min,
            max=impact_factor.max * (
                self.usage.hours_electrical_consumption.max / 1000) * self.usage.use_time.max
        )

        sig_fig = self.__compute_significant_numbers_usage(impact_factor.value)
        return impact.value, sig_fig, impact.min, impact.max, []

    def __compute_significant_numbers_usage(self, impact_factor: float) -> int:
        return rd.min_significant_figures(self.usage.hours_electrical_consumption.value, self.usage.use_time.value,
                                          impact_factor)

    # TODO: compute min & max
    def model_power_consumption(self) -> ImpactFactor:
        self.usage.consumption_profile = CPUConsumptionProfileModel()

        manuf, model, tdp = None, None, None
        if self.manufacturer.is_set(): manuf = self.manufacturer.value
        if self.model_range.is_set(): model = self.model_range.value
        if self.tdp.is_set(): tdp = self.tdp.value

        self.usage.consumption_profile.compute_consumption_profile_model(cpu_manufacturer=manuf,
                                                                         cpu_model_range=model,
                                                                         cpu_tdp=tdp)
        if type(self.usage.time_workload.value) in (float, int):
            self.usage.hours_electrical_consumption.set_completed(self.usage.consumption_profile.apply_consumption_profile(self.usage.time_workload.value))
        else:
            self.usage.hours_electrical_consumption.set_completed(self.usage.consumption_profile.apply_multiple_workloads(self.usage.time_workload.value))

        return ImpactFactor(
                value=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5),
                min=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5),
                max=rd.round_to_sigfig(self.usage.hours_electrical_consumption.value, 5)
        )

    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor, ImpactFactor]:
        core_impact = ImpactFactor(
            value=self.IMPACT_FACTOR['constant_core_impact'],
            min=self.IMPACT_FACTOR['constant_core_impact'],
            max=self.IMPACT_FACTOR['constant_core_impact']
        )
        cpu_die_impact =  ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['die_impact'],
            min=self.IMPACT_FACTOR[impact_type]['die_impact'],
            max=self.IMPACT_FACTOR[impact_type]['die_impact']
        )
        cpu_impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['impact'],
            min=self.IMPACT_FACTOR[impact_type]['impact'],
            max=self.IMPACT_FACTOR[impact_type]['impact']
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

    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    def impact_use_gwp(self) -> ComputedImpacts:
        return self.__impact_usage("gwp")

    def impact_use_pe(self) -> ComputedImpacts:
        return self.__impact_usage("pe")

    def impact_use_adp(self) -> ComputedImpacts:
        return self.__impact_usage("adp")

    # COMPLETION
    def _complete_from_crowdsourcing(self):
        self._complete_from_name()
        sub = self._cpu_df
        if self.family.is_set():
            corrected_family = fuzzymatch_attr_from_pdf(self.family.value, "family", sub)
            if corrected_family != self.family.value:
                self.family.set_changed(corrected_family)
            tmp = sub[sub['family'] == corrected_family]
            if len(tmp) > 0:
                sub = tmp.copy()

        if len(sub) == 0 or len(sub) == len(self._cpu_df):
            pass

        elif len(sub) == 1:
            row = sub.iloc[0]
            self.die_size_per_core.set_completed(float(row['die_size_per_core']), source=row['Source'])

        elif self.core_units.is_set():
            # Find the closest line to the number of cores provided by the user
            sub['core_dif'] = sub[['core_units']].apply(lambda x: abs(x[0] - self.core_units.value), axis=1)
            sub = sub.sort_values(by='core_dif', ascending=True)
            row = sub.iloc[0]
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
        else:
            self.die_size_per_core.set_completed(float(sub['die_size_per_core'].mean()), source=f"Average for the {self.family.value} family")
            self.die_size_per_core.min = float(float(sub['die_size_per_core'].min()))
            self.die_size_per_core.max = float(float(sub['die_size_per_core'].max()))

    def _complete_from_name(self):
        if self.name.is_set():
            manufacturer, model_range, family, tdp = self._attributes_from_cpu_name(self.name.value)
            if manufacturer is not None:
                self.manufacturer.set_completed(manufacturer, source="from name")
            if model_range is not None:
                self.model_range.set_completed(model_range, source="from name")
            if family is not None:
                self.family.set_completed(family, source="from name")
            if tdp is not None:
                self.tdp.set_completed(tdp, source="from name")

    def _attributes_from_cpu_name(self, cpu_name: str) -> [str, str, str, int]:
        cpu_name = cpu_name.lower()
        manufacturer, cpu_sub_name = parse(cpu_name)
        sub = self._cpu_index
        if manufacturer is None:
            name_list = list(sub.sub_model_name.unique())
        else:
            name_list = list(sub[sub['manufacturer'] == manufacturer].sub_model_name.unique())
        result = fuzzymatch(cpu_sub_name, name_list)

        if result is not None:
            model_range = sub[sub['sub_model_name'] == result[0]].iloc[0].model_range
            family = sub[sub['sub_model_name'] == result[0]].iloc[0].family
            tdp = sub[sub['sub_model_name'] == result[0]].iloc[0].tdp
            if np.isnan(tdp):
                tdp = None

        else:
            model_range = None
            family = None
            tdp = None

        return manufacturer, model_range, family, tdp


