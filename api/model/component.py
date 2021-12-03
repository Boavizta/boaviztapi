from typing import Optional

from pydantic import BaseModel


class ComponentCPU(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    family: Optional[str] = None

    def impact_gwp(self) -> float:
        core_impact = self.IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self.IMPACT_FACTOR_DICT['gwp']['die_impact']
        cpu_impact = self.IMPACT_FACTOR_DICT['gwp']['impact']
        return (self.core_units * self.die_size_per_core + core_impact) * cpu_die_impact + cpu_impact

    def impact_pe(self) -> float:
        core_impact = self.IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self.IMPACT_FACTOR_DICT['pe']['die_impact']
        cpu_impact = self.IMPACT_FACTOR_DICT['pe']['impact']
        return (self.core_units * self.die_size_per_core + core_impact) * cpu_die_impact + cpu_impact

    def impact_adp(self) -> float:
        core_impact = self.IMPACT_FACTOR_DICT['constant_core_impact']
        cpu_die_impact = self.IMPACT_FACTOR_DICT['adp']['die_impact']
        cpu_impact = self.IMPACT_FACTOR_DICT['adp']['impact']
        return (self.core_units * self.die_size_per_core + core_impact) * cpu_die_impact + cpu_impact


class ComponentRAM(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    capacity: Optional[int] = None
    density: Optional[float] = None
    process: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None
    integrator: Optional[str] = None

    def impact_gwp(self) -> float:
        ram_die_impact = self.IMPACT_FACTOR_DICT['gwp']['die_impact']
        ram_impact = self.IMPACT_FACTOR_DICT['gwp']['impact']
        return (self.capacity / self.density) * ram_die_impact + ram_impact

    def impact_pe(self) -> float:
        ram_die_impact = self.IMPACT_FACTOR_DICT['pe']['die_impact']
        ram_impact = self.IMPACT_FACTOR_DICT['pe']['impact']
        return (self.capacity / self.density) * ram_die_impact + ram_impact

    def impact_adp(self) -> float:
        ram_die_impact = self.IMPACT_FACTOR_DICT['adp']['die_impact']
        ram_impact = self.IMPACT_FACTOR_DICT['adp']['impact']
        return (self.capacity / self.density) * ram_die_impact + ram_impact


class ComponentHDD(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    def impact_gwp(self) -> float:
        return self.IMPACT_FACTOR_DICT['gwp']['impact']

    def impact_pe(self) -> float:
        return self.IMPACT_FACTOR_DICT['pe']['impact']

    def impact_adp(self) -> float:
        return self.IMPACT_FACTOR_DICT['adp']['impact']


class ComponentSSD(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    capacity: Optional[int] = None
    density: Optional[float] = None
    manufacturer: Optional[str] = None
    manufacture_date: Optional[str] = None
    model: Optional[str] = None

    def impact_gwp(self) -> float:
        ssd_die_impact = self.IMPACT_FACTOR_DICT['gwp']['die_impact']
        ssd_impact = self.IMPACT_FACTOR_DICT['gwp']['impact']
        return (self.capacity / self.density) * ssd_die_impact + ssd_impact

    def impact_pe(self) -> float:
        ssd_die_impact = self.IMPACT_FACTOR_DICT['pe']['die_impact']
        ssd_impact = self.IMPACT_FACTOR_DICT['pe']['impact']
        return (self.capacity / self.density) * ssd_die_impact + ssd_impact

    def impact_adp(self) -> float:
        ssd_die_impact = self.IMPACT_FACTOR_DICT['adp']['die_impact']
        ssd_impact = self.IMPACT_FACTOR_DICT['adp']['impact']
        return (self.capacity / self.density) * ssd_die_impact + ssd_impact


class PowerSupply(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    unit_weight: Optional[float] = None

    def impact_gwp(self) -> float:
        power_supply_weight = self.unit_weight
        power_supply_impact = self.IMPACT_FACTOR_DICT['gwp']['impact']
        return power_supply_weight * power_supply_impact

    def impact_pe(self) -> float:
        power_supply_weight = self.unit_weight
        power_supply_impact = self.IMPACT_FACTOR_DICT['pe']['impact']
        return power_supply_weight * power_supply_impact

    def impact_adp(self) -> float:
        power_supply_weight = self.unit_weight
        power_supply_impact = self.IMPACT_FACTOR_DICT['adp']['impact']
        return power_supply_weight * power_supply_impact


class MotherBoard(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    def impact_gwp(self) -> float:
        return self.IMPACT_FACTOR_DICT['gwp']['impact']

    def impact_pe(self) -> float:
        return self.IMPACT_FACTOR_DICT['pe']['impact']

    def impact_adp(self) -> float:
        return self.IMPACT_FACTOR_DICT['adp']['impact']


class Rack(BaseModel):
    IMPACT_FACTOR_DICT = {
        "gwp": {
            "impact": 150.00
        },
        "pe": {
            "impact": 2200.00
        },
        "adp": {
            "impact": 2.02E-02
        }
    }

    def impact_gwp(self) -> float:
        return self.IMPACT_FACTOR_DICT['gwp']['impact']

    def impact_pe(self) -> float:
        return self.IMPACT_FACTOR_DICT['pe']['impact']

    def impact_adp(self) -> float:
        return self.IMPACT_FACTOR_DICT['adp']['impact']


class Blade(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    def impact_gwp(self) -> float:
        return self.IMPACT_FACTOR_DICT['gwp']['impact']

    def impact_pe(self) -> float:
        return self.IMPACT_FACTOR_DICT['pe']['impact']

    def impact_adp(self) -> float:
        return self.IMPACT_FACTOR_DICT['adp']['impact']


class Assembly(BaseModel):
    IMPACT_FACTOR_DICT = {
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

    def impact_gwp(self) -> float:
        return self.IMPACT_FACTOR_DICT['gwp']['impact']

    def impact_pe(self) -> float:
        return self.IMPACT_FACTOR_DICT['pe']['impact']

    def impact_adp(self) -> float:
        return self.IMPACT_FACTOR_DICT['adp']['impact']
