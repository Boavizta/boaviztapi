from typing import Optional, List

from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends

from boaviztapi import config
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, CloudConfigurationModel
from boaviztapi.model.services.configuration_service import ConfigurationService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.service.sustainability_provider import get_cloud_impact, get_server_impact_on_premise
from boaviztapi.utils.costs_calculator import CostCalculator

sustainability_router = APIRouter(
    prefix='/v1/sustainability',
    tags=['sustainability']
)

def get_scoped_configuration_service(current_user: UserPublicDTO = Depends(get_current_user)) -> ConfigurationService:
    return ConfigurationService(user_id=current_user.sub)

@sustainability_router.get('/on-premise/{id}')
async def get_results_on_premise_configuration(
        configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
        id: str = Depends(validate_id),
        verbose: bool = True,
        costs: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])
):
    server = await configuration_service.get_by_id(id)
    if not server:
        raise HTTPException(status_code=404, detail=f"Configuration with id {id} not found")
    if server.type != 'on-premise':
        raise HTTPException(status_code=400, detail=f"Configuration with id {id} is not an on-premise server")
    try:
        result = await get_server_impact_on_premise(server, verbose, costs, duration, criteria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"An error occurred! Details: {str(e)}")

    return result


@sustainability_router.post('/on-premise')
async def post_results_on_premise_configuration(
        server: OnPremiseConfigurationModel,
        verbose: bool = True,
        costs: bool = True,
        duration: Optional[float] = Query(None),
        criteria: List[str] = Query(config["default_criteria"]),
):
    try:
        final_duration = duration if duration is not None else getattr(server.usage, "lifespan", 1)

        result = await get_server_impact_on_premise(server, verbose, costs, final_duration, criteria)

        calculator = CostCalculator(duration=final_duration)
        cost_results = await calculator.configuration_costs(server)

        if "costs" in result:
            result["costs"].update({
                "total_cost": cost_results.get("total_cost"),
                "breakdown": cost_results.get("breakdown")
            })
        else:
            result["costs"] = cost_results

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"An error occurred! Details: {str(e)}")

    return result

@sustainability_router.get('/cloud/{id}')
async def get_results_cloud_configuration(
        configuration_service: ConfigurationService = Depends(get_scoped_configuration_service),
        current_user: UserPublicDTO = Depends(get_current_user),
        id: str = Depends(validate_id),
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = Query(config["default_criteria"])
):
    cloud_instance = await configuration_service.get_by_id(id)
    if not cloud_instance:
        raise HTTPException(status_code=404, detail=f"Configuration with id {id} not found")
    if cloud_instance.type != 'cloud':
        raise HTTPException(status_code=400, detail=f"Configuration with id {id} is not a cloud instance")
    try:
        result = await get_cloud_impact(cloud_instance, verbose, duration, criteria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"An error occurred! Details: {str(e)}")
    return result


@sustainability_router.post('/cloud')
async def post_results_cloud_configuration(
    cloud_instance: CloudConfigurationModel,
    verbose: bool = True,
    duration: Optional[float] = config["default_duration"],
    criteria: List[str] = Query(config["default_criteria"])
):
    try:
        result = await get_cloud_impact(cloud_instance, verbose, duration, criteria)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"An error occurred! Details: {str(e)}")
    return result

