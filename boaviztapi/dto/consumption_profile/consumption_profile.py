from typing import List, Tuple, Optional

import pandas as pd
from rapidfuzz import process, fuzz

from boaviztapi.dto import BaseDTO
from boaviztapi.dto.component import CPU
from boaviztapi.model.consumption_profile import CPUConsumptionProfileModel

_cpu_index = pd.read_csv('./boaviztapi/data/components/cpu_index.csv')


class Workload:
    load: float = None
    power: float = None


class ConsumptionProfile(BaseDTO):
    workload: List[Workload] = None

    class Config:
        arbitrary_types_allowed = True


class ConsumptionProfileCPU(ConsumptionProfile):
    cpu: CPU = None


def smart_mapper_consumption_profile_cpu(cp_cpu_dto: ConsumptionProfileCPU) -> CPUConsumptionProfileModel:
    cpu_manufacturer, cpu_sub_name = parse_cpu_name(cp_cpu_dto.cpu.name)
    if cpu_manufacturer is None:
        name_list = list(_cpu_index.sub_model_name.unique())
    else:
        name_list = list(_cpu_index[_cpu_index['manufacturer'] == cpu_manufacturer].sub_model_name.unique())
    result = match_cpu_model_range(cpu_sub_name, name_list)
    if result is not None:
        model_range = _cpu_index[_cpu_index['sub_model_name'] == result[0]].iloc[0].model_range
    else:
        model_range = None

    cpu_consumption_profile = CPUConsumptionProfileModel()
    cpu_consumption_profile.cpu_manufacturer.value = cpu_manufacturer
    cpu_consumption_profile.cpu_model_range.value = model_range
    return cpu_consumption_profile


def parse_cpu_name(cpu_name: str) -> Tuple[str, str]:
    vendor_list = ["intel", "amd", "arm"]  # every string in lowercase
    for vendor in vendor_list:
        if vendor in cpu_name:
            cpu_name.replace(vendor, '')
            return vendor, cpu_name.replace(vendor, '')
    return None, cpu_name


def match_cpu_model_range(cpu_name_to_match: str, cpu_name_list: list) -> Optional[Tuple[str, float, int]]:
    foo = process.extractOne(cpu_name_to_match, cpu_name_list, scorer=fuzz.WRatio)
    if foo is not None:
        return foo if foo[1] > 88.0 else None


if __name__ == '__main__':
    cp_cpu = ConsumptionProfileCPU(cpu=CPU(name="Intel Xeon W-2155"))
    cp_model = smart_mapper_consumption_profile_cpu(cp_cpu)

    print(cp_model.cpu_manufacturer.value)
    print(cp_model.cpu_model_range.value)

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
