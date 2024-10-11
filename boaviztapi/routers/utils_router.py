import os

import pandas as pd
import toml
from fastapi import APIRouter, Query

from boaviztapi.dto.component.cpu import CPU
from boaviztapi.model import impact
from boaviztapi.model.component import ComponentCase
from boaviztapi.model.component.cpu import attributes_from_cpu_name
from boaviztapi.routers.openapi_doc.descriptions import country_code, cpu_family, cpu_model_range, ssd_manufacturer, \
    ram_manufacturer, case_type, name_to_cpu, cpu_names, impacts_criteria
from boaviztapi.service.factor_provider import get_available_countries

utils_router = APIRouter(
    prefix='/v1/utils',
    tags=['utils']
)

data_dir = os.path.join(os.path.dirname(__file__), '../data')
_cpu_specs = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/cpu_specs.csv'))
_ssd_manuf = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/ssd_manufacture.csv'))
_ram_manuf = pd.read_csv(os.path.join(data_dir, 'crowdsourcing/ram_manufacture.csv'))



@utils_router.get('/version', description="Get the version of the API")
async def version():
    return toml.loads(open(os.path.join(os.path.dirname(__file__), '../../pyproject.toml'), 'r').read())['tool']['poetry'][
    'version']

@utils_router.get('/country_code', description=country_code)
async def utils_get_all_countries():
    return get_available_countries()


@utils_router.get('/cpu_family', description=cpu_family)
async def utils_get_all_cpu_family():
    df = _cpu_specs[_cpu_specs["code_name"].notna()]
    return [*df["code_name"].unique()]


@utils_router.get('/cpu_model_range', description=cpu_model_range)
async def utils_get_all_cpu_model_range():
    df = _cpu_specs[_cpu_specs["model_range"].notna()]
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
async def name_to_cpu(cpu_name: str = Query(example="Intel Core i7-9700K")):
    cpu_attributes = attributes_from_cpu_name(cpu_name)
    if cpu_attributes is not None:
        name, manufacturer, code_name, model_range, tdp, cores, threads, die_size, die_size_source, source = cpu_attributes
        return CPU(family=code_name, name=name, tdp=tdp, core_units=cores, die_size=die_size, model_range=model_range,
                   manufacturer=manufacturer)
    else:
        return f"CPU name {cpu_name} is not found in our database"

@utils_router.get('/cpu_name', description=cpu_names)
async def utils_get_all_cpu_name():
    df = _cpu_specs[_cpu_specs["name"].notna()]
    return [*df["name"].unique()]


@utils_router.get('/impact_criteria', description=impacts_criteria)
async def utils_get_all_impacts_criteria():
    return impact.IMPACT_CRITERIAS
