import os
from typing import Optional, List, Union

import pandas as pd

from boaviztapi.dto import BaseDTO
from boaviztapi.model.boattribute import Status, Boattribute
from boaviztapi.model.usage import ModelUsage, ModelUsageServer, ModelUsageCloud
from boaviztapi.model.usage.usage import default_impact_factor

_electricity_emission_factors_df = pd.read_csv(os.path.join(os.path.dirname(__file__),
                                                            '../../data/electricity/electricity_impact_factors.csv'))


class WorkloadTime(BaseDTO):
    time_percentage: float = None
    load_percentage: float = None


class Usage(BaseDTO):
    years_use_time: Optional[float] = None
    days_use_time: Optional[float] = None
    hours_use_time: Optional[float] = None

    years_life_time: Optional[float] = None

    hours_electrical_consumption: Optional[float] = None
    time_workload: Optional[Union[float, List[WorkloadTime]]] = None

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

    if usage_dto.time_workload is not None:
        usage_model.time_workload.value = usage_dto.time_workload
        usage_model.time_workload.min = usage_dto.time_workload
        usage_model.time_workload.max = usage_dto.time_workload

        if type(usage_dto.time_workload) == float:
            usage_model.time_workload.unit = "%"
        else:
            usage_model.time_workload.unit = "(time_percentage:%, load_percentage: %)"
        usage_model.time_workload.status = Status.INPUT

    if usage_dto.hours_electrical_consumption is not None:
        usage_model.hours_electrical_consumption.set_input(usage_dto.hours_electrical_consumption)

    if usage_dto.years_life_time is not None:
        usage_model.life_time.set_input(usage_dto.years_life_time * 24 * 365)

    if usage_dto.hours_use_time is not None or usage_dto.days_use_time is not None or usage_dto.years_use_time is not None:
        usage_model.use_time.set_input((usage_dto.hours_use_time or 0) + \
                                     (usage_dto.days_use_time or 0) * 24 + \
                                     (usage_dto.years_use_time or 0) * 24 * 365)

    if usage_dto.usage_location is not None:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == usage_dto.usage_location]
        if len(sub) == 0:
            pass
        else:
            usage_model.usage_location.set_input(usage_dto.usage_location)

    return usage_model


def smart_mapper_usage_server(usage_dto: UsageServer) -> ModelUsageServer:
    usage_model_server = ModelUsageServer()

    if usage_dto.hours_electrical_consumption is not None:
        usage_model_server.hours_electrical_consumption.set_input(usage_dto.hours_electrical_consumption)

    if usage_dto.years_life_time is not None:
        usage_model_server.life_time.set_input(usage_dto.years_life_time * 24 * 365)

    if usage_dto.hours_use_time is not None or usage_dto.days_use_time is not None or usage_dto.years_use_time is not None:
        usage_model_server.use_time.set_input((usage_dto.hours_use_time or 0) + \
                                     (usage_dto.days_use_time or 0) * 24 + \
                                     (usage_dto.years_use_time or 0) * 24 * 365)

    if usage_dto.time_workload is not None:
        usage_model_server.time_workload.set_input(usage_dto.time_workload)

    if usage_dto.usage_location is not None:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == usage_dto.usage_location]
        if len(sub) == 0:
            pass
        else:
            usage_model_server.usage_location.set_input(usage_dto.usage_location)

    if usage_dto.other_consumption_ratio is not None:
        usage_model_server.other_consumption_ratio.set_input(usage_dto.other_consumption_ratio)

    return usage_model_server


def smart_mapper_usage_cloud(usage_dto: UsageCloud):
    usage_model_cloud = ModelUsageCloud()

    if usage_dto.hours_electrical_consumption is not None:
        usage_model_cloud.hours_electrical_consumption.set_input(usage_dto.hours_electrical_consumption)

    if usage_dto.years_life_time is not None:
        usage_model_cloud.life_time.set_input(usage_dto.years_life_time * 24 * 365)

    if usage_dto.hours_use_time is not None or usage_dto.days_use_time is not None or usage_dto.years_use_time is not None:
        usage_model_cloud.use_time.set_input((usage_dto.hours_use_time or 0) + \
                                            (usage_dto.days_use_time or 0) * 24 + \
                                            (usage_dto.years_use_time or 0) * 24 * 365)

    if usage_dto.time_workload is not None:
        usage_model_cloud.time_workload.set_input(usage_dto.time_workload)

    if usage_dto.usage_location is not None:
        sub = _electricity_emission_factors_df
        sub = sub[sub['code'] == usage_dto.usage_location]
        if len(sub) == 0:
            pass
        else:
            usage_model_cloud.usage_location.set_input(usage_dto.usage_location)

    if usage_dto.other_consumption_ratio is not None:
        usage_model_cloud.other_consumption_ratio.set_input(usage_dto.other_consumption_ratio)
        usage_model_cloud.other_consumption_ratio.set_input(Status.INPUT)

    if usage_dto.instance_per_server is not None:
        usage_model_cloud.instance_per_server.set_input(usage_dto.instance_per_server)

    return usage_model_cloud
