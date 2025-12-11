import logging
from copy import deepcopy
from typing import Optional, List, Dict, Any

from boaviztapi import config
from boaviztapi.dto.device.device import mapper_cloud_instance, mapper_server
from boaviztapi.model.crud_models.configuration_model import CloudConfigurationModel, OnPremiseConfigurationModel, \
    ConfigurationModelWithResults
from boaviztapi.routers.cloud_router import cloud_instance_impact
from boaviztapi.routers.server_router import server_impact
from boaviztapi.service.archetype import get_cloud_instance_archetype, get_server_archetype
from boaviztapi.service.results_provider import mapper_config_to_server

_log = logging.getLogger(__name__)

async def get_cloud_impact(
        cloud_instance: CloudConfigurationModel,
        verbose: bool = True,
        duration: Optional[float] = config["default_duration"],
        criteria: List[str] = config["default_criteria"]):
    cloud_provider = cloud_instance.cloud_provider.lower()  # Solves the path not being found issue.
    cloud_archetype = get_cloud_instance_archetype(cloud_instance.instance_type, cloud_provider)
    if not cloud_archetype:
        raise ValueError(f"{cloud_instance.instance_type} at {cloud_instance.cloud_provider} not found")
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
        criteria=criteria)


async def add_results_to_configuration(c: ConfigurationModelWithResults):
    _type = c['configuration']['type'] if isinstance(c, dict) else c.configuration.type
    config = c['configuration'] if isinstance(c, dict) else c.configuration
    if _type == 'cloud':
        results = await get_cloud_impact(CloudConfigurationModel.model_validate(config),
                                         verbose=False,
                                         criteria=["gwp", "pe"])
    else:
        results = await get_server_impact_on_premise(OnPremiseConfigurationModel.model_validate(config),
                                                     verbose=False,
                                                     criteria=["gwp", "pe"])
    return c.results | results


async def compute_portfolio_totals(configs: List[ConfigurationModelWithResults]) -> Dict[str, Any] | None:
    """
    Compute the total impact values of an entire portfolio by summing each configuration's impact results.

    Raises:
        ValueError if mandatory impact results of one of the configurations are missing (gwp or pe).
    """
    if len(configs) == 0:
        return None
    if len(configs) == 1:
        return configs[0].results

    total = deepcopy(configs[0].results['impacts'])
    try:
        for conf in configs[1:]:
            results = conf.results
            gwp = results['impacts']['gwp']
            pe = results['impacts']['pe']

            _add_all_to_total(total['gwp'], gwp)
            _add_all_to_total(total['pe'], pe)
    except KeyError as e:
        _log.error(e)
        raise ValueError("Mandatory impact results of one of the configurations are missing! (gwp, pe)")
    return total


def _add_all_to_total(total: Dict[str, Any], impact: Dict[str, Any]) -> None:
    if 'embedded' in total and 'embedded' in impact:
        _add_values_to_total(total['embedded'], impact['embedded'])
    if 'use' in total and 'use' in impact:
        _add_values_to_total(total['use'], impact['use'])


def _add_values_to_total(total: Dict[str, Any], impact: Dict[str, Any]) -> None:
    total['value'] += impact['value']
    total['min'] += impact['min']
    total['max'] += impact['max']