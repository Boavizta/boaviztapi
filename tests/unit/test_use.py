from boaviztapi.dto.usage.usage import mapper_usage_server
from boaviztapi.model.device import DeviceServer
from boaviztapi.service.bottom_up import get_model_single_impact


def test_usage_server_french_mix_1_kw(french_mix_1_kw_dto):
    server = DeviceServer()
    usage = mapper_usage_server(french_mix_1_kw_dto)
    server.usage = usage

    assert get_model_single_impact(server, 'use', 'pe', duration=365*24).to_json() == {'max': 99.0, 'min': 99.0, 'significant_figures': 2, 'value': 99.0}
    assert get_model_single_impact(server, 'use', 'adp', duration=365*24).to_json() == {'max': 4.3e-07, 'min': 4.3e-07, 'significant_figures': 2, 'value': 4.3e-07}
    assert get_model_single_impact(server, 'use', 'gwp', duration=365*24).to_json() == {'max': 0.86, 'min': 0.86, 'significant_figures': 2, 'value': 0.86}


def test_usage_server_empty_usage(empty_usage_dto):
    server = DeviceServer()
    usage = mapper_usage_server(empty_usage_dto)
    server.usage = usage

    assert get_model_single_impact(server, 'use', 'pe', duration=365*24).to_json() == {'max': 33455000.0, 'min': 21.787, 'significant_figures': 5, 'value': 87381.0}
    assert get_model_single_impact(server, 'use', 'adp', duration=365*24).to_json() == {'max': 0.019, 'min': 2.21e-05, 'significant_figures': 3, 'value': 0.000436}
    assert get_model_single_impact(server, 'use', 'gwp', duration=365*24).to_json() == {'max': 64000.0, 'min': 39.0, 'significant_figures': 2, 'value': 2600.0}