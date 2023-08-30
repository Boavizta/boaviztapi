from boaviztapi.utils.fuzzymatch import fuzzymatch_attr_from_pdf, fuzzymatch_attr_from_cpu_name
import pytest


@pytest.mark.parametrize("cpu_name_input, name, manufacturer, code_name, model_range, tdp, cores, total_die_size, total_die_size_source, source", [
    ("Intel(R) Pentium(R) CPU G2030 @ 3.00GHz", "Intel Pentium G2030", "Intel", "Ivy Bridge", "Pentium G", None, None, None, None, "https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data"),
    ("Intel(R) Core(TM) m7-6Y75 CPU @ 1.20GHz", "Intel Core m7-6Y75", "Intel", "Skylake", "Core m7", None, None, None, None, "https://github.com/cloud-carbon-footprint/cloud-carbon-coefficients/tree/main/data"),
    ("AMD EPYC 7R32 48-Core Processor", "AMD EPYC 7R32", "AMD", "Rome", "EPYC", 280, 48, None, None, "https://docs.google.com/spreadsheets/d/1DqYgQnEDLQVQm5acMAhLgHLD8xXCG9BIrk-_Nv6jF3k/edit#gid=224728652"),
    ("Intel(R) Xeon(R) CPU E5-2660 0 @ 2.20GHz", "Intel Xeon E5-2660", "Intel", "Sandy Bridge-EP", "Xeon E5", 95, 8, 435, "io_die_size () + die_size (435 mm²)", "https://www.techpowerup.com/cpu-specs/xeon-e5-2660.c976"),
    ("Intel(R) Xeon(R) CPU E5-2680 v2 @ 2.80GHz", "Intel Xeon E5-2680 v2", "Intel", "Ivy Bridge-EP", "Xeon E5", 115, 10, 160, "io_die_size () + die_size (160 mm²)", "https://www.techpowerup.com/cpu-specs/xeon-e5-2680-v2.c1666"),
    ("Intel(R) Celeron(R) CPU G3900 @ 2.80GHz", "Intel Celeron G3900", "Intel", "Skylake", "Celeron G", 51, 2, 150, "io_die_size () + die_size (150 mm²)", "https://www.techpowerup.com/cpu-specs/celeron-g3900.c1855"),
    ("Intel® Xeon™ CPU 3.20GHz", "Intel Xeon 3.20", "Intel", "Gallatin", "Xeon", 97, 1, 237, "io_die_size () + die_size (237 mm²)", "https://www.techpowerup.com/cpu-specs/xeon-3-20.c298"),
    ("Intel(R) Core(TM)2 Duo CPU     E8400  @ 3.00GHz", "Intel Core 2 Duo E8400", "Intel", "Wolfdale", "Core 2 Duo E", 65, 2, 104, "io_die_size () + die_size (104 mm²)", "https://www.techpowerup.com/cpu-specs/core-2-duo-e8400.c467"),
    ("AMD Athlon(tm) II X3 450 Processor", "AMD Athlon II X3 450", "AMD", "Rana", "Athlon II X3", 95, 3, 169, "io_die_size () + die_size (169 mm²)", "https://www.techpowerup.com/cpu-specs/athlon-ii-x3-450.c697"),
    ("Intel(R) Core(TM) i7-8550U CPU @ 1.80GHz", "Intel Core i7-8550U", "Intel", "Kaby Lake-R", "Core i7", 15, 4, 123, "io_die_size () + die_size (123 mm²)", "https://www.techpowerup.com/cpu-specs/core-i7-8550u.c1974"),
    ("AMD Ryzen 9 5900X 12-Core Processor", "AMD Ryzen 9 5900X", "AMD", "Vermeer", "Ryzen 9", 105, 12, 205, "io_die_size (124 mm²) + die_size (81 mm²)", "https://www.techpowerup.com/cpu-specs/ryzen-9-5900x.c2363"),
    ("AMD Ryzen 7 1700 Eight-Core Processor", "AMD Ryzen 7 1700", "AMD", "Zen", "Ryzen 7", 65, 8, 213, "io_die_size () + die_size (213 mm²)", "https://www.techpowerup.com/cpu-specs/ryzen-7-1700.c1893"),
])
def test_fuzzymatch_attr_from_cpu_name(cpu_specs_dataframe, cpu_name_input, name, manufacturer, code_name, model_range, tdp, cores, total_die_size, total_die_size_source, source):
    assert (name, manufacturer, code_name, model_range, tdp, cores, total_die_size, total_die_size_source, source) == fuzzymatch_attr_from_cpu_name(cpu_name_input, cpu_specs_dataframe)


def test_fuzzymatch_cpu(cpu_dataframe):
    assert "broadwell" == fuzzymatch_attr_from_pdf("broadwel", "code_name", cpu_dataframe).lower()
    assert fuzzymatch_attr_from_pdf("cevevvreceerf", "code_name", cpu_dataframe) is None


def test_fuzzymatch_ssd(ssd_dataframe):
    assert "samsung" == fuzzymatch_attr_from_pdf("samesung", "manufacturer", ssd_dataframe).lower()
    assert fuzzymatch_attr_from_pdf("deer", "manufacturer", ssd_dataframe) is None


def test_fuzzymatch_ram(ram_dataframe):
    assert "samsung" == fuzzymatch_attr_from_pdf("samesung", "manufacturer", ram_dataframe).lower()
    assert fuzzymatch_attr_from_pdf("4R", "manufacturer", ram_dataframe) is None


