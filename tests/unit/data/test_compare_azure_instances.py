import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parents[3] / (
    "boaviztapi/data/utils/scripts/compare_azure_instances.py"
)
spec = importlib.util.spec_from_file_location("compare_azure", SCRIPT)
compare_azure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compare_azure)


def sku(temp_mib, nvme_mib):
    return {
        "vcpu": 16,
        "memory": 128.0,
        "temp_disk_mib": temp_mib,
        "nvme_disk_mib": nvme_mib,
        "gpus": 0.0,
    }


def test_temp_disk_stays_in_gib():
    specs = compare_azure.azure_specs(sku(76800, 0))
    assert specs["ssd_storage"] == pytest.approx(75.0)


def test_nvme_is_converted_to_decimal_gb():
    specs = compare_azure.azure_specs(sku(163840, 3662109))
    assert specs["ssd_storage"] == pytest.approx(4000, rel=1e-3)


def test_lsv3_row_is_not_a_mismatch():
    azure = compare_azure.azure_specs(sku(163840, 3662109))
    boavizta = {
        "vcpu": 16.0,
        "memory": 128.0,
        "ssd_storage": 4000.0,
        "hdd_storage": 0.0,
        "gpu_units": 0.0,
    }
    diffs = compare_azure.diff_specs(boavizta, azure, 0.05)
    assert "ssd_storage" not in diffs
