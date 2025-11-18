from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends

from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.model.crud_models.portfolio_model import ExtendedPortfolioModel
from boaviztapi.model.services.configuration_service import ConfigurationService
from boaviztapi.model.services.portfolio_service import PortfolioService
from boaviztapi.service.auth.dependencies import get_current_user

user_router = APIRouter(
    prefix='/v1/user',
    tags=['user'],
    dependencies=[Depends(get_current_user)]
)

@user_router.get("/configurations")
async def get_user_configurations(current_user: UserPublicDTO = Depends(get_current_user), configuration_service: ConfigurationService = Depends(ConfigurationService.get_crud_service)):
    if (
        configurations := await configuration_service.get_all_by_filter(filter={"user_id": current_user.sub})
    ) is not None:
        return configurations
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No configurations were found for the given user id {current_user.sub}")

@user_router.get("/portfolios")
async def get_user_portfolios(current_user: UserPublicDTO = Depends(get_current_user), portfolio_service: PortfolioService = Depends(PortfolioService.get_crud_service)):
    pipeline = [
            {
                "$match": {"user_id": current_user.sub}
            },
            {
                "$lookup": {
                    "from": "configurations",
                    "let": {"config_ids": "$configuration_ids"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {
                                    "$in": [
                                        {"$toString": "$_id"},  # convert ObjectId -> string
                                        "$$config_ids"  # compare against portfolio strings
                                    ]
                                }
                            }
                        }
                    ],
                    "as": "configurations"
                }
            }
        ]
    collection = portfolio_service.get_mongo_collection()
    aggCursor = await collection.aggregate(pipeline)
    results = await aggCursor.to_list(length=None)
    return [ExtendedPortfolioModel(**doc) for doc in results]
