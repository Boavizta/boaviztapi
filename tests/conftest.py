import pytest


# All top-level pytest configuration
def pytest_configure(config):
    # E2E marker to mark tests as E2E
    config.addinivalue_line("markers", "e2e: mark test as an e2e test")


# Add option to run only E2E tests. If not specified, all non-E2E tests will run
def pytest_addoption(parser):
    parser.addoption(
        "--rune2e",
        action="store_true",
        default=False,
        help="Run e2e tests",
    )


def pytest_collection_modifyitems(config, items):
    # Run only E2E tests if --rune2e specified, otherwise exclude them
    if config.getoption("--rune2e"):
        skip_non_e2e = pytest.mark.skip(reason="--rune2e runs only e2e tests")
        for item in items:
            if "e2e" not in item.keywords:
                item.add_marker(skip_non_e2e)
        return

    skip_e2e = pytest.mark.skip(reason="need --rune2e option to run")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)
