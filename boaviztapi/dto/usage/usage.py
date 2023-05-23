import os
from typing import Optional, List, Union

import pandas as pd

from boaviztapi import config
from boaviztapi.dto import BaseDTO
from boaviztapi.model.boattribute import Status
from boaviztapi.model.usage import ModelUsage, ModelUsageServer, ModelUsageCloud
from boaviztapi.service.archetype import get_cloud_instance_archetype, get_server_archetype
from boaviztapi.service.factor_provider import get_available_countries


class WorkloadTime(BaseDTO):
    time_percentage: float = None
    load_percentage: float = None


class ElecFactors(BaseDTO):
    gwp: Optional[float] = None
    adp: Optional[float] = None
    pe: Optional[float] = None
    gwppb: Optional[float] = None
    gwppf: Optional[float] = None
    gwpplu: Optional[float] = None
    ir: Optional[float] = None
    lu: Optional[float] = None
    odp: Optional[float] = None
    pm: Optional[float] = None
    pocp: Optional[float] = None
    wu: Optional[float] = None
    mips: Optional[float] = None
    adpe: Optional[float] = None
    adpf: Optional[float] = None
    ap: Optional[float] = None
    ctue: Optional[float] = None
    ctuh_c: Optional[float] = None
    ctuh_nc: Optional[float] = None
    epf: Optional[float] = None
    epm: Optional[float] = None
    ept: Optional[float] = None


class Usage(BaseDTO):
    years_use_time: Optional[float] = None
    days_use_time: Optional[float] = None
    hours_use_time: Optional[float] = None

    years_life_time: Optional[float] = None

    hours_electrical_consumption: Optional[float] = None
    time_workload: Optional[Union[float, List[WorkloadTime]]] = None

    usage_location: Optional[str] = None
    elec_factors: Optional[ElecFactors] = ElecFactors()


class UsageServer(Usage):
    other_consumption_ratio: Optional[float] = None


class UsageCloud(UsageServer):
    instance_per_server: Optional[int] = None


def mapper_usage(usage_dto: Usage, archetype=None) -> ModelUsage:
    usage_model = ModelUsage(archetype=archetype)

    for elec_factor in usage_dto.elec_factors.__dict__.keys():
        if usage_dto.elec_factors.__dict__[elec_factor] is not None:
            usage_model.elec_factors.get(elec_factor).set_input(usage_dto.elec_factors.__dict__[elec_factor])

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
        if usage_dto.usage_location in get_available_countries(reverse=True):
            usage_model.usage_location.set_input(usage_dto.usage_location)
        else:
            usage_model.usage_location.set_changed(usage_model.usage_location.default)
            usage_model.usage_location.add_warning("Location not found. Default value used.")

    return usage_model


def mapper_usage_server(usage_dto: UsageServer, archetype=get_server_archetype(config["default_server"]).get("USAGE")) -> ModelUsageServer:
    usage_model_server = ModelUsageServer(archetype=archetype)

    for elec_factor in usage_dto.elec_factors.__dict__.keys():
        if usage_dto.elec_factors.__dict__[elec_factor] is not None:
            usage_model_server.elec_factors.get(elec_factor).set_input(usage_dto.elec_factors.__dict__[elec_factor])

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
        if usage_dto.usage_location in get_available_countries(reverse=True):
            usage_model_server.usage_location.set_input(usage_dto.usage_location)
        else:
            usage_model_server.usage_location.set_changed(usage_model_server.usage_location.default)
            usage_model_server.usage_location.add_warning("Location not found. Default value used.")
    if usage_dto.other_consumption_ratio is not None:
        usage_model_server.other_consumption_ratio.set_input(usage_dto.other_consumption_ratio)

    return usage_model_server


def mapper_usage_cloud(usage_dto: UsageCloud, archetype=get_cloud_instance_archetype(config["default_cloud"], config["default_cloud_provider"]).get("USAGE")) -> ModelUsageCloud:
    usage_model_cloud = ModelUsageCloud(archetype=archetype)

    for elec_factor in usage_dto.elec_factors.__dict__.keys():
        if usage_dto.elec_factors.__dict__[elec_factor] is not None:
            usage_model_cloud.elec_factors.get(elec_factor).set_input(usage_dto.elec_factors.__dict__[elec_factor])

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
        if usage_dto.usage_location in get_available_countries(reverse=True):
            usage_model_cloud.usage_location.set_input(usage_dto.usage_location)
        else:
            usage_model_cloud.usage_location.set_changed(usage_model_cloud.usage_location.default)
            usage_model_cloud.usage_location.add_warning("Location not found. Default value used.")

    if usage_dto.other_consumption_ratio is not None:
        usage_model_cloud.other_consumption_ratio.set_input(usage_dto.other_consumption_ratio)

    if usage_dto.instance_per_server is not None:
        usage_model_cloud.instance_per_server.set_input(usage_dto.instance_per_server)

    return usage_model_cloud
