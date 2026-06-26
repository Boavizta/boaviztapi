import os
from typing import List, Optional

import pandas as pd

from fastapi import APIRouter, Query, Body, HTTPException

from boaviztapi import config, data_dir
from boaviztapi.dto.device import Cloud
from boaviztapi.dto.device.device import mapper_cloud_instance
from boaviztapi.models.services.cloud_instance import ServiceCloudInstance
from boaviztapi.routers.openapi_doc.descriptions import (
    cloud_provider_description,
    all_default_cloud_instances,
    all_default_cloud_providers,
    get_instance_config,
)
from boaviztapi.routers.openapi_doc.examples import cloud_example
from boaviztapi.data.archetype import (
    fuzzy_get_cloud_instance_archetype,
    get_device_archetype_lst,
)
from boaviztapi.compute.impacts_computation import compute_impacts
from boaviztapi.compute.verbose import verbose_cloud

cloud_router = APIRouter(prefix="/v1/cloud", tags=["cloud"])


def _resolve_instance_archetype(instance_type: str, provider: str) -> tuple:
    """
    Returns (archetype, substitution_warning_or_None).
    Raises HTTPException 404 if no match is found even after fuzzy lookup.
    """
    arch, matched = fuzzy_get_cloud_instance_archetype(instance_type, provider)
    if not arch:
        raise HTTPException(
            status_code=404, detail=f"{instance_type} at {provider} not found"
        )
    warning = None
    if matched != instance_type:
        warning = (
            f"Instance '{instance_type}' not found; "
            f"using closest match '{matched}' (fuzzy match)"
        )
    return arch, warning


@cloud_router.get("/instance/instance_config", description=get_instance_config)
async def get_archetype_config(
    provider: str = Query(
        config.default_cloud_provider, examples=[config.default_cloud_provider]
    ),
    instance_type: str = Query(
        config.default_cloud_instance, examples=[config.default_cloud_instance]
    ),
):
    result, _ = _resolve_instance_archetype(instance_type, provider)
    return result


@cloud_router.post("/instance", description=cloud_provider_description)
async def instance_cloud_impact_from_configuration(
    cloud_instance: Cloud = Body(None, examples=[cloud_example]),
    verbose: bool = True,
    duration: Optional[float] = config.default_duration,
    criteria: List[str] = Query(config.default_criteria),
):
    instance_archetype, warning = _resolve_instance_archetype(
        cloud_instance.instance_type, cloud_instance.provider
    )
    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
        warning=warning,
    )


@cloud_router.get("/instance", description=cloud_provider_description)
async def instance_cloud_impact_from_model(
    provider: str = Query(
        config.default_cloud_provider, examples=[config.default_cloud_provider]
    ),
    instance_type: str = Query(
        config.default_cloud_instance, examples=[config.default_cloud_instance]
    ),
    verbose: bool = True,
    duration: Optional[float] = config.default_duration,
    criteria: List[str] = Query(config.default_criteria),
):
    cloud_instance = Cloud()
    cloud_instance.usage = {}
    instance_archetype, warning = _resolve_instance_archetype(instance_type, provider)
    instance_model = mapper_cloud_instance(cloud_instance, archetype=instance_archetype)

    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
        warning=warning,
    )


@cloud_router.get("/instance/all_instances", description=all_default_cloud_instances)
async def server_get_all_archetype_name(provider: str = Query(None, examples=["aws"])):
    if not os.path.exists(data_dir + "/archetypes/cloud/" + provider + ".csv"):
        raise HTTPException(
            status_code=404,
            detail=f"No available data for this cloud provider ({provider})",
        )
    return get_device_archetype_lst(
        os.path.join(data_dir, "archetypes/cloud/" + provider + ".csv")
    )


@cloud_router.get("/instance/all_providers", description=all_default_cloud_providers)
async def server_get_all_provider_name():
    df = pd.read_csv(os.path.join(data_dir, "archetypes/cloud/providers.csv"))
    return df["provider.name"].tolist()


async def cloud_instance_impact(
    cloud_instance: ServiceCloudInstance,
    verbose: bool,
    duration: Optional[float] = config.default_duration,
    criteria: List[str] = Query(config.default_criteria),
    warning: Optional[str] = None,
) -> dict:
    if duration is None:
        duration = cloud_instance.platform.usage.hours_life_time.value

    impacts = compute_impacts(
        model=cloud_instance, selected_criteria=criteria, duration=duration
    )

    result: dict = {"impacts": impacts}
    if verbose:
        result["verbose"] = verbose_cloud(
            cloud_instance, selected_criteria=criteria, duration=duration
        )
    if warning:
        result["warnings"] = [warning]
    return result
