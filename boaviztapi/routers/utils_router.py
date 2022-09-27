import os

import pandas as pd
from fastapi import APIRouter

from boaviztapi.dto.component.cpu import attributes_from_cpu_name, CPU
from boaviztapi.model.component import ComponentCase, ComponentCPU
from boaviztapi.routers.openapi_doc.descriptions import country_code, cpu_family, cpu_model_range, ssd_manufacturer, \
    ram_manufacturer, case_type, name_to_cpu

utils_router = APIRouter(
    prefix='/v1/utils',
    tags=['utils']
)

data_dir = os.path.join(os.path.dirname(__file__), '../data')
_countries_df = pd.read_csv(os.path.join(data_dir, 'electricity/electricity_impact_factors.csv'))
_cpu_index = pd.read_csv(os.path.join(data_dir, 'components/cpu_index.csv'))
_cpu_manuf = pd.read_csv(os.path.join(data_dir, 'components/cpu_manufacture.csv'))
_ssd_manuf = pd.read_csv(os.path.join(data_dir, 'components/ssd_manufacture.csv'))
_ram_manuf = pd.read_csv(os.path.join(data_dir, 'components/ram_manufacture.csv'))


@utils_router.get('/country_code', description=country_code)
async def utils_get_all_countries():
    res = {}
    for ind in _countries_df.index:
        res[_countries_df["country"][ind]] = _countries_df["code"][ind]

    return res


@utils_router.get('/cpu_family', description=cpu_family)
async def utils_get_all_cpu_family():
    df = _cpu_manuf[_cpu_manuf["family"].notna()]
    return [*df["family"].unique()]


@utils_router.get('/cpu_model_range', description=cpu_model_range)
async def utils_get_all_cpu_model_range():
    df = _cpu_index[_cpu_index["model_range"].notna()]
    return [*df["model_range"].unique()]


@utils_router.get('/ssd_manufacturer', description=ssd_manufacturer)
async def utils_get_all_ssd_manufacturer():
    df = _ssd_manuf[_ssd_manuf["manufacturer"].notna()]

    return [*df["manufacturer"].unique()]


@utils_router.get('/ram_manufacturer', description=ram_manufacturer)
async def utils_get_all_ram_manufacturer():
    df = _ram_manuf[_ram_manuf["manufacturer"].notna()]

    return [*df["manufacturer"].unique()]


@utils_router.get('/case_type', description=case_type)
async def utils_get_all_case_type():
    return ComponentCase.AVAILABLE_CASE_TYPE


@utils_router.get('/name_to_cpu', description=name_to_cpu)
async def name_to_cpu(cpu_name: str = None):
    manufacturer, model_range, family = attributes_from_cpu_name(cpu_name)
    cpu = CPU(manufacturer=manufacturer, model_range=model_range, family=family)
    return cpu
