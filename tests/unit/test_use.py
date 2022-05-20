def test_usage_server_french_mix_1_kw(french_mix_1_kw):
    french_mix_1_kw.smart_complete_data()
    assert round(french_mix_1_kw.impact_manufacture_pe()[0], 0) == 98892.0
    assert round(french_mix_1_kw.impact_manufacture_adp()[0], 6) == 0.000426
    assert round(french_mix_1_kw.impact_manufacture_gwp()[0], 0) == 858.0


def test_usage_server_empty_usage(empty_usage):
    empty_usage.smart_complete_data()
    assert round(empty_usage.impact_manufacture_pe()[0], 0) == 39669.0
    assert round(empty_usage.impact_manufacture_adp()[0], 6) == 0.000198
    assert round(empty_usage.impact_manufacture_gwp()[0], 0) == 1171.0
