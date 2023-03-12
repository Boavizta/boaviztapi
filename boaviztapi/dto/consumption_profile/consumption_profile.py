import os
from typing import List

import pandas as pd

from boaviztapi.dto import BaseDTO
from boaviztapi.dto.component import CPU
from boaviztapi.model.component import ComponentCPU
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel

_cpu_index = os.path.join(os.path.dirname(__file__), '../../data/crowdsourcing/cpu_index.csv')


class WorkloadPower(BaseDTO):
    load_percentage: float = None
    power_watt: float = None


class ConsumptionProfile(BaseDTO):
    workload: List[WorkloadPower] = None

    class Config:
        arbitrary_types_allowed = True


class ConsumptionProfileCPU(ConsumptionProfile):
    cpu: CPU = None


def mapper_cp(cp_dto: ConsumptionProfile) -> CPUConsumptionProfileModel:
    cp = CPUConsumptionProfileModel()
    if cp_dto.workload is not None:
        cp.workloads.set_input(cp_dto.workload)
    return cp


def mapper_cp_cpu(cp_dto: ConsumptionProfileCPU) -> (CPUConsumptionProfileModel, ComponentCPU):
    cpu = ComponentCPU()
    manufacturer, model_range, family = None, None, None

    if cp_dto.cpu.name is not None:
        manufacturer, model_range, family = attributes_from_cpu_name(cp_dto.cpu.name)

    if cp_dto.cpu.manufacturer is not None:
        cpu.manufacturer.set_input(cp_dto.cpu.manufacturer)
    elif manufacturer is not None:
        cpu.manufacturer.set_completed(manufacturer)

    if cp_dto.cpu.model_range is not None:
        cpu.model_range.set_input(cp_dto.cpu.model_range)
    elif model_range is not None:
        cpu.model_range.set_input(model_range)

    return mapper_cp(cp_dto), cpu
