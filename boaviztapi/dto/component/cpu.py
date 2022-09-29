import os
from typing import Optional, Tuple

import pandas as pd
from rapidfuzz import fuzz, process

from boaviztapi.dto.component import ComponentDTO
from boaviztapi.dto.usage.usage import smart_mapper_usage, Usage
from boaviztapi.model.boattribute import Status
from boaviztapi.model.component import ComponentCPU
from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf

_cpu_df = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/cpu_manufacture.csv'))
_cpu_index = pd.read_csv(os.path.join(os.path.dirname(__file__), '../../data/components/cpu_index.csv'))


class CPU(ComponentDTO):
    core_units: Optional[int] = None
    die_size: Optional[float] = None
    die_size_per_core: Optional[float] = None
    manufacturer: Optional[str] = None
    model_range: Optional[str] = None
    family: Optional[str] = None
    name: Optional[str] = None
    tdp: Optional[int] = None


def smart_mapper_cpu(cpu_dto: CPU) -> ComponentCPU:
    cpu_component = ComponentCPU()
    cpu_component.usage = smart_mapper_usage(cpu_dto.usage or Usage())

    cpu_component.units = cpu_dto.units

    if cpu_dto.name is not None:
        manufacturer, model_range, family = attributes_from_cpu_name(cpu_dto.name)
        if manufacturer is not None:
            cpu_dto.manufacturer = manufacturer
            cpu_component.manufacturer.value = manufacturer
            cpu_component.manufacturer.status = Status.COMPLETED
        if model_range is not None:
            cpu_dto.model_range = model_range
            cpu_component.model_range.value = model_range
            cpu_component.model_range.status = Status.COMPLETED
        if family is not None:
            cpu_dto.family = family
            cpu_component.family.value = family
            cpu_component.family.status = Status.COMPLETED

    if cpu_dto.family is not None and cpu_component.family.status != Status.COMPLETED:
        cpu_component.family.value = cpu_dto.family
        cpu_component.family.status = Status.INPUT

    if cpu_dto.core_units is not None:
        cpu_component.core_units.value = cpu_dto.core_units
        cpu_component.core_units.status = Status.INPUT

    if cpu_dto.tdp is not None:
        cpu_component.tdp.value = cpu_dto.tdp
        cpu_component.tdp.status = Status.INPUT

    if cpu_dto.model_range is not None:
        cpu_component.model_range.value = cpu_dto.model_range
        cpu_component.model_range.status = Status.INPUT

    if cpu_dto.die_size_per_core is not None:
        cpu_component.die_size_per_core.value = cpu_dto.die_size_per_core
        cpu_component.die_size_per_core.status = Status.INPUT

    elif cpu_dto.die_size is not None and cpu_dto.core_units is not None:
        cpu_component.die_size_per_core.value = cpu_dto.die_size / cpu_dto.core_units
        cpu_component.die_size_per_core.status = Status.COMPLETED
        cpu_component.die_size_per_core.source = "INPUT : die_size / core_units"

    else:
        sub = _cpu_df
        if cpu_dto.family is not None:
            corrected_family = fuzzymatch_attr_from_pdf(cpu_dto.family, "family", sub)
            if corrected_family != cpu_dto.family:
                cpu_component.family.value = corrected_family
                cpu_component.family.status = Status.CHANGED
            tmp = sub[sub['family'] == corrected_family]
            if len(tmp) > 0:
                sub = tmp.copy()

        if cpu_dto.core_units is not None:
            tmp = sub[sub['core_units'] == cpu_dto.core_units]
            if len(tmp) > 0:
                sub = tmp.copy()

        if len(sub) == 0 or len(sub) == len(_cpu_df):
            pass
        elif len(sub) == 1:
            cpu_component.die_size_per_core.value = float(sub['die_size_per_core'])
            cpu_component.die_size_per_core.status = Status.COMPLETED
            cpu_component.die_size_per_core.source = sub['Source']
        else:
            sub['_scope3'] = sub[['core_units', 'die_size_per_core']].apply(lambda x: x[0] * x[1], axis=1)
            sub = sub.sort_values(by='_scope3', ascending=False)
            row = sub.iloc[0]

            cpu_component.die_size_per_core.value = float(row['die_size_per_core'])
            cpu_component.die_size_per_core.source = row['Source']

            if cpu_dto.die_size_per_core is None:
                cpu_component.die_size_per_core.status = Status.COMPLETED
            else:
                cpu_component.die_size_per_core.status = Status.CHANGED

            cpu_component.core_units.value = int(row['core_units'])
            cpu_component.core_units.source = row['Source']

            if cpu_dto.core_units is None:
                cpu_component.core_units.status = Status.COMPLETED
            else:
                cpu_component.core_units.status = Status.CHANGED

    return cpu_component


def attributes_from_cpu_name(cpu_name: str) -> [str, str, str]:
    cpu_name = cpu_name.lower()
    manufacturer, cpu_sub_name = parse(cpu_name)
    sub = _cpu_index
    if manufacturer is None:
        name_list = list(sub.sub_model_name.unique())
    else:
        name_list = list(sub[sub['manufacturer'] == manufacturer].sub_model_name.unique())
    result = fuzzymatch(cpu_sub_name, name_list)
    if result is not None:
        model_range = sub[sub['sub_model_name'] == result[0]].iloc[0].model_range
        family = sub[sub['sub_model_name'] == result[0]].iloc[0].family
    else:
        model_range = None
        family = None

    return manufacturer, model_range, family


def parse(cpu_name: str) -> Tuple[str, str]:
    vendor_list = ["intel", "amd", "arm"]  # every string in lowercase
    for vendor in vendor_list:
        if vendor in cpu_name:
            cpu_name.replace(vendor, '')
            return vendor, cpu_name.replace(vendor, '')
    return None, cpu_name


def fuzzymatch(cpu_name_to_match: str, cpu_name_list: list) -> Optional[Tuple[str, float, int]]:
    foo = process.extractOne(cpu_name_to_match, cpu_name_list, scorer=fuzz.WRatio)
    print(foo)
    if foo is not None:
        return foo if foo[1] > 88.0 else None
