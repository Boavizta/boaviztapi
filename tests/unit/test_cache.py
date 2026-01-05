import pytest
import respx
from httpx import Response
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, patch, MagicMock

from boaviztapi.service.cache.cache import CacheService

@pytest.fixture(autouse=True)
def reset_singleton():
    """Ensure each test has a fresh CacheService instance."""
    CacheService._instances = {}


@pytest.fixture
def mock_db():
    """Mocks the MongoDB collection."""
    collection = AsyncMock()
    # Default behavior: no cache found in DB
    collection.find_one.return_value = None
    collection.find_one_and_update = AsyncMock()
    return collection


@pytest.mark.asyncio
async def test_singleton_behavior():
    """Verify that same name returns same instance, different name returns new."""
    s1 = CacheService(name="auth", endpoints=["http://api/1"])
    s2 = CacheService(name="auth", endpoints=["http://api/1"])
    s3 = CacheService(name="data", endpoints=["http://api/2"])

    assert s1 is s2
    assert s1 is not s3


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_cache_miss(mock_db):
    """Test full refresh: API call & DB persistence."""
    url = "https://api.test/data"
    route = respx.get(url).mock(return_value=Response(200, json={"result": "ok"}))

    # 1 hour and 1 minute
    service = CacheService(name="test_miss", endpoints=[url], ttl=3660)
    service.db_cache = mock_db

    await service.fetch_all()

    # Verify API was called
    assert route.called
    # Verify memory update
    assert service.memory_cache[url] == {"result": "ok"}
    # Verify DB update call
    assert mock_db.find_one_and_update.called
    args, kwargs = mock_db.find_one_and_update.call_args
    assert kwargs['update']['$set']['data'][url] == {"result": "ok"}


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_cache_hit_valid(mock_db):
    """Test that fetch_all skips API call if DB cache is still valid."""
    url = "https://api.test/data"
    route = respx.get(url).mock(return_value=Response(200, json={"new": "data"}))

    # Mock valid cache in DB (expires in 1 hour)
    valid_time = datetime.now(timezone.utc) + timedelta(hours=1)
    mock_db.find_one.return_value = {
        "expires_at": valid_time,
        "data": {url: {"old": "data"}}
    }

    service = CacheService(name="test_hit", endpoints=[url])
    service.db_cache = mock_db

    await service.fetch_all()

    # Assert API was NEVER called
    assert not route.called
    # Assert memory was populated from DB
    assert service.memory_cache[url] == {"old": "data"}


@pytest.mark.asyncio
@respx.mock
async def test_fetch_all_with_errors_saved(mock_db):
    """Verify error handling when save_errors is True."""
    url = "https://api.test/fail"
    respx.get(url).mock(return_value=Response(500))

    service = CacheService(name="test_err", endpoints=[url], save_errors=True)
    service.db_cache = mock_db

    await service.fetch_all()

    # Verify error is stored in cache
    assert "error" in service.memory_cache[url]
    assert "500" in service.memory_cache[url]["error"]


# @pytest.mark.asyncio
# async def test_startup_logic(mock_db):
#     """Tests the full startup sequence including scheduler."""
#     CacheService._instances = {}
#     with patch("boaviztapi.application_context.get_app_context") as mock_ctx:
#         # Mocking the deeply nested app context for MongoDB
#         mock_db_client = MagicMock()
#         mock_db_client.get_database.return_value.get_collection.return_value = mock_db
#         mock_ctx.return_value.mongodb_client = mock_db_client
#
#         service = CacheService(name="test_startup", endpoints=["http://api"])
#         service.db_cache = mock_db
#
#         # Patch fetch_all so we don't trigger actual network/db logic here
#         with patch.object(CacheService, 'fetch_all', new_callable=AsyncMock) as mock_fetch:
#             await service.startup()
#
#             assert mock_fetch.called
#             assert service.scheduler.running
#
#             # Critical: stop scheduler so it doesn't hang the test runner
#             service.scheduler.shutdown()


@pytest.mark.asyncio
async def test_get_results_lazy_start(mock_db):
    """Verifies that get_results triggers startup if db_cache is missing."""
    service = CacheService(name="lazy", endpoints=["http://api"])

    with patch.object(service, 'startup', new_callable=AsyncMock) as mock_start:
        # Simulate startup setting the db_cache
        async def side_effect():
            service.db_cache = mock_db

        mock_start.side_effect = side_effect

        await service.get_results()
        assert mock_start.called