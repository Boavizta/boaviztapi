from typing import Optional, Union, Dict

from boaviztapi.dto import BaseDTO


class WorkloadUnit(BaseDTO):
    time_ratio: Optional[float] = None
    power_ratio: Optional[float] = None
    power: Optional[float] = None


class Usage(BaseDTO):
    years_use_time: Optional[float] = None
    days_use_time: Optional[float] = None
    hours_use_time: Optional[float] = None

    year_life_time: Optional[float] = None

    hours_electrical_consumption: Optional[float] = None
    workload: Optional[Dict[str, WorkloadUnit]] = None

    usage_location: Optional[str] = None
    gwp_factor: Optional[float] = None
    pe_factor: Optional[float] = None
    adp_factor: Optional[float] = None


class UsageServer(Usage):
    other_consumption_ratio: Optional[float] = None


class UsageCloud(UsageServer):
    instance_per_server: Optional[int] = None


class UsageComponent(BaseDTO):
    year_life_time: Optional[float] = None
