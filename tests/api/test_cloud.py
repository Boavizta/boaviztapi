import pytest
pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_complete_usage():
    assert True  # TODO


@pytest.mark.asyncio
async def test_default_usage():
    assert True  # TODO
