from fastapi import APIRouter, status, Response, Depends

from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, CloudConfigurationModel
from boaviztapi.service.cloud_provider import get_cloud_providers
from boaviztapi.service.wizard_service import strategy_lift_shift

wizard_router = APIRouter(
    prefix='/v1/wizard',
    tags=['wizard']
)

def _validate_provider(provider_name: str) -> str:
    cloud_providers = [p.strip().lower() for p in get_cloud_providers()]
    if provider_name not in cloud_providers:
        raise ValueError(f"Provider {provider_name} not found. Available providers: {cloud_providers}")
    return provider_name


@wizard_router.post('/lift-shift',
                    description="Get a cloud configuration with similar performance to your on-premise configuration",
                    response_model=CloudConfigurationModel,
                    response_model_exclude={'id'})
async def get_lift_shift_strategy(
        on_premise_config: OnPremiseConfigurationModel,
        provider: str = Depends(_validate_provider)
):
    return strategy_lift_shift(on_premise_config, provider)

@wizard_router.post('/greener-region',
                    description="Get a cloud configuration with less CO2 emissions and possibly better energy costs",
                    response_model=CloudConfigurationModel)
async def get_greener_region_strategy(
        cloud_config: CloudConfigurationModel
):
    return Response(status_code=status.HTTP_200_OK, content="TODO")

@wizard_router.post('/rightsizing',
                    description="Optimise your given cloud configuration to reduce costs and improve efficiency",
                    response_model=CloudConfigurationModel)
async def get_rightsizing_strategy(
        cloud_config: CloudConfigurationModel
):
    return Response(status_code=status.HTTP_200_OK, content="TODO")