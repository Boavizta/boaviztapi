from dataclasses import dataclass
from typing import Optional

import boaviztapi.utils.roundit as rd
from boaviztapi import config

WARNING_IMPORTANT_UNCERTAINTY = ("Uncertainty from technical characteristics is very important. Results should be interpreted with caution (see min and max values)")
NOT_IMPLEMENTED = 'not implemented'


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
        if warn not in self.warnings:
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
            self.add_warning(WARNING_IMPORTANT_UNCERTAINTY)
            return rd.round_to_sigfig(self.value, config["min_sig_fig"])
        else:
            return rd_value

    def rounded_min(self):
        return rd.round_to_sigfig(self.min, config["max_sig_fig"])

    def rounded_max(self):
        return rd.round_to_sigfig(self.max, config["max_sig_fig"])

    def allocate(self, duration, life_time):
        if duration > life_time.value:
            allocation_ratio, allocation_ratio_min, allocation_ratio_max = 1, 1, 1
        else:
            allocation_ratio = duration / life_time.value
            allocation_ratio_min = duration / life_time.max
            allocation_ratio_max = duration / life_time.min

        self.value = self.value * allocation_ratio
        self.min = self.min * allocation_ratio_min
        self.max = self.max * allocation_ratio_max



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
MIPS = ImpactCriteria(name="mips", unit="kg", description="Material input per unit of services")
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

IMPACT_CRITERIAS = {"gwp": GWP, "adp": ADP, "pe": PE, "gwppb": GWPPb, "gwppf": GWPPf, "gwpplu": GWPPlu, "ir": IR,
                    "lu": LU, "odp": ODP, "pm": PM, "pocp": POCP, "wu": WU, "mips": MIPS, "adpe": ADPe, "adpf": ADPf,
                    "ap": AP, "ctue": CTUe, "CTUh_c": CTUh_c, "CTUh_nc": CTUh_nc, "epf": Epf, "epm": Epm, "ept": Ept,
                    "fw": FW}

EMBEDDED = "embedded"
USE = "use"

IMPACT_PHASES = [EMBEDDED, USE]


class ImpactFactor:
    def __init__(self, **kwargs):
        self.value = 0
        self.min = 0
        self.max = 0
        for attr, val in kwargs.items():
            if val is not None:
                self.__setattr__(attr, val)


class Assessable:
    def __init__(self, **kwargs):
        self._impacts = {}

    def get_impacts(self, selected_criteria):
        result = {}
        for criteria in selected_criteria:
            result[criteria] = {}
            result[criteria]["unit"] = IMPACT_CRITERIAS[criteria].unit
            result[criteria]["description"] = IMPACT_CRITERIAS[criteria].description
            for phase in IMPACT_PHASES:
                if criteria not in self._impacts or phase not in self._impacts[criteria] or self._impacts[criteria][phase] is None:
                    result[criteria][phase] = NOT_IMPLEMENTED
                else:
                    result[criteria][phase] = self._impacts[criteria][phase].to_json()
        return result
    @property
    def impacts(self):
        return self._impacts

    @impacts.setter
    def impacts(self, impacts):
        self._impacts = impacts

    def add_impacts(self, impact, criteria, phase):
        if criteria not in self._impacts:
            self._impacts[criteria] = {}
            self._impacts[criteria]["unit"] = IMPACT_CRITERIAS[criteria].unit
            self._impacts[criteria]["description"] = IMPACT_CRITERIAS[criteria].description
        if phase not in self._impacts[criteria]:
            self._impacts[criteria][phase] = {}
        self._impacts[criteria][phase] = impact


