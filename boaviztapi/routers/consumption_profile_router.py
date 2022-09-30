from fastapi import APIRouter, Body

from boaviztapi.dto.consumption_profile import ConsumptionProfileCPU
from boaviztapi.dto.consumption_profile.consumption_profile import mapper_cp_cpu
from boaviztapi.routers.openapi_doc.examples import cpu_consumption_profiles

consumption_profile = APIRouter(
    prefix='/v1/consumption_profile',
    tags=['consumption_profile']
)


@consumption_profile.post('/cpu',
                          description="cpu consumption profile generator")
async def cpu_consumption_profile(cp_dto: ConsumptionProfileCPU = Body(None, example=cpu_consumption_profiles),
                                  verbose: bool = True):
    cp, cpu = mapper_cp_cpu(cp_dto)
    result = cp.compute_consumption_profile_model(cpu_manufacturer=cpu.manufacturer.value,
                                                  cpu_model_range=cpu.model_range.value,
                                                  cpu_tdp=cpu.tdp.value)
    return result
