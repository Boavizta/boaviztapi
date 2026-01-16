import random

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

import boaviztapi.service.cloud_provider as cloud_provider
import boaviztapi.service.utils_provider as utils_provider
from boaviztapi import config
from boaviztapi.service.electricity_maps.costs_provider import ElectricityCostsProvider

options_router = APIRouter(
    prefix='/v1/options',
    tags=['options']
)


@options_router.get('/onprem/configuration', description="Return the available configuration options for on-premise server configuration form inputs")
@cache(expire=60 * 60 * 24) # 1 day
async def get_onprem_server_configuration():
    response = dict()
    response["cpu_architectures"] = utils_provider.get_all_cpu_family()
    response["ram_manufacturers"] = utils_provider.get_all_ram_manufacturer()
    response["ssd_manufacturers"] = utils_provider.get_all_ssd_manufacturer()
    response["server_types"] = utils_provider.get_all_case_type()
    return response


@options_router.get('/cloud/configuration', description="Return the available configuration options for cloud instance configuration form inputs")
@cache(expire=60 * 60 * 24)
async def get_cloud_instance_configuration():
    response = dict()
    response["cloud_providers"] = cloud_provider.get_cloud_providers()
    response["instance_types"] = cloud_provider.get_cloud_instance_types_for_all_providers()
    return response


@options_router.get('/cloud/usage', description="Return the available configuration options for cloud instance usage form inputs")
@cache(expire=60 * 60 * 24)
async def get_cloud_instance_usage(
        provider: str = Query(config["default_cloud_provider"], example=config["default_cloud_provider"]),
        instance_type: str = Query(config["default_cloud_instance"], example=config["default_cloud_instance"])):
    response = dict()
    # TODO: Add instance pricing types to the vantage API scraper
    response["details"] = "WARNING: THIS DATA IS SYNTHETICALLY GENERATED FOR MOCK-UP PURPOSES."
    response["instance_pricing_types"] = _get_synthetic_costs()
    return response


@options_router.get('/localisation', description="Return the available locations for electricity cost estimation")
@cache(expire=60 * 60 * 24)
async def get_localisations(provider: str | None = None, instance_type: str | None = None,):
    if provider and instance_type:
        return ElectricityCostsProvider.get_eic_countries_for_instance(
            provider=provider,
            instance_type=instance_type,
        )
    return ElectricityCostsProvider.get_eic_countries()


def _get_synthetic_costs():
    """
    Generate synthetic costs for the cloud instance usage endpoint

    Can return None for (Unavailable Vantage) or a random price.
    """
    costs = dict()
    costs["linux_reserved"] = random.choice([None, _get_random_price()])
    costs["linux_spot_minimum"] = random.choice([None, _get_random_price()])
    costs["windows_on_demand"] = random.choice([None, _get_random_price()])
    costs["windows_reserved"] = random.choice([None, _get_random_price()])
    return costs


def _get_random_price() -> float:
    """ Get a random price between 0 and 10"""
    return round(random.random() * random.randint(1, 10), 4)
