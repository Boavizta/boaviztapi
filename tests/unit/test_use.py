from boaviztapi.dto.usage.usage import (
    mapper_usage_server,
    _reset_usage_dto_if_matches_config_defaults,
    UsageServer,
)
from boaviztapi.model.device.server import DeviceServer
from boaviztapi.service.impacts_computation import compute_single_impact
from boaviztapi import config


def test_usage_server_french_mix_1_kw(french_mix_1_kw_dto):
    server = DeviceServer()
    usage = mapper_usage_server(french_mix_1_kw_dto)
    server.usage = usage

    assert compute_single_impact(server, "use", "pe", duration=365 * 24).to_json() == {
        "max": 98.89,
        "min": 98.89,
        "value": 98.89,
    }
    assert compute_single_impact(server, "use", "adp", duration=365 * 24).to_json() == {
        "max": 4.256e-07,
        "min": 4.256e-07,
        "value": 4.256e-07,
    }
    assert compute_single_impact(server, "use", "gwp", duration=365 * 24).to_json() == {
        "max": 0.8585,
        "min": 0.8585,
        "value": 0.8585,
    }


def test_usage_server_empty_usage(empty_usage_dto):
    server = DeviceServer()
    usage = mapper_usage_server(empty_usage_dto)
    server.usage = usage

    assert compute_single_impact(server, "use", "pe", duration=365 * 24).to_json() == {
        "max": 33460000.0,
        "min": 21.79,
        "value": 90000.0,
        "warnings": [
            "Uncertainty from technical characteristics is very important. Results should "
            "be interpreted with caution (see min and max values)"
        ],
    }
    assert compute_single_impact(server, "use", "adp", duration=365 * 24).to_json() == {
        "max": 0.01898,
        "min": 2.212e-05,
        "value": 0.0004,
        "warnings": [
            "Uncertainty from technical characteristics is very important. Results should "
            "be interpreted with caution (see min and max values)"
        ],
    }
    assert compute_single_impact(server, "use", "gwp", duration=365 * 24).to_json() == {
        "max": 64320.0,
        "min": 38.55,
        "value": 3000.0,
    }


def test_reset_usage_dto_if_matches_config_defaults():
    """Test that usage_location is reset to None when it matches config default"""

    usage_dto = UsageServer()
    usage_dto.usage_location = "EEE"
    _reset_usage_dto_if_matches_config_defaults(usage_dto)
    assert usage_dto.usage_location is None

    usage_dto = UsageServer()
    usage_dto.usage_location = "eee"
    _reset_usage_dto_if_matches_config_defaults(usage_dto)
    assert usage_dto.usage_location is None

    usage_dto = UsageServer()
    usage_dto.usage_location = "Eee "
    _reset_usage_dto_if_matches_config_defaults(usage_dto)
    assert usage_dto.usage_location is None

    usage_dto = UsageServer()
    usage_dto.usage_location = "FRA"
    _reset_usage_dto_if_matches_config_defaults(usage_dto)
    assert usage_dto.usage_location == "FRA"

    usage_dto = UsageServer()
    usage_dto.usage_location = None
    _reset_usage_dto_if_matches_config_defaults(usage_dto)
    assert usage_dto.usage_location is None
