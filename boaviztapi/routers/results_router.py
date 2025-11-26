from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException

from boaviztapi import config
from boaviztapi.dto.device.device import mapper_server, mapper_cloud_instance
from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, CloudConfigurationModel
from boaviztapi.routers.cloud_router import cloud_instance_impact
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import get_server_archetype, get_cloud_instance_archetype
from boaviztapi.service.results_provider import mapper_config_to_server

results_router = APIRouter(
    prefix='/v1/results',
    tags=['results']
)

@results_router.post('/on-premise')
async def post_results_on_premise_configuration(
        server: OnPremiseConfigurationModel,
        verbose: bool = True,
        costs: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])
):
    archetype_config = get_server_archetype(config["default_server"])

    configured_server = mapper_config_to_server(server)
    completed_server = mapper_server(configured_server, archetype_config)

    return await server_impact(
        device=completed_server,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
        costs=costs
    )

@results_router.post('/cloud')
async def post_results_cloud_configuration(
    cloud_instance: CloudConfigurationModel,
    verbose: bool = True,
    duration: Optional[float] = config["default_duration"],
    criteria: List[str] = Query(config["default_criteria"])
):
    cloud_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.cloud_provider)

    if not cloud_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")

    cloud_model = mapper_config_to_server(cloud_instance)
    instance_model = mapper_cloud_instance(cloud_model, archetype=cloud_archetype)

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria
    )
