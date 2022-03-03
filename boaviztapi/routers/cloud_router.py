import copy
import os

from boaviztapi.model.components.usage import UsageCloud

from fastapi import APIRouter, Query, Body

from boaviztapi.model.devices.device import CloudInstance
from boaviztapi.routers import data_dir
from boaviztapi.routers.openapi_doc.descriptions import cloud_aws_description, all_default_aws_instances
from boaviztapi.routers.openapi_doc.examples import cloud_usage_example
from boaviztapi.service.archetype import complete_with_archetype, get_cloud_instance_archetype, \
    get_device_archetype_lst, known_server_directory
from boaviztapi.service.bottom_up import bottom_up_device
from boaviztapi.service.verbose import verbose_device

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


@cloud_router.post('/aws',
                   description=cloud_aws_description)
def instance_cloud_impact(cloud_usage: UsageCloud = Body(None, example=cloud_usage_example["1"]),
                          instance_type: str = Query(None, example="a1.4xlarge"), verbose: bool = True):
    cloud_instance = CloudInstance()

    cloud_instance.usage = cloud_usage

    # Setting empty config on behalf of the user
    cloud_instance.config_components = []

    completed_instance = copy.deepcopy(cloud_instance)
    instance_archetype = get_cloud_instance_archetype(instance_type, "aws")
    completed_instance = complete_with_archetype(completed_instance, instance_archetype)

    impacts = bottom_up_device(device=completed_instance)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_instance, input_device=cloud_instance)}

    return result


@cloud_router.get('/aws/all_instances',
                  description=all_default_aws_instances)
async def server_get_all_archetype_name():
    return get_device_archetype_lst(os.path.join(data_dir, 'devices/cloud/aws'))
