from boaviztapi.dto.usage.usage import smart_mapper_usage, smart_mapper_usage_server
from boaviztapi.model.device import DeviceServer
from boaviztapi.service.bottom_up import get_model_impact


def test_usage_server_french_mix_1_kw(french_mix_1_kw_dto):
    server = DeviceServer()
    usage = smart_mapper_usage_server(french_mix_1_kw_dto)
    server.usage = usage

    assert get_model_impact(server, 'use', 'pe') == 100
    assert get_model_impact(server, 'use', 'adp') == 4e-07
    assert get_model_impact(server, 'use', 'gwp') == 0.9


def test_usage_server_empty_usage(empty_usage_dto):
    server = DeviceServer()
    usage = smart_mapper_usage_server(empty_usage_dto)
    server.usage = usage

    assert get_model_impact(server, 'use', 'pe') == 87380
    assert get_model_impact(server, 'use', 'adp') == 0.000436
    assert get_model_impact(server, 'use', 'gwp') == 2600