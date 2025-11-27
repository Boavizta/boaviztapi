from fastapi import APIRouter, Body, status
from fastapi.params import Depends

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.configuration_model import ConfigurationModel, ConfigurationCollection
from boaviztapi.model.services.configuration_service import ConfigurationService
from boaviztapi.routers.pydantic_based_router import validate_id
from boaviztapi.service.auth.dependencies import get_current_user

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
async def create_configuration(configuration: ConfigurationModel = Body(...), service: ConfigurationService = Depends(get_scoped_configuration_service)):
    """
    Insert a new configuration record.

    A unique `id` will be created and provided in the response.
    """
    return await service.create(configuration)


@configuration_router.get("/",
                          response_description="List all configurations",
                          response_model=ConfigurationCollection,
                          response_model_by_alias=False,
                          )
async def list_configurations(service: ConfigurationService = Depends(get_scoped_configuration_service)):
    return await service.get_all()

@configuration_router.get("/{id}",
                          response_description="Get a single configuration",
                          response_model=ConfigurationModel,
                          response_model_by_alias=False,
                          )
async def find_configuration(id: str = Depends(validate_id), service: ConfigurationService = Depends(get_scoped_configuration_service)):
    return await service.get_by_id(id)

@configuration_router.put(
    "/{id}",
    response_description="Update a configuration",
    response_model=ConfigurationModel,
    response_model_by_alias=False,
)
async def update_configuration(id: str = Depends(validate_id), configuration: ConfigurationModel = Body(...), service: ConfigurationService = Depends(get_scoped_configuration_service)):
    return await service.update(id, configuration)


@configuration_router.delete("/{id}", response_description="Delete a configuration")
async def delete_configuration(id: str = Depends(validate_id), service: ConfigurationService = Depends(get_scoped_configuration_service)):
    return await service.delete(id)

