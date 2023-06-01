from boaviztapi.dto.usage.usage import mapper_usage_server
from boaviztapi.model.device import DeviceServer
from boaviztapi.service.bottom_up import get_model_single_impact


def test_usage_server_french_mix_1_kw(french_mix_1_kw_dto):
    server = DeviceServer()
    usage = mapper_usage_server(french_mix_1_kw_dto)
    server.usage = usage

    assert get_model_single_impact(server, 'use', 'pe').to_json() == {'max': 1000.0, 'min': 0.01, 'significant_figures': 1, 'value': 100.0}
    assert get_model_single_impact(server, 'use', 'adpe').to_json() == {'max': 4e-06, 'min': 5e-11, 'significant_figures': 1, 'value': 4e-07}
    assert get_model_single_impact(server, 'use', 'gwp').to_json() == {'max': 9.0, 'min': 0.0001, 'significant_figures': 1, 'value': 0.9}


def test_usage_server_empty_usage(empty_usage_dto):
    server = DeviceServer()
    usage = mapper_usage_server(empty_usage_dto)
    server.usage = usage

    assert get_model_single_impact(server, 'use', 'pe').to_json() == {'max': 334600000.0,'min': 0.002487,'significant_figures': 4,'value': 87380.0}
    assert get_model_single_impact(server, 'use', 'adpe').to_json() == {'max': 0.19,'min': 2.53e-09,'significant_figures': 3, 'value': 0.000436}
    assert get_model_single_impact(server, 'use', 'gwp').to_json() == {'max': 640000.0,'min': 0.0044,'significant_figures': 2, 'value': 2600.0}