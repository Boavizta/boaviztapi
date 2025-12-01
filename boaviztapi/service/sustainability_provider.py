from typing import Optional, List

from pydantic import TypeAdapter

from boaviztapi import config
from boaviztapi.dto.device.device import mapper_cloud_instance, mapper_server
from boaviztapi.model.crud_models.configuration_model import CloudConfigurationModel, OnPremiseConfigurationModel, \
    ConfigurationModel, ConfigurationModelWithResults
from boaviztapi.routers.cloud_router import cloud_instance_impact
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import get_cloud_instance_archetype, get_server_archetype
from boaviztapi.service.results_provider import mapper_config_to_server


async def get_cloud_impact(
        cloud_instance: CloudConfigurationModel,
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = config["default_criteria"]):
    cloud_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_instance.cloud_provider)
    if not cloud_archetype:
        raise ValueError(f"{cloud_instance.instance_type} at {cloud_instance.provider} not found")
    cloud_model = mapper_config_to_server(cloud_instance)
    instance_model = mapper_cloud_instance(cloud_model, archetype=cloud_archetype)
    return await cloud_instance_impact(
        cloud_instance=instance_model,
        verbose=verbose,
        duration=duration,
        criteria=criteria,
    )


async def get_server_impact_on_premise(
        server: OnPremiseConfigurationModel,
        verbose: bool = True,
        costs: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = config["default_criteria"]
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
        location=server.usage.localisation)


async def add_results_to_configuration(c: ConfigurationModel):
    _type = c['type'] if isinstance(c, dict) else c.type
    if _type == 'cloud':
        results = await get_cloud_impact(CloudConfigurationModel.model_validate(c), verbose=False)
    else:
        results = await get_server_impact_on_premise(OnPremiseConfigurationModel.model_validate(c), verbose=False,
                                                     costs=True)
    return ConfigurationModelWithResults(results=results, configuration=c)
