from typing import Optional, Union, Dict

from boaviztapi.dto import BaseDTO


class Usage(BaseDTO):
    years_use_time: Optional[float] = None
    days_use_time: Optional[float] = None
    hours_use_time: Optional[float] = None

    hours_electrical_consumption: Optional[float] = None
    workload: Optional[Union[Dict[str, float], float]] = None

    usage_location: Optional[str] = None
    gwp_factor: Optional[float] = None
    pe_factor: Optional[float] = None
    adp_factor: Optional[float] = None


class UsageServer(Usage):
    other_consumption_ratio: Optional[float] = None


class UsageCloud(UsageServer):
    instance_per_server: Optional[int] = None
