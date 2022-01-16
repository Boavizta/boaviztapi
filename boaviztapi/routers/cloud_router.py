import copy
from boaviztapi.model.components.usage import UsageCloud

from fastapi import APIRouter


server_router = APIRouter(
    prefix='/v1/cloud',
    tags=['cloud']
)


# Grosse fiesta
"""
Usage_Cloud
CloudDTO                                                                                ->  Server -> Impact
avoir des fichiers .json de config aws dans la racine /data/devices/cloud/aws/.


@cloud_router.post('/aws',
                    description="Get the impact of a server of AWS by the model name given in parameter")
def cloud_impact_server(cloud_server :CloudDTO, verbose: bool = True):
    server = get_server_cloud(cloud_DTO)
    completed_server = copy.deepcopy(server)

    impacts = bottom_up_device(device=completed_server)
    result = impacts

    if verbose:
        result = {"impacts": impacts,
                  "verbose": verbose_device(complete_device=completed_server, input_device=server)}

    return result

"""
