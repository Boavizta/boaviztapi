from typing import List

import pandas as pd

from boaviztapi.dto import BaseDTO
from boaviztapi.dto.component import CPU
from boaviztapi.dto.component.cpu import attributes_from_cpu_name
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentCPU
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel

_cpu_index = pd.read_csv('./boaviztapi/data/components/cpu_index.csv')


class WorkloadPower(BaseDTO):
    load: float = None
    power: float = None


class ConsumptionProfile(BaseDTO):
    workload: List[WorkloadPower] = None

    class Config:
        arbitrary_types_allowed = True


class ConsumptionProfileCPU(ConsumptionProfile):
    cpu: CPU = None


def mapper_cp(cp_dto: ConsumptionProfile) -> CPUConsumptionProfileModel:
    cp = CPUConsumptionProfileModel()
    cp.power_workloads.value = cp_dto.workload
    cp.power_workloads.status = Status.INPUT
    return cp


def mapper_cp_cpu(cp_dto: ConsumptionProfileCPU) -> (CPUConsumptionProfileModel, ComponentCPU):

    cpu = ComponentCPU()
    manufacturer, model_range, family = None, None, None

    if cp_dto.cpu.name is not None:
        manufacturer, model_range, family = attributes_from_cpu_name(cp_dto.cpu.name)

    if cp_dto.cpu.manufacturer is not None:
        cpu.manufacturer.value = cp_dto.cpu.manufacturer
        cpu.manufacturer.status = Status.INPUT
    elif manufacturer is not None:
        cpu.manufacturer.value = manufacturer
        cpu.manufacturer.status = Status.COMPLETED

    if cp_dto.cpu.model_range is not None:
        cpu.model_range = cp_dto.cpu.model_range
        cpu.model_range.status = Status.INPUT
    elif model_range is not None:
        cpu.model_range.value = model_range
        cpu.model_range.status = Status.COMPLETED

    return mapper_cp(cp_dto), cpu

# Intel Pentium Gold G5500T
# Intel Xeon Platinum 8253
# Intel Core i7-5650U
# Intel Xeon D-1533N
# Intel Xeon W-2155
# AMD EPYC 7352
# AMD EPYC 7713P
# intel Xeon Minister of Ecology isn't good enough
# Intel Core i75650U
# Intel Xeon D 1533N
# Intel Xeon W 2155
# AMD-EPYC 7352
# Intel xeon-Gold 6244
# Intel Pentium Gold G5500T
# Intel Xeon Platinum 8253
# Intel Core i7-5650U
# Intel Xeon D-1533N
# Intel Xeon W-2155
