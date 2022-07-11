from typing import Optional, Dict

import pandas as pd

from boaviztapi.dto import BaseDTO
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.usage import ModelUsage, ModelUsageServer

_electricity_emission_factors_df = pd.read_csv('./boaviztapi/data/electricity/electricity_impact_factors.csv')


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


def smart_mapper_usage(usage_dto: Usage) -> ModelUsage:
    usage_model = ModelUsage()

    if usage_dto.hours_electrical_consumption is not None:
        usage_model.hours_electrical_consumption.value = usage_dto.hours_electrical_consumption
        usage_model.hours_electrical_consumption.status = Status.INPUT

    if usage_dto.workload is not None:
        pass  # TODO

    if usage_dto.year_life_time is not None:
        usage_model.life_time.value = usage_dto.year_life_time
        usage_model.life_time.status = Status.INPUT

    if usage_dto.hours_use_time is not None or usage_dto.days_use_time is not None or usage_dto.years_use_time is not None:
        usage_model.use_time.value = (usage_dto.hours_use_time or 0) + \
                                     (usage_dto.days_use_time or 0) * 24 + \
                                     (usage_dto.years_use_time or 0) * 24 * 365

        usage_model.use_time.status = Status.INPUT

    if usage_dto.usage_location is not None:

        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == usage_dto.usage_location]
        if len(sub) == 0:
            pass
        else:
            usage_model.usage_location.value = usage_dto.usage_location
            usage_model.usage_location.status = Status.INPUT

    return usage_model


def smart_mapper_usage_server(usage_dto: UsageServer) -> ModelUsageServer:
    usage = smart_mapper_usage(usage_dto)
    usage_server_model = ModelUsageServer()

    for attr, val in usage.__iter__():
        if isinstance(val, Boattribute):
            usage_server_model.__getattribute__(attr).__setattr__("val", val)

    if usage_dto.other_consumption_ratio is not None:
        usage_server_model.other_consumption_ratio.value = usage_dto.other_consumption_ratio
        usage_server_model.other_consumption_ratio.status = Status.INPUT

    return usage_server_model
