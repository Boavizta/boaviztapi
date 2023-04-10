from dataclasses import dataclass
from typing import Optional

import boaviztapi.utils.roundit as rd

@dataclass
class ImpactCriteria:
    name: str
    unit: str
    description: str
    method: Optional[str] = None
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
        if self.min or self.min==0: json['min'] = rd.round_to_sigfig(self.min, self.significant_figures)
        if self.max or self.max==0: json['max'] = rd.round_to_sigfig(self.max, self.significant_figures)
        if self.warnings: json['warnings'] = self.warnings

        return json
    def rounded_value(self):
        return rd.round_to_sigfig(self.value, self.significant_figures)


GWP = ImpactCriteria(name="gwp", unit="kgCO2eq", description="Effects on global warming")
ADP = ImpactCriteria(name="adp", unit="kgSbeq", description="Use of minerals and fossil ressources")
PE = ImpactCriteria(name="pe", unit="MJ", description="Consumption of primary energy")
GWPPb = ImpactCriteria(name="gwppb", unit="kg CO2 eq.", method="PEF", description="")
GWPPf = ImpactCriteria(name="gwppf", unit="kg CO2 eq.", method="PEF", description="")
GWPPlu = ImpactCriteria(name="gwpplu", unit="kg CO2 eq.", method="PEF", description="")
IR = ImpactCriteria(name="ir", unit="kg U235 eq.", method="PEF", description="")
LU = ImpactCriteria(name="lu", unit="No dimension", method="PEF", description="")
ODP = ImpactCriteria(name="odp", unit="kg CFC-11 eq.", method="PEF", description="")
PM = ImpactCriteria(name="pm", unit="Disease occurrence", method="PEF", description="")
POCP = ImpactCriteria(name="pocp", unit="kg NMVOC eq.", method="PEF", description="")
WU = ImpactCriteria(name="wu", unit="m3 eq.", method="PEF", description="")
MIPS = ImpactCriteria(name="mips", unit="kg", description="")
ADPe = ImpactCriteria(name="adpe", unit="kg SB eq.", method="PEF", description="")
ADPf = ImpactCriteria(name="adpf", unit="MJ", method="PEF", description="")
AP = ImpactCriteria(name="ap", unit="mol H+ eq.", method="PEF", description="")
CTUe = ImpactCriteria(name="ctue", unit="CTUe", method="PEF", description="")
CTUh_c = ImpactCriteria(name="ctuh_c", unit="CTUh", method="PEF", description="")
CTUh_nc = ImpactCriteria(name="ctuh_nc", unit="CTUh", method="PEF", description="")
Epf = ImpactCriteria(name="epf", unit="kg P eq.", method="PEF", description="")
Epm = ImpactCriteria(name="epm", unit="kg N eq.", method="PEF", description="")
Ept = ImpactCriteria(name="ept", unit="mol N eq.", method="PEF", description="")

IMPACT_CRITERIAS = [GWP, ADP, PE, GWPPb, GWPPf, GWPPlu, IR, LU, ODP, PM, POCP, WU, MIPS, ADPe, ADPf, AP, CTUe, CTUh_c, CTUh_nc, Epf, Epm, Ept]
IMPACT_PHASES = ["other", "use"]

class ImpactFactor:
    def __init__(self, **kwargs):
        self.value = 0
        self.min = 0
        self.max = 0
        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)