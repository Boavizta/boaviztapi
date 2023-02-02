from dataclasses import dataclass
from typing import Tuple

import boaviztapi.utils.roundit as rd

@dataclass
class ImpactCriteria:
    name: str
    unit: str
    description: str
class Impact:
    def __init__(self, **kwargs):
        self.value = 0
        self.significant_figures = 1
        self.min = 0
        self.max = 0
        self.warnings = []

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)
    def add_warning(self, warn):
        self.warnings.append(warn)
    def to_json(self):
        json = {"value": rd.round_to_sigfig(self.value, self.significant_figures), "significant_figures": self.significant_figures}
        if self.min: json['min'] = rd.round_to_sigfig(self.min, self.significant_figures)
        if self.max: json['max'] = rd.round_to_sigfig(self.max, self.significant_figures)
        if self.warnings: json['warnings'] = self.warnings

        return json
    def rounded_value(self):
        return rd.round_to_sigfig(self.value, self.significant_figures)


GWP = ImpactCriteria(name="gwp", unit="kgCO2eq", description="Effects on global warming")
ADP = ImpactCriteria(name="adp", unit="kgSbeq", description="Use of minerals and fossil ressources")
PE = ImpactCriteria(name="pe", unit="MJ", description="Consumption of primary energy")

IMPACT_CRITERIAS = [GWP, ADP, PE]
IMPACT_PHASES = ["manufacture", "use"]

class ImpactFactor:
    def __init__(self, **kwargs):
        self.value = 0
        self.min = 0
        self.max = 0
        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)
