import hashlib
import os
from abc import abstractmethod
from typing import Optional
import boaviztapi.utils.roundit as rd
import pandas as pd
from pydantic import BaseModel

from boaviztapi.model.components import data_dir
from boaviztapi.model.usage.usage import Usage, UsageCPU

_cpu_df = pd.read_csv(os.path.join(data_dir, 'components/cpu_manufacture.csv'))
_ram_df = pd.read_csv(os.path.join(data_dir, 'components/ram_manufacture.csv'))
_ssd_df = pd.read_csv(os.path.join(data_dir, 'components/ssd_manufacture.csv'))
_cpu_df['manufacture_date'] = _cpu_df['manufacture_date'].astype(str)  # Convert date column to string


class Component(BaseModel):
    hash: str = None
    TYPE: str = None
    _IMPACT_FACTOR_DICT: dict = None
    usage: Usage = None

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __hash__(self):
        object_fingerprint = bytes(((type(self),) + tuple(self.__dict__.values())).__str__(), encoding='utf8')
        return hashlib.sha256(object_fingerprint).hexdigest()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hash = self.__hash__()

    def get_impacts_factors(self) -> dict:
        return self._IMPACT_FACTOR_DICT

    @abstractmethod
    def impact_manufacture_gwp(self) -> (float, int):
        pass

    @abstractmethod
    def impact_manufacture_pe(self) -> (float, int):
        pass

    @abstractmethod
    def impact_manufacture_adp(self) -> (float, int):
        pass

    @abstractmethod
    def impact_use_gwp(self, model=None) -> (float, int):
        return self.usage.get_hours_electrical_consumption(
            model) * self.usage.get_duration_hours() * self.usage.get_gwp_factor(), rd.DEFAULT_SIG_FIGURES

    @abstractmethod
    def impact_use_pe(self, model=None) -> (float, int):
        return self.usage.get_hours_electrical_consumption(
            model) * self.usage.get_duration_hours() * self.usage.get_pe_factor(), rd.DEFAULT_SIG_FIGURES

    @abstractmethod
    def impact_use_adp(self, model=None) -> (float, int):
        return self.usage.get_hours_electrical_consumption(
            model) * self.usage.get_duration_hours() * self.usage.get_adp_factor(), rd.DEFAULT_SIG_FIGURES


