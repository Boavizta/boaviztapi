import os
from typing import Tuple

import pandas as pd

from boaviztapi import config, data_dir
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.service.archetype import get_component_archetype, get_arch_value
from boaviztapi.service.factor_provider import get_impact_factor
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf


class ComponentSSD(Component):
    _ssd_df = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/ssd_manufacture.csv'))

    NAME = "SSD"

    __DISK_TYPE = 'ssd'

    DEFAULT_SSD_CAPACITY = 1000
    DEFAULT_SSD_DENSITY = 48.5

    def __init__(self, archetype=get_component_archetype(config["default_ssd"], "ssd"), **kwargs):
        super().__init__(archetype=archetype, **kwargs)
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
            unit="GB/cm2",
            complete_function=self._complete_density,
            default=get_arch_value(archetype, 'density', 'default'),
            min=get_arch_value(archetype, 'density', 'min'),
            max=get_arch_value(archetype, 'density', 'max')
        )
        self.layers = Boattribute(
            default=get_arch_value(archetype, 'layers', 'default'),
            min=get_arch_value(archetype, 'layers', 'min'),
            max=get_arch_value(archetype, 'layers', 'max')
        )

    # IMPACT CALCUATION
    def impact_embedded(self, impact_type: str) -> ComputedImpacts:
        ssd_die_impact, ssd_impact = self.__get_impact_constants(impact_type)
        impact = self.__compute_impact_manufacture(ssd_die_impact, ssd_impact)
        return impact.value, impact.min, impact.max, ["End of life is not included in the calculation"]


    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        ssd_die_impact = ImpactFactor(
            value=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact'],
            min=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact'],
            max=get_impact_factor(item='ssd', impact_type=impact_type)['die_impact']
        )
        ssd_impact = ImpactFactor(
            value=get_impact_factor(item='ssd', impact_type=impact_type)['impact'],
            min=get_impact_factor(item='ssd', impact_type=impact_type)['impact'],
            max=get_impact_factor(item='ssd', impact_type=impact_type)['impact']
        )
        return ssd_die_impact, ssd_impact

    def __compute_impact_manufacture(self, ssd_die_impact: ImpactFactor, ssd_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(self.capacity.value / self.density.value) * ssd_die_impact.value + ssd_impact.value,
            min=(self.capacity.min / self.density.max) * ssd_die_impact.min + ssd_impact.min,
            max=(self.capacity.max / self.density.min) * ssd_die_impact.max + ssd_impact.max
        )

    # COMPLETION
    def _complete_density(self):
        sub = self._ssd_df
        if self.manufacturer.has_value():
            corrected_manufacturer = fuzzymatch_attr_from_pdf(self.manufacturer.value, "manufacturer", sub)
            sub = sub[sub['manufacturer'] == corrected_manufacturer]
            if corrected_manufacturer != self.manufacturer.value:
                self.manufacturer.set_changed(corrected_manufacturer)

        if self.layers.has_value():
            sub = sub[sub['layers'] == self.layers.value]

        if len(sub) == 1:
            self.density.set_completed(float(sub['density']), source=str(sub['source'].iloc[0]),
                                                         min=float(sub['density']), max=float(sub['density']))

        elif (len(sub) == 0 or len(sub) == len(self._ssd_df)) and self.density.has_value():
            return

        else:
            self.density.set_completed(
                float(sub['density'].mean()),
                source="Average of " + str(len(sub)) + " rows",
                min=float(sub['density'].min()),
                max=float(sub['density'].max())
            )