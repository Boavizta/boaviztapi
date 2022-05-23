from boaviztapi.utils.roundit import round_to_sigfig


def test_usage_server_french_mix_1_kw(french_mix_1_kw):
    french_mix_1_kw.smart_complete_data()
    assert round_to_sigfig(french_mix_1_kw.impact_pe()[0], 2) == 99.0
    assert round_to_sigfig(french_mix_1_kw.impact_adp()[0], 2) == 4.3e-07
    assert round_to_sigfig(french_mix_1_kw.impact_gwp()[0], 2) == 0.86


def test_usage_server_empty_usage(empty_usage):
    empty_usage.smart_complete_data()
    assert round_to_sigfig(empty_usage.impact_pe()[0], 2) == 40000.0
    assert round_to_sigfig(empty_usage.impact_adp()[0], 2) == 0.0002
    assert round_to_sigfig(empty_usage.impact_gwp()[0], 2) == 1200.0
