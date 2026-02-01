import os
from pathlib import Path

import yaml
from boaviztapi import data_dir
from boaviztapi.service.electricitymaps import fetch_carbon_intensity
from boaviztapi.utils.config import config
from boaviztapi.utils.country import iso3_to_iso2

config_file = os.path.join(data_dir, "factors.yml")
impact_factors = yaml.load(Path(config_file).read_text(), Loader=yaml.CSafeLoader)


def get_impact_factor(item, impact_type) -> dict:
    if impact_factors.get(item):
        if impact_factors.get(item).get(impact_type):
            return impact_factors.get(item).get(impact_type)
    raise NotImplementedError


def get_gpu_impact_factor(component, phase, impact_type) -> dict:
    if impact_factors.get("gpu"):
        if impact_factors.get("gpu").get(component):
            if impact_factors.get("gpu").get(component).get(phase):
                return (
                    impact_factors.get("gpu").get(component).get(phase).get(impact_type)
                )
    raise NotImplementedError


def get_electrical_impact_factor(usage_location, impact_type) -> dict:
    if config.electricity_maps_api_key and impact_type == "gwp":
        try:
            zone = iso3_to_iso2(usage_location)
            return fetch_carbon_intensity(config.electricity_maps_api_key, zone)
        except ValueError:
            # If we don't have a valid ISO3 location, continue
            pass

    if impact_factors["electricity"].get(usage_location):
        if impact_factors["electricity"].get(usage_location).get(impact_type):
            return impact_factors["electricity"].get(usage_location).get(impact_type)
    raise NotImplementedError


def get_electrical_min_max(impact_type, type) -> float:
    if impact_factors["electricity"].get("min-max").get(impact_type):
        if impact_factors["electricity"].get("min-max").get(impact_type).get(type):
            return (
                impact_factors["electricity"].get("min-max").get(impact_type).get(type)
            )
    raise NotImplementedError


def get_available_countries(reverse=False):
    if reverse:
        return {
            v: k
            for k, v in impact_factors["electricity"]["available_countries"].items()
        }
    return impact_factors["electricity"]["available_countries"]


def get_available_iot_functional_block():
    if impact_factors.get("IoT"):
        return impact_factors.get("IoT").keys()


def get_available_iot_hsl():
    response = {}
    for functional_block in get_available_iot_functional_block():
        response[functional_block] = (
            impact_factors.get("IoT").get(functional_block).keys()
        )
    return response


def get_iot_impact_factor(functional_block, hsl, impact_type):
    if impact_factors["IoT"].get(functional_block):
        if impact_factors["IoT"].get(functional_block).get(hsl):
            if (
                impact_factors["IoT"]
                .get(functional_block)
                .get(hsl)["manufacture"]
                .get(impact_type)
                is not None
                and impact_factors["IoT"]
                .get(functional_block)
                .get(hsl)["eol"]
                .get(impact_type)
                is not None
            ):
                return (
                    impact_factors["IoT"]
                    .get(functional_block)
                    .get(hsl)["manufacture"][impact_type]
                    + impact_factors["IoT"]
                    .get(functional_block)
                    .get(hsl)["eol"][impact_type]
                )
    raise NotImplementedError
