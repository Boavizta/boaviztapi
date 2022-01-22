import copy

from boaviztapi.model.components.usage import UsageCloud

from fastapi import APIRouter

from boaviztapi.model.devices.device import CloudInstance
from boaviztapi.service.archetype import complete_with_archetype, get_cloud_instance_archetype
from boaviztapi.service.bottom_up import bottom_up_device
from boaviztapi.service.verbose import verbose_device

cloud_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


@cloud_router.post('/aws',
                   description="Get the impact of an AWS instance by the model name given in parameter")
def instance_cloud_impact(cloud_usage: UsageCloud, instance_type: str = True, verbose: bool = True):
    cloud_instance = CloudInstance()
    cloud_instance.usage = cloud_usage

    completed_instance = copy.deepcopy(cloud_instance)
    instance_archetype = get_cloud_instance_archetype(instance_type, "aws")
    print(instance_archetype)
    completed_instance = complete_with_archetype(completed_instance, instance_archetype)

    impacts = bottom_up_device(device=completed_instance)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_instance, input_device=cloud_instance)}

    return result
