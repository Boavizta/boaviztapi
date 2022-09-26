from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf


def test_fuzzymatch_cpu(cpu_dataframe):
    assert "Broadwell" == fuzzymatch_attr_from_pdf("broadwel", "family", cpu_dataframe)
    assert fuzzymatch_attr_from_pdf("cevevvreceerf", "family", cpu_dataframe) is None


def test_fuzzymatch_ssd(ssd_dataframe):
    assert "Samsung" == fuzzymatch_attr_from_pdf("samesung", "manufacturer", ssd_dataframe)
    assert fuzzymatch_attr_from_pdf("deer", "manufacturer", ssd_dataframe) is None


def test_fuzzymatch_ram(ram_dataframe):
    assert "Samsung" == fuzzymatch_attr_from_pdf("samesung", "manufacturer", ram_dataframe)
    assert fuzzymatch_attr_from_pdf("4R", "manufacturer", ram_dataframe) is None

