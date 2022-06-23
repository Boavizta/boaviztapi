import copy
import os

from fastapi import APIRouter, Query, Body

from boaviztapi.dto.device import Cloud
from boaviztapi.dto.device.device import smart_complete_server
from boaviztapi.model.device import DeviceCloudInstance
from boaviztapi.routers import data_dir
from boaviztapi.routers.openapi_doc.descriptions import cloud_aws_description, all_default_aws_instances
from boaviztapi.routers.openapi_doc.examples import cloud_usage_example
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import complete_with_archetype, get_cloud_instance_archetype, \
    get_device_archetype_lst
from boaviztapi.service.bottom_up import bottom_up_device
from boaviztapi.service.verbose import verbose_device
from boaviztapi.dto.usage import UsageCloud

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


@cloud_router.post('/aws',
                   description=cloud_aws_description)
async def instance_cloud_impact(cloud_usage: UsageCloud = Body(None, example=cloud_usage_example["1"]),
                                instance_type: str = Query(None, example="a1.4xlarge"), verbose: bool = True):
    cloud_instance = Cloud()
    cloud_instance.usage = cloud_usage
    completed_instance = copy.deepcopy(cloud_instance)

    instance_archetype = await get_cloud_instance_archetype(instance_type, "aws")
    if instance_archetype:
        completed_instance = Cloud(**complete_with_archetype(completed_instance, instance_archetype))
        completed_instance = smart_complete_server(completed_instance)

        return await server_impact(
            input_device_dto=cloud_instance,
            smart_complete_device_dto=completed_instance,
            device_class=DeviceCloudInstance,
            verbose=verbose
        )
    return {f'{instance_type} is not referenced has an aws instance'}


@cloud_router.get('/aws/all_instances',
                  description=all_default_aws_instances)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/cloud/aws'))
