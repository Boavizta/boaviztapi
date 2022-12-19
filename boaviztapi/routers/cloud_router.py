import copy
import os
import pandas as pd

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi.dto.device import Cloud
from boaviztapi.dto.device.device import smart_mapper_server, mapper_cloud_instance
from boaviztapi.dto.usage import UsageCloud
from boaviztapi.model.device import DeviceCloudInstance
from boaviztapi.routers import data_dir
from boaviztapi.routers.openapi_doc.descriptions import cloud_provider_description, all_default_cloud_instances, all_default_cloud_providers, cloud_aws_description, all_default_aws_instances
from boaviztapi.routers.openapi_doc.examples import cloud_usage_example, cloud_example
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.allocation import Allocation
from boaviztapi.service.archetype import complete_with_archetype, get_cloud_instance_archetype, \
    get_device_archetype_lst

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


@cloud_router.post('/aws',
                   description=cloud_aws_description)
async def legacy_instance_cloud_impact(cloud_usage: UsageCloud = Body(None, example=cloud_usage_example),
                                instance_type: str = Query(None, example="a1.4xlarge"), verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):
    cloud_instance = Cloud()
    cloud_instance.usage = cloud_usage
    instance_archetype = await get_cloud_instance_archetype(instance_type, "aws")

    if not instance_archetype:
        raise HTTPException(status_code=404, detail=f"{instance_type} not found")

    instance_archetype = Cloud(**complete_with_archetype(cloud_instance, instance_archetype))
    instance_model = mapper_cloud_instance(instance_archetype)

    return await server_impact(
        device=instance_model,
        verbose=verbose,
        allocation=allocation
    )


@cloud_router.get('/aws/all_instances',
                  description=all_default_aws_instances)
async def legacy_server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/cloud/aws.csv'))

@cloud_router.post('/',
                   description=cloud_provider_description)
async def instance_cloud_impact(cloud_instance: Cloud = Body(None, example=cloud_example),
                                verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):
    instance_archetype = await get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.provider)

    if not instance_archetype:
        raise HTTPException(status_code=404, detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")

    instance_archetype = Cloud(**complete_with_archetype(cloud_instance, instance_archetype))
    instance_model = mapper_cloud_instance(instance_archetype)

    return await server_impact(
        device=instance_model,
        verbose=verbose,
        allocation=allocation
    )

@cloud_router.get('/',
                   description=cloud_provider_description)
async def instance_cloud_impact(provider: str = Query(None, example="aws"),
                                instance_type: str = Query(None, example="a1.4xlarge"), verbose: bool = True,
                                allocation: Allocation = Allocation.TOTAL):
    cloud_instance = Cloud()
    cloud_instance.usage = {}
    instance_archetype = await get_cloud_instance_archetype(instance_type, provider)

    if not instance_archetype:
        raise HTTPException(status_code=404, detail=f"{instance_type} at {provider} not found")

    instance_archetype = Cloud(**complete_with_archetype(cloud_instance, instance_archetype))
    instance_model = mapper_cloud_instance(instance_archetype)

    return await server_impact(
        device=instance_model,
        verbose=verbose,
        allocation=allocation
    )

@cloud_router.get('/all_instances',
                  description=all_default_cloud_instances)
async def server_get_all_archetype_name(cloud_provider: str = Query(None, example="aws")):
    if not os.path.exists(data_dir+'/devices/cloud/'+cloud_provider+'.csv'):
        print(data_dir+'devices/cloud/'+cloud_provider+'.csv')
        raise HTTPException(status_code=404, detail=f"No available data for this cloud provider ({cloud_provider})")
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/cloud/'+cloud_provider+'.csv'))

@cloud_router.get('/all_providers',
                  description=all_default_cloud_providers)
async def server_get_all_provider_name():
    df = pd.read_csv(os.path.join(data_dir, 'devices/cloud/providers.csv'))
    return df['provider.name'].tolist()