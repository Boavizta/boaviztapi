from fastapi import APIRouter, Body

from boaviztapi.dto.consumption_profile import ConsumptionProfileCPU

consumption_profile = APIRouter(
    prefix='/v1/consumption_profile',
    tags=['consumption_profile']
)


@consumption_profile.post('/cpu',
                          description="cpu consumption profile generator")
async def cpu_consumption_profile(cpu: ConsumptionProfileCPU = Body(None),
                                  verbose: bool = True):
    pass
