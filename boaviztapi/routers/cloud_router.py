import os
from typing import List, Optional

import pandas as pd

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device import CloudInstance
from boaviztapi.dto.device.device import CloudPlatform, mapper_cloud_instance, mapper_cloud_platform
from boaviztapi.model.services.cloud_instance import ServiceCloudInstance
from boaviztapi.model.services.cloud_platform import ServiceCloudPlatform
from boaviztapi.routers.openapi_doc.descriptions import cloud_instance_description, get_platform_config_desc, cloud_platform_description, all_default_cloud_instances, \
    all_default_cloud_providers, all_default_cloud_platforms, get_instance_config
from boaviztapi.routers.openapi_doc.examples import cloud_example, platform_example
from boaviztapi.service.archetype import get_cloud_instance_archetype, get_cloud_platform_archetype, get_device_archetype_lst
from boaviztapi.service.impacts_computation import compute_impacts
from boaviztapi.service.verbose import verbose_device, verbose_cloud

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


@cloud_router.get('/instance/instance_config',
                  description=get_instance_config)
async def get_instance_config(
        provider: str = Query(config["default_cloud_provider"], example=config["default_cloud_provider"]),
        instance_type: str = Query(config["default_cloud_instance"], example=config["default_cloud_instance"])):
    result = get_cloud_instance_archetype(instance_type, provider)
    if not result:
        raise HTTPException(status_code=404, detail=f"{instance_type} at {provider} not found")
    return result


@cloud_router.post('/instance',
                   description=cloud_instance_description)
async def instance_cloud_impact(cloud_instance: CloudInstance = Body(None, example=cloud_example),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])):
    instance_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.provider)

    if not instance_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")

    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@cloud_router.get('/instance',
                  description=cloud_instance_description)
async def instance_cloud_impact(
        provider: str = Query(config["default_cloud_provider"], example=config["default_cloud_provider"]),
        instance_type: str = Query(config["default_cloud_instance"], example=config["default_cloud_instance"]),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])):

    cloud_instance = CloudInstance()
    cloud_instance.usage = {}
    instance_archetype = get_cloud_instance_archetype(instance_type, provider)

    if not instance_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{instance_type} at {provider} not found")

    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )


@cloud_router.get('/instance/all_instances',
                  description=all_default_cloud_instances)
async def server_get_all_archetype_name(provider: str = Query(None, example="aws")):
    if not os.path.exists(data_dir + '/archetypes/cloud_instance/' + provider + '.csv'):
        raise HTTPException(status_code=404, detail=f"No available data for this cloud provider ({provider})")
    return get_device_archetype_lst(os.path.join(data_dir, 'archetypes/cloud_instance/' + provider + '.csv'))


@cloud_router.get('/instance/all_providers',
                  description=all_default_cloud_providers)
async def server_get_all_provider_name():
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/cloud_instance/providers.csv'))
    return df['provider.name'].tolist()


async def cloud_instance_impact(cloud_instance: ServiceCloudInstance,
                                verbose: bool,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])) -> dict:
    if duration is None:
        duration = cloud_instance.platform.usage.hours_life_time.value

    impacts = compute_impacts(model=cloud_instance, selected_criteria=criteria, duration=duration)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_cloud(cloud_instance, selected_criteria=criteria, duration=duration)
        }
    return {"impacts": impacts}


@cloud_router.get('/platform/platform_config',
                  description=get_platform_config_desc)
async def get_platform_config(
        provider: str = Query(config["default_platform_provider"], example=config["default_platform_provider"]),
        platform_type: str = Query(config["default_platform_type"], example=config["default_platform_type"])):
    result = get_cloud_platform_archetype(platform_type, provider)
    if not result:
        raise HTTPException(status_code=404, detail=f"{platform_type} at {provider} not found")
    return result


@cloud_router.post('/platform',
                   description=cloud_platform_description)
async def platform_impact(platform: CloudPlatform = Body(None, example=platform_example),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])):
    platform_archetype = get_cloud_platform_archetype(archetype_name=platform.platform_type, provider=platform.provider)

    if not platform_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{platform.platform_type} at {platform.provider} not found")

    platform_model = mapper_cloud_platform(platform_dto=platform, archetype=platform_archetype)

    t = await cloud_platform_impact(
        cloud_platform=platform_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )
    return t


@cloud_router.get('/platform/all_platforms',
                  description=all_default_cloud_platforms)
async def get_all_platforms_name(provider: str = Query(None, example="scaleway")):
    if not os.path.exists(data_dir + '/archetypes/cloud_platform/' + provider + '.csv'):
        raise HTTPException(status_code=404, detail=f"No available data for this cloud provider ({provider})")
    return get_device_archetype_lst(os.path.join(data_dir, 'archetypes/cloud_platform/' + provider + '.csv'))


@cloud_router.get('/platform/all_providers',
                  description=all_default_cloud_providers)
async def get_all_provider_name():
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/cloud_instance/providers.csv'))
    return df['provider.name'].tolist()

async def cloud_platform_impact(cloud_platform: ServiceCloudPlatform,
                                verbose: bool,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])) -> dict:
    if duration is None:
        duration = cloud_platform.server.usage.hours_life_time.value

    impacts = compute_impacts(model=cloud_platform, selected_criteria=criteria, duration=duration)

    if verbose:
        return {
            "impacts": impacts,
            "verbose": verbose_cloud(cloud_platform, selected_criteria=criteria, duration=duration)
        }
    return {"impacts": impacts}