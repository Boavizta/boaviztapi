from typing import Dict, List, Any

from fastapi import APIRouter, Body, status, HTTPException
from fastapi.params import Depends, Query

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.basemodel import PyObjectId
from boaviztapi.model.crud_models.configuration_model import ConfigurationModel, ConfigurationCollection, \
    ConfigurationWithResultsCollection, ConfigurationModelWithResults
from boaviztapi.model.services.configuration_service import ConfigurationService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.sustainability_provider import add_results_to_configuration
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.utils.costs_calculator import CostCalculator

configuration_router = APIRouter(
    prefix='/v1/configurations',
    tags=['configuration'],
    dependencies=[Depends(get_current_user)]
)

def get_scoped_configuration_service(current_user: UserPublicDTO = Depends(get_current_user)) -> ConfigurationService:
    return ConfigurationService(user_id=current_user.sub)

@configuration_router.post("/",
                           response_description="Add a new configuration",
                           response_model=ConfigurationModel,
                           status_code=status.HTTP_201_CREATED,
                           response_model_by_alias=False,
                           )
async def create_configuration(configuration: ConfigurationModel = Body(...), service: ConfigurationService = Depends(
    get_scoped_configuration_service)):
    """
    Insert a new configuration record.

    A unique `id` will be created and provided in the response.
    """
    return await service.create(configuration)


@configuration_router.get(
    "/",
    response_description="List all configurations",
    response_model=ConfigurationWithResultsCollection,
    response_model_by_alias=False,
)
async def list_configurations(
        service: ConfigurationService = Depends(get_scoped_configuration_service),
        impacts: bool = False,
        costs: bool = False
):
    items = await service.get_all()
    extended_configs = [ConfigurationModelWithResults(results={}, configuration=config) for config in items.items]

    if impacts:
        for wrapper in extended_configs:
            wrapper.results = await add_results_to_configuration(wrapper)

    if costs:
        for wrapper in extended_configs:
            duration = getattr(wrapper.configuration.usage, "lifespan", 1)
            calculator = CostCalculator(duration=duration)
            wrapper.results['costs'] = await calculator.configuration_costs(wrapper.configuration)

    return ConfigurationWithResultsCollection(items=extended_configs)

# @configuration_router.get(
#     "/with-results",
#     response_description="List all configurations with their sustainability and cost results",
#     response_model=ConfigurationWithResultsCollection,
#     response_model_by_alias=False,
# )
# async def list_configurations_with_results(
#     service: ConfigurationService = Depends(get_scoped_configuration_service),
#     costs: bool = False,
#     impacts: bool = False
# ):
#     items = await service.get_all()
#     extended_configs = []
#
#     for config in items.items:
#         config_with_results = await add_results_to_configuration(config)
#
#         duration = getattr(config.usage, "lifespan", 1)
#         calculator = CostCalculator(duration=duration)
#         cost_results = await calculator.configuration_costs(config)
#
#         config_with_results.configuration.costs = cost_results
#
#         extended_configs.append(config_with_results)
#
#     return ConfigurationWithResultsCollection(items=extended_configs)
@configuration_router.get("/{id}",
                          response_description="Get a single configuration",
                          response_model=ConfigurationModelWithResults,
                          response_model_by_alias=False,
                          )
async def find_configuration(
    id: str = Depends(validate_id),
    service: ConfigurationService = Depends(get_scoped_configuration_service),
    impacts: bool = False,
    costs: bool = False
):
    config = await service.get_by_id(id)
    if not config:
        raise HTTPException(404, f"Configuration with id {id} not found")

    wrapper = ConfigurationModelWithResults(results={}, configuration=config)

    if impacts:
        wrapper.results = await add_results_to_configuration(wrapper)

    if costs:
        duration = getattr(wrapper.configuration.usage, "lifespan", 1)
        calculator = CostCalculator(duration=duration)
        wrapper.results["costs"] = await calculator.configuration_costs(wrapper.configuration)

    return wrapper

@configuration_router.put(
    "/{id}",
    response_description="Update a configuration",
    response_model=ConfigurationModel,
    response_model_by_alias=False,
)
async def update_configuration(id: str = Depends(validate_id), configuration: ConfigurationModel = Body(...), service: ConfigurationService = Depends(
    get_scoped_configuration_service)):
    return await service.update(id, configuration)


@configuration_router.delete("/{id}", response_description="Delete a configuration")
async def delete_configuration(id: str = Depends(validate_id), service: ConfigurationService = Depends(
    get_scoped_configuration_service)):
    return await service.delete(id)