class ComponentCPU(Component):
    TYPE = "CPU"

    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "die_impact": 1.97,
            "impact": 9.14
        },
        "pe": {
            "die_impact": 26.50,
            "impact": 156.00
        },
        "adp": {
            "die_impact": 5.80E-07,
            "impact": 2.04E-02
        },
        "constant_core_impact": 0.491
    }

    _DEFAULT_CPU_DIE_SIZE_PER_CORE = 0.245
    _DEFAULT_CPU_CORE_UNITS = 24
    _DEFAULT_CPU_FAMILY = "skylake"
    _DEFAULT_MODEL_FAMILY = "xeon platinium"

    usage: UsageCPU = None

    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model_name: Optional[str] = None
    model_id: Optional[str] = None
    family: Optional[str] = None
    name: Optional[str] = None

    def get_core_units(self):
        if not self.core_units:
            self.core_units = self._DEFAULT_CPU_CORE_UNITS
        return self.core_units

    def get_die_size_per_core(self):
        if not self.die_size_per_core:
            if self.die_size and self.core_units:
                self.die_size_per_core = self.die_size / self.core_units
            else:
                sub = _cpu_df
                if self.family:
                    sub = sub[sub['family'] == self.get_family()]
                if self.core_units:
                    sub = sub[sub['core_units'] == self.core_units]

                if len(sub) == 0 or len(sub) == len(_cpu_df):
                    self.die_size_per_core = self._DEFAULT_CPU_DIE_SIZE_PER_CORE

                elif len(sub) == 1:
                    self.die_size_per_core = float(sub['die_size_per_core'])

                else:
                    sub['_scope3'] = sub[['core_units', 'die_size_per_core']].apply(lambda x: x[0] * x[1], axis=1)
                    sub = sub.sort_values(by='_scope3', ascending=False)
                    row = sub.iloc[0]
                    die_size_per_core = float(row['die_size_per_core'])
                    core_units = int(row['core_units'])
                    self.die_size_per_core = die_size_per_core
                    self.core_units = core_units

        return self.die_size_per_core

    def get_family(self):
        if not self.family:
            pass  # TODO : find family from name
            if not self.family:
                self.family = self._DEFAULT_CPU_FAMILY
        return self.family

    def get_model_name(self):
        if not self.model_name:
            pass  # TODO : get model name from name
            if not self.model_name:
                self.model_name = self._DEFAULT_MODEL_FAMILY
        return self.model_name

    def impact_manufacture_gwp(self) -> (float, int):
        core_impact = self._IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self._IMPACT_FACTOR_DICT['gwp']['die_impact']
        cpu_impact = self._IMPACT_FACTOR_DICT['gwp']['impact']
        significant_figures = \
            rd.min_significant_figures(self.get_die_size_per_core(), core_impact, cpu_die_impact, cpu_impact)
        return (
                           self.get_core_units() * self.get_die_size_per_core() + core_impact) * cpu_die_impact + cpu_impact, significant_figures

    def impact_manufacture_pe(self) -> (float, int):
        core_impact = self._IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self._IMPACT_FACTOR_DICT['pe']['die_impact']
        cpu_impact = self._IMPACT_FACTOR_DICT['pe']['impact']
        significant_figures = rd.min_significant_figures(self.get_die_size_per_core(), core_impact, cpu_die_impact,
                                                         cpu_impact)
        return (
                           self.get_core_units() * self.get_die_size_per_core() + core_impact) * cpu_die_impact + cpu_impact, significant_figures

    def impact_manufacture_adp(self) -> (float, int):
        core_impact = self._IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self._IMPACT_FACTOR_DICT['adp']['die_impact']
        cpu_impact = self._IMPACT_FACTOR_DICT['adp']['impact']
        significant_figures = rd.min_significant_figures(self.get_die_size_per_core(), core_impact, cpu_die_impact,
                                                         cpu_impact)
        return (
                           self.get_core_units() * self.get_die_size_per_core() + core_impact) * cpu_die_impact + cpu_impact, significant_figures

    def impact_use_gwp(self, model=None) -> (float, int):
        model = None
        if not self.usage.hours_electrical_consumption:
            model = self.get_model_name()
        return super().impact_use_gwp(model)

    def impact_use_pe(self, model=None) -> (float, int):
        model = None
        if not self.usage.hours_electrical_consumption:
            model = self.get_model_name()
        return super().impact_use_pe(model)

    def impact_use_adp(self, model=None) -> (float, int):
        model = None
        if not self.usage.hours_electrical_consumption:
            model = self.get_model_name()
        return super().impact_use_adp(model)


