from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends

from boaviztapi import config
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.dto.device.device import mapper_server, mapper_cloud_instance
from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, CloudConfigurationModel
from boaviztapi.routers.cloud_router import cloud_instance_impact
from boaviztapi.routers.configuration_router import get_scoped_configuration_service
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import get_server_archetype, get_cloud_instance_archetype
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.results_provider import mapper_config_to_server

sustainability_router = APIRouter(
    prefix='/v1/sustainability',
    tags=['sustainability']
)

@sustainability_router.get('/on-premise/{id}')
async def get_results_on_premise_configuration(
        current_user: UserPublicDTO = Depends(get_current_user),
        id: str = Depends(validate_id),
        verbose: bool = True,
        costs: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])
):
    archetype_config = get_server_archetype(config["default_server"])
    configuration_service = get_scoped_configuration_service(current_user)

    server = await configuration_service.get_by_id(id)
    if not server:
        raise HTTPException(status_code=404, detail=f"Configuration with id {id} not found")
    if server.type != 'on-premise':
        raise HTTPException(status_code=400, detail=f"Configuration with id {id} is not an on-premise server")
    configured_server = mapper_config_to_server(server)
    completed_server = mapper_server(configured_server, archetype_config)
    if not completed_server:
        raise HTTPException(status_code=400, detail="Could not compute the sustainability impact of the server")
    return await server_impact(
        device=completed_server,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
        costs=costs,
        location=server.usage.localisation
    )

@sustainability_router.post('/on-premise')
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
        costs=costs,
        location=server.usage.localisation
    )

@sustainability_router.get('/cloud/{id}')
async def get_results_cloud_configuration(
        current_user: UserPublicDTO = Depends(get_current_user),
        id: str = Depends(validate_id),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])
):
    configuration_service = get_scoped_configuration_service(current_user)

    cloud_instance = await configuration_service.get_by_id(id)
    if not cloud_instance:
        raise HTTPException(status_code=404, detail=f"Configuration with id {id} not found")
    if cloud_instance.type != 'cloud':
        raise HTTPException(status_code=400, detail=f"Configuration with id {id} is not a cloud instance")
    cloud_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.cloud_provider)
    if not cloud_archetype:
        raise HTTPException(status_code=404,
                            detail=f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")
    cloud_model = mapper_config_to_server(cloud_instance)
    instance_model = mapper_cloud_instance(cloud_model, archetype=cloud_archetype)
    if not instance_model:
        raise HTTPException(status_code=400, detail="Could not compute the sustainability impact of the cloud instance")

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
    )

@sustainability_router.post('/cloud')
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

