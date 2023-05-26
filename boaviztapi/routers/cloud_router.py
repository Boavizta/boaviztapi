import os
from typing import List, Union, Optional

import pandas as pd

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device import Cloud
from boaviztapi.dto.device.device import mapper_cloud_instance
from boaviztapi.routers.openapi_doc.descriptions import cloud_provider_description, all_default_cloud_instances, \
    all_default_cloud_providers,get_instance_config
from boaviztapi.routers.openapi_doc.examples import cloud_example
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import get_cloud_instance_archetype, get_device_archetype_lst

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)

@cloud_router.get('/instance/instance_config',
                   description=get_instance_config)
async def get_archetype_config(provider: str = Query(config["default_cloud_provider"], example=config["default_cloud_provider"]),
                               instance_type: str = Query(config["default_cloud"], example=config["default_cloud"])):

    result = get_cloud_instance_archetype(instance_type, provider)
    if not result:
        raise HTTPException(status_code=404, detail=f"{instance_type} at {provider} not found")
    return result

@cloud_router.post('/instance',
                   description=cloud_provider_description)
async def instance_cloud_impact(cloud_instance: Cloud = Body(None, example=cloud_example),
                                verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])):
    instance_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.provider)

    if not instance_archetype:
        raise HTTPException(status_code=404, detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")

    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await server_impact(
        device=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )

@cloud_router.get('/instance',
                   description=cloud_provider_description)
async def instance_cloud_impact(provider: str = Query(config["default_cloud_provider"], example=config["default_cloud_provider"]),
                                instance_type: str = Query(config["default_cloud"], example=config["default_cloud"]), verbose: bool = True,
                                duration: Optional[float] = config["default_duration"],
                                criteria: List[str] = Query(config["default_criteria"])):
    cloud_instance = Cloud()
    cloud_instance.usage = {}
    instance_archetype = get_cloud_instance_archetype(instance_type, provider)

    if not instance_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")

    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await server_impact(
        device=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )

@cloud_router.get('/instance/all_instances',
                  description=all_default_cloud_instances)
async def server_get_all_archetype_name(provider: str = Query(None, example="aws")):
    if not os.path.exists(data_dir +'/archetypes/cloud/' + provider + '.csv'):
        raise HTTPException(status_code=404, detail=f"No available data for this cloud provider ({provider})")
    return get_device_archetype_lst(os.path.join(data_dir, 'archetypes/cloud/' + provider + '.csv'))

@cloud_router.get('/instance/all_providers',
                  description=all_default_cloud_providers)
async def server_get_all_provider_name():
    df = pd.read_csv(os.path.join(data_dir, 'archetypes/cloud/providers.csv'))
    return df['provider.name'].tolist()