class ComponentRAM(Component):
    TYPE = "RAM"

    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "die_impact": 2.20,
            "impact": 5.22
        },
        "pe": {
            "die_impact": 27.30,
            "impact": 74.00
        },
        "adp": {
            "die_impact": 6.30E-05,
            "impact": 1.69E-03
        }
    }

    _DEFAULT_RAM_CAPACITY = 32
    _DEFAULT_RAM_DENSITY = 0.625

    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None

    def get_density(self):
        if not self.density:
            sub = _ram_df

            if self.manufacturer:
                sub = sub[sub['manufacturer'] == self.manufacturer]

            if len(sub) == 0 or len(sub) == len(_cpu_df):
                self.density = self._DEFAULT_RAM_DENSITY

            elif len(sub) == 1:
                self.density = float(sub['density'])

            else:
                capacity = self.get_capacity()
                sub['_scope3'] = sub['density'].apply(lambda x: capacity / x)
                sub = sub.sort_values(by='_scope3', ascending=False)
                density = float(sub.iloc[0].density)
                self.density = density
        return self.density

    def get_capacity(self):
        if not self.capacity:
            self.capacity = self._DEFAULT_RAM_CAPACITY
        return self.capacity

    def impact_manufacture_gwp(self) -> (float, int):
        ram_die_impact = self._IMPACT_FACTOR_DICT['gwp']['die_impact']
        ram_impact = self._IMPACT_FACTOR_DICT['gwp']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ram_die_impact, ram_impact)
        return (self.get_capacity() / self.get_density()) * ram_die_impact + ram_impact, significant_figure

    def impact_manufacture_pe(self) -> (float, int):
        ram_die_impact = self._IMPACT_FACTOR_DICT['pe']['die_impact']
        ram_impact = self._IMPACT_FACTOR_DICT['pe']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ram_die_impact, ram_impact)
        return (self.get_capacity() / self.get_density()) * ram_die_impact + ram_impact, significant_figure

    def impact_manufacture_adp(self) -> (float, int):
        ram_die_impact = self._IMPACT_FACTOR_DICT['adp']['die_impact']
        ram_impact = self._IMPACT_FACTOR_DICT['adp']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ram_die_impact, ram_impact)
        return (self.get_capacity() / self.get_density()) * ram_die_impact + ram_impact, significant_figure

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentHDD(Component):
    TYPE = "HDD"
    _DEFAULT_HDD_CAPACITY = 500

    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "impact": 31.10
        },
        "pe": {
            "impact": 276.00
        },
        "adp": {
            "impact": 2.50E-04
        }

    }

    capacity: Optional[int] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None

    def get_capacity(self):
        if not self.capacity:
            self.capacity = self._DEFAULT_HDD_CAPACITY
        return self.capacity

    def impact_manufacture_gwp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['gwp']['impact'], 4

    def impact_manufacture_pe(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['pe']['impact'], 3

    def impact_manufacture_adp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['adp']['impact'], 3

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentSSD(Component):
    TYPE = "SSD"

    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "die_impact": 2.20,
            "impact": 6.34
        },
        "pe": {
            "die_impact": 27.30,
            "impact": 76.90
        },
        "adp": {
            "die_impact": 6.30E-05,
            "impact": 5.63E-04
        }
    }

    _DEFAULT_SSD_CAPACITY = 1000
    _DEFAULT_SSD_DENSITY = 48.5

    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None

    def get_density(self):
        if not self.density:
            sub = _ssd_df

            if self.manufacturer:
                sub = sub[sub['manufacturer'] == self.manufacturer]

            if len(sub) == 0 or len(sub) == len(_cpu_df):
                self.density = self.density if self.density else self._DEFAULT_SSD_DENSITY

            elif len(sub) == 1:
                self.density = float(sub['density'])

            else:
                capacity = self.get_capacity()
                sub['_scope3'] = sub['density'].apply(lambda x: capacity / x)
                sub = sub.sort_values(by='_scope3', ascending=False)
                density = float(sub.iloc[0].density)
                self.density = density
        return self.density

    def get_capacity(self):
        if not self.capacity:
            self.capacity = self._DEFAULT_SSD_CAPACITY
        return self.capacity

    def impact_manufacture_gwp(self) -> (float, int):
        ssd_die_impact = self._IMPACT_FACTOR_DICT['gwp']['die_impact']
        ssd_impact = self._IMPACT_FACTOR_DICT['gwp']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ssd_impact, ssd_die_impact)
        return (self.get_capacity() / self.get_density()) * ssd_die_impact + ssd_impact, significant_figure

    def impact_manufacture_pe(self) -> (float, int):
        ssd_die_impact = self._IMPACT_FACTOR_DICT['pe']['die_impact']
        ssd_impact = self._IMPACT_FACTOR_DICT['pe']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ssd_impact, ssd_die_impact)
        return (self.get_capacity() / self.get_density()) * ssd_die_impact + ssd_impact, significant_figure

    def impact_manufacture_adp(self) -> (float, int):
        ssd_die_impact = self._IMPACT_FACTOR_DICT['adp']['die_impact']
        ssd_impact = self._IMPACT_FACTOR_DICT['adp']['impact']
        significant_figure = rd.min_significant_figures(self.get_density(), ssd_impact, ssd_die_impact)
        return (self.get_capacity() / self.get_density()) * ssd_die_impact + ssd_impact, significant_figure

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentPowerSupply(Component):
    TYPE = "POWER_SUPPLY"
    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "impact": 24.30
        },
        "pe": {
            "impact": 352.00
        },
        "adp": {
            "impact": 8.30E-03
        }
    }

    _DEFAULT_POWER_SUPPLY_WEIGHT = 2.99

    unit_weight: Optional[float] = None

    def get_unit_weight(self):
        if not self.unit_weight:
            self.unit_weight = self._DEFAULT_POWER_SUPPLY_WEIGHT
        return self.unit_weight

    def impact_manufacture_gwp(self) -> (float, int):
        power_supply_weight = self.get_unit_weight()
        power_supply_impact = self._IMPACT_FACTOR_DICT['gwp']['impact']
        return power_supply_weight * power_supply_impact, 4

    def impact_manufacture_pe(self) -> (float, int):
        power_supply_weight = self.get_unit_weight()
        power_supply_impact = self._IMPACT_FACTOR_DICT['pe']['impact']
        return power_supply_weight * power_supply_impact, 3

    def impact_manufacture_adp(self) -> (float, int):
        power_supply_weight = self.get_unit_weight()
        power_supply_impact = self._IMPACT_FACTOR_DICT['adp']['impact']
        return power_supply_weight * power_supply_impact, 3

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentMotherBoard(Component):
    TYPE = "MOTHERBOARD"
    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "impact": 66.10
        },
        "pe": {
            "impact": 836.00
        },
        "adp": {
            "impact": 3.69E-03
        }
    }

    def impact_manufacture_gwp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['gwp']['impact'], 4

    def impact_manufacture_pe(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['pe']['impact'], 3

    def impact_manufacture_adp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['adp']['impact'], 3

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentCase(Component):
    TYPE = "CASE"
    case_type: str = None
    _IMPACT_FACTOR_DICT = {
        "rack": {
            "gwp": {
                "impact": 150.00
            },
            "pe": {
                "impact": 2200.00

            },
            "adp": {
                "impact": 2.02E-02
            }
        },
        "blade": {
            "gwp": {
                "impact_blade_server": 30.90,
                "impact_blade_16_slots": 880.00
            },
            "pe": {
                "impact_blade_server": 435.00,
                "impact_blade_16_slots": 12700.00
            },
            "adp": {
                "impact_blade_server": 6.72E-04,
                "impact_blade_16_slots": 4.32E-01
            }
        }

    }

    def get_case_type(self):
        if not self.case_type:
            self.case_type = "rack"
        return self.case_type

    def impact_manufacture_gwp(self) -> (float, int):
        if self.get_case_type() == "blade":
            impact_blade_16_slots = self._IMPACT_FACTOR_DICT['blade']['gwp']['impact_blade_16_slots']
            impact_blade_server = self._IMPACT_FACTOR_DICT['blade']['gwp']['impact_blade_server']
            sigfig = rd.min_significant_figures(impact_blade_16_slots, impact_blade_server)
            return (impact_blade_16_slots / 16) + impact_blade_server, sigfig
        else:
            return self._IMPACT_FACTOR_DICT['rack']['gwp']['impact'], 5

    def impact_manufacture_pe(self) -> (float, int):
        if self.get_case_type() == "blade":
            impact_blade_16_slots = self._IMPACT_FACTOR_DICT['blade']['pe']['impact_blade_16_slots']
            impact_blade_server = self._IMPACT_FACTOR_DICT['blade']['pe']['impact_blade_server']
            sigfig = rd.min_significant_figures(impact_blade_16_slots, impact_blade_server)
            return (impact_blade_16_slots / 16) + impact_blade_server, sigfig
        else:
            return self._IMPACT_FACTOR_DICT['rack']['pe']['impact'], 4

    def impact_manufacture_adp(self) -> (float, int):
        if self.get_case_type() == "blade":
            impact_blade_16_slots = self._IMPACT_FACTOR_DICT['blade']['adp']['impact_blade_16_slots']
            impact_blade_server = self._IMPACT_FACTOR_DICT['blade']['adp']['impact_blade_server']
            sigfig = rd.min_significant_figures(impact_blade_16_slots, impact_blade_server)
            return (impact_blade_16_slots / 16) + impact_blade_server, sigfig
        else:
            return self._IMPACT_FACTOR_DICT['rack']['adp']['impact'], 3

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"


class ComponentAssembly(Component):
    TYPE = "ASSEMBLY"

    _IMPACT_FACTOR_DICT = {
        "gwp": {
            "impact": 6.68

        },
        "pe": {
            "impact": 68.60

        },
        "adp": {
            "impact": 1.41E-06
        }
    }

    def impact_manufacture_gwp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['gwp']['impact'], 3

    def impact_manufacture_pe(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['pe']['impact'], 3

    def impact_manufacture_adp(self) -> (float, int):
        return self._IMPACT_FACTOR_DICT['adp']['impact'], 3

    def impact_use_gwp(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_pe(self, model=None) -> (float, int):
        return "not implemented"

    def impact_use_adp(self, model=None) -> (float, int):
        return "not implemented"
