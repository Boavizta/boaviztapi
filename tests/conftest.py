import sys

import pytest

from boaviztapi import config as bv_config

# Check if we're running end-to-end tests
_running_e2e = "--rune2e" in sys.argv

# Add overrides for non-E2E tests
if not _running_e2e:
    bv_config.cpu_name_fuzzymatch_threshold = 60
    bv_config.default_case = "DEFAULT"
    bv_config.default_server = "DEFAULT"
    bv_config.electricity_maps_api_key = (
        ""  # Deactivate Electricity Maps integration for unit tests
    )


def pytest_configure(config):
    """Applies all top-level pytest configuration."""

    # Allow marking end-to-end tests with annotation
    config.addinivalue_line("markers", "e2e: mark test as an end-to-end test")


def pytest_addoption(parser):
    """Adds global options to the pytest commandline."""

    # Option to run only end-to-end tests. If not specified, all non-E2E tests will run
    parser.addoption(
        "--rune2e",
        action="store_true",
        default=False,
        help="Run end-to-end tests",
    )


def pytest_collection_modifyitems(config, items):
    """Provides the list of tests for pytest to run."""

    # Skip non-end-to-end tests if running end-to-end tests
    if config.getoption("--rune2e"):
        skip_non_e2e = pytest.mark.skip(reason="--rune2e runs only end-to-end tests")
        for item in items:
            if "e2e" not in item.keywords:
                item.add_marker(skip_non_e2e)
        return

    skip_e2e = pytest.mark.skip(reason="need --rune2e option to run")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)
