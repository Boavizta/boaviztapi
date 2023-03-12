import os
from typing import Tuple

import pandas as pd

import boaviztapi.utils.roundit as rd
from boaviztapi import config
from boaviztapi.model.boattribute import Boattribute
from boaviztapi.model.component.component import Component, ComputedImpacts
from boaviztapi.model.impact import ImpactFactor
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf


class ComponentSSD(Component):
    _ssd_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/crowdsourcing/ssd_manufacture.csv'))

    NAME = "SSD"

    __DISK_TYPE = 'ssd'

    DEFAULT_SSD_CAPACITY = 1000
    DEFAULT_SSD_DENSITY = 48.5

    IMPACT_FACTOR = {
        'gwp': {
            'die_impact': 2.20,
            'impact': 6.34
        },
        'pe': {
            'die_impact': 27.30,
            'impact': 76.90
        },
        'adp': {
            'die_impact': 6.30E-05,
            'impact': 5.63E-04
        }
    }

    def __init__(self, default_config=config["DEFAULT"]["SSD"], **kwargs):
        super().__init__(default_config=default_config, **kwargs)

        self.manufacturer = Boattribute(
            unit="none",
            default=default_config['manufacturer']['default'],
        )
        self.capacity = Boattribute(
            unit="GB",
            default=default_config['capacity']['default'],
            min=default_config['capacity']['min'],
            max=default_config['capacity']['max']
        )
        self.density = Boattribute(
            unit="GB/cm2",
            complete_function=self._complete_from_crowdsourcing,
            default=default_config['density']['default'],
            min=default_config['density']['min'],
            max=default_config['density']['max']
        )

    # IMPACT CALCUATION
    def impact_manufacture_gwp(self) -> ComputedImpacts:
        return self.__impact_manufacture('gwp')

    def __impact_manufacture(self, impact_type: str) -> ComputedImpacts:
        ssd_die_impact, ssd_impact = self.__get_impact_constants(impact_type)
        sign_figures = self.__compute_significant_numbers(ssd_die_impact.value, ssd_impact.value)
        impact = self.__compute_impact_manufacture(ssd_die_impact, ssd_impact)
        return impact.value, sign_figures, impact.min, impact.max, []

    def __get_impact_constants(self, impact_type: str) -> Tuple[ImpactFactor, ImpactFactor]:
        ssd_die_impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['die_impact'],
            min=self.IMPACT_FACTOR[impact_type]['die_impact'],
            max=self.IMPACT_FACTOR[impact_type]['die_impact']
        )
        ssd_impact = ImpactFactor(
            value=self.IMPACT_FACTOR[impact_type]['impact'],
            min=self.IMPACT_FACTOR[impact_type]['impact'],
            max=self.IMPACT_FACTOR[impact_type]['impact']
        )
        return ssd_die_impact, ssd_impact

    def __compute_significant_numbers(self, ssd_die_impact: float, ssd_impact: float) -> int:
        return rd.min_significant_figures(self.density.value, ssd_die_impact, ssd_impact)

    def __compute_impact_manufacture(self, ssd_die_impact: ImpactFactor, ssd_impact: ImpactFactor) -> ImpactFactor:
        return ImpactFactor(
            value=(self.capacity.value / self.density.value) * ssd_die_impact.value + ssd_impact.value,
            min=(self.capacity.min / self.density.min) * ssd_die_impact.min + ssd_impact.min,
            max=(self.capacity.max / self.density.max) * ssd_die_impact.max + ssd_impact.max
        )
    def impact_manufacture_pe(self) -> ComputedImpacts:
        return self.__impact_manufacture('pe')

    def impact_manufacture_adp(self) -> ComputedImpacts:
        return self.__impact_manufacture('adp')

    # COMPLETION
    def _complete_from_crowdsourcing(self):
        if self.density.is_none():
            sub = self._ssd_df
            if self.manufacturer.is_set():
                corrected_manufacturer = fuzzymatch_attr_from_pdf(self.manufacturer.value, "manufacturer", sub)
                sub = sub[sub['manufacturer'] == corrected_manufacturer]
                if corrected_manufacturer != self.manufacturer.value:
                    self.manufacturer.set_changed(corrected_manufacturer)

            if len(sub) == 0 or len(sub) == len(self._ssd_df):
                pass
            elif len(sub) == 1:
                self.density.set_completed(float(sub['density']), source=str(sub['manufacturer'].iloc[0]),
                                                         min=float(sub['density']), max=float(sub['density']))
            else:
                self.density.set_completed(
                    float(sub['density'].mean()),
                    source="Average of " + str(len(sub)) + " rows",
                    min=float(sub['density'].min()),
                    max=float(sub['density'].max())
                )