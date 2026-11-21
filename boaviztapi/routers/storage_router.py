from typing import List, Optional

from fastapi import APIRouter, Body, Query

from boaviztapi import config
from boaviztapi.compute.impacts_computation import compute_impacts
from boaviztapi.compute.verbose import verbose_storage
from boaviztapi.dto.storage import Storage, mapper_storage
from boaviztapi.routers.openapi_doc.descriptions import storage_description
from boaviztapi.routers.openapi_doc.examples import storage_example

storage_router = APIRouter(prefix="/v1/storage", tags=["storage"])


@storage_router.post("/", description=storage_description)
async def storage_impact_from_configuration(
    storage: Storage = Body(..., examples=[storage_example]),
    verbose: bool = True,
    duration: Optional[float] = config.default_duration,
    criteria: List[str] = Query(config.default_criteria),
):
    model = mapper_storage(storage)
    if duration is None:
        duration = model.usage.hours_life_time.value

    result: dict = {
        "impacts": compute_impacts(
            model=model, selected_criteria=criteria, duration=duration
        )
    }
    if verbose:
        result["verbose"] = verbose_storage(model, duration=duration)
    return result
