from dataclasses import dataclass
from typing import Optional

import boaviztapi.utils.roundit as rd
from boaviztapi import config

WARNING_IMPORTANT_UNCERTAINTY = ("Uncertainty from technical characteristics is very important. Results should be interpreted with caution (see min and max values)")


@dataclass
class ImpactCriteria:
    name: str
    unit: str
    description: str
    method: Optional[str] = None


class Impact:
    def __init__(self, **kwargs):
        self.value = 0
        self.min = 0
        self.max = 0
        self.warnings = []

        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)

    def add_warning(self, warn):
        self.warnings.append(warn)

    def to_json(self):
        json = {"value": self.rounded_value()}
        if self.min or self.min == 0: json['min'] = self.rounded_min()
        if self.max or self.max == 0: json['max'] = self.rounded_max()
        if self.warnings: json['warnings'] = sorted(self.warnings)

        return json

    def rounded_value(self):
        rd_value = rd.round_based_on_min_max(self.value, self.min, self.max)
        nb_sig_fig = rd.significant_number(rd_value)

        if nb_sig_fig > config["max_sig_fig"]:
            return rd.round_to_sigfig(rd_value, config["max_sig_fig"])
        elif rd_value == 0:
            self.warnings.append(WARNING_IMPORTANT_UNCERTAINTY)
            return rd.round_to_sigfig(self.value, config["min_sig_fig"])
        else:
            return rd_value

    def rounded_min(self):
        return rd.round_to_sigfig(self.min, config["max_sig_fig"])

    def rounded_max(self):
        return rd.round_to_sigfig(self.max, config["max_sig_fig"])


GWP = ImpactCriteria(name="gwp", unit="kgCO2eq", description="Total climate change")
ADP = ImpactCriteria(name="adp", unit="kgSbeq", description="Use of minerals and fossil ressources")
PE = ImpactCriteria(name="pe", unit="MJ", description="Consumption of primary energy")
GWPPb = ImpactCriteria(name="gwppb", unit="kg CO2 eq.", method="PEF",
                       description="Climate change - Contribution of biogenic emissions")
GWPPf = ImpactCriteria(name="gwppf", unit="kg CO2 eq.", method="PEF",
                       description="Climate change - Contribution of fossil fuel emissions")
GWPPlu = ImpactCriteria(name="gwpplu", unit="kg CO2 eq.", method="PEF",
                        description="Climate change - Contribution of emissions from land use change")
IR = ImpactCriteria(name="ir", unit="kg U235 eq.", method="PEF", description="Emissions of radionizing substances")
LU = ImpactCriteria(name="lu", unit="No dimension", method="PEF", description="Land use")
ODP = ImpactCriteria(name="odp", unit="kg CFC-11 eq.", method="PEF", description="Depletion of the ozone layer")
PM = ImpactCriteria(name="pm", unit="Disease occurrence", method="PEF", description="Fine particle emissions")
POCP = ImpactCriteria(name="pocp", unit="kg NMVOC eq.", method="PEF", description="Photochemical ozone formation")
WU = ImpactCriteria(name="wu", unit="m3 eq.", method="PEF", description="Use of water resources")
MIPS = ImpactCriteria(name="mips", unit="kg", description="Material input per unit of service")
ADPe = ImpactCriteria(name="adpe", unit="kg SB eq.", method="PEF", description="Use of mineral and metal resources")
ADPf = ImpactCriteria(name="adpf", unit="MJ", method="PEF", description="Use of fossil resources (including nuclear)")
AP = ImpactCriteria(name="ap", unit="mol H+ eq.", method="PEF", description="Acidification")
CTUe = ImpactCriteria(name="ctue", unit="CTUe", method="PEF", description="Freshwater ecotoxicity")
CTUh_c = ImpactCriteria(name="ctuh_c", unit="CTUh", method="PEF", description="Human Toxicity - Carcinogenic Effects")
CTUh_nc = ImpactCriteria(name="ctuh_nc", unit="CTUh", method="PEF",
                         description="Human toxicity - non-carcinogenic effects")
Epf = ImpactCriteria(name="epf", unit="kg P eq.", method="PEF", description="Eutrophication of freshwater")
Epm = ImpactCriteria(name="epm", unit="kg N eq.", method="PEF", description="Eutrophication of marine waters")
Ept = ImpactCriteria(name="ept", unit="mol N eq.", method="PEF", description="Terrestrial eutrophication")
FW = ImpactCriteria(name="fw", unit="m3", method="", description="Net use of freshwater")

IMPACT_CRITERIAS = [GWP, ADP, PE, GWPPb, GWPPf, GWPPlu, IR, LU, ODP, PM, POCP, WU, MIPS, ADPe, ADPf, AP, CTUe, CTUh_c,
                    CTUh_nc, Epf, Epm, Ept, FW]

IMPACT_PHASES = ["embedded", "use"]


class ImpactFactor:
    def __init__(self, **kwargs):
        self.value = 0
        self.min = 0
        self.max = 0
        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)
