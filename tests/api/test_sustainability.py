import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport
from boaviztapi.main import app
from boaviztapi.dto.auth.user_dto import UserPublicDTO
from boaviztapi.service.auth.dependencies import get_current_user
from boaviztapi.routers.sustainability_router import get_scoped_configuration_service
from boaviztapi.model.crud_models.configuration_model import OnPremiseConfigurationModel, CloudConfigurationModel

pytest_plugins = ('pytest_asyncio', 'pytest_regressions')

# Mock user for authentication
mock_user = UserPublicDTO(
    sub="1234567890",
    email="test@example.com",
    name="Test User",
    given_name="Test",
    family_name="User",
    picture="http://example.com/pic.jpg"
)

aws_cloud_config = {
            "type": "cloud",
            "name": "Development Cloud",
            "created": "2023-01-01T00:00:00.000Z",
            "cloud_provider": "aws",
            "instance_type": "a1.large",
            "user_id": "1234567890",
            "usage": {
                "localisation": "NL",
                "lifespan": 100,
                "method": "Load",
                "serverLoad": 100,
                "instancePricingType": "OnDemand",
                "reservedPlan": "yrTerm1Standard.noUpfront"
            }
        }

azure_cloud_config = {
            "type": "cloud",
            "name": "Development Cloud",
            "created": "2023-01-01T00:00:00.000Z",
            "cloud_provider": "azure",
            "instance_type": "e2ads_v5",
            "user_id": "1234567890",
            "usage": {
                "localisation": "NL",
                "lifespan": 100,
                "method": "Load",
                "serverLoad": 100,
                "instancePricingType": "OnDemand",
                "reservedPlan": "yrTerm1Savings.allUpfront"
            }
        }

gcp_cloud_config = {
            "type": "cloud",
            "name": "Development Cloud",
            "created": "2023-01-01T00:00:00.000Z",
            "cloud_provider": "gcp",
            "instance_type": "c3-standard-192-metal",
            "user_id": "1234567890",
            "usage": {
                "localisation": "NL",
                "lifespan": 100,
                "method": "Load",
                "serverLoad": 100,
                "instancePricingType": "OnDemand",
                "reservedPlan": None
            }
        }

async def override_get_current_user():
    return mock_user

# Mock ConfigurationService
@pytest.fixture
def mock_configuration_service():
    return AsyncMock()

@pytest.fixture(autouse=True)
def setup_dependencies(mock_configuration_service):
    async def override_get_service():
        return mock_configuration_service

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_scoped_configuration_service] = override_get_service

    yield
    app.dependency_overrides = {}

@pytest.fixture(autouse=True)
def mock_currency_table():
    with patch("boaviztapi.service.currency_converter.CurrencyConverter._get_currency_table", new_callable=AsyncMock) as mock:
        mock.return_value = {"AUD": 1.7508, "BRL": 6.3743, "CAD": 1.6097, "CHF": 0.9296, "CNY": 8.1973, "CZK": 24.177, "DKK": 7.4694, "GBP": 0.8719, "HKD": 9.1329, "HUF": 383.58, "IDR": 19593.06, "ILS": 3.7214, "INR": 105.719, "ISK": 147.4, "JPY": 183.94, "KRW": 1693.53, "MXN": 21.0274, "MYR": 4.7517, "NOK": 11.7985, "NZD": 2.0317, "PHP": 68.975, "PLN": 4.2123, "RON": 5.0895, "SEK": 10.8085, "SGD": 1.5077, "THB": 36.792, "TRY": 50.4332, "USD": 1.1721, "ZAR": 19.3561}
        yield mock

@pytest.mark.asyncio
async def test_post_results_on_premise_configuration(data_regression):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post('/v1/sustainability/on-premise?verbose=true&costs=true', json={
            "type": "on-premise",
            "name": "R740",
            "created": "2023-01-01T00:00:00.000Z",
            "cpu_quantity": 2,
            "cpu_core_units": 24,
            "cpu_tdp": 120,
            "cpu_architecture": "Intel Xeon",
            "ram_quantity": 12,
            "ram_capacity": 32,
            "ram_manufacturer": "Micron",
            "ssd_quantity": 1,
            "ssd_capacity": 400,
            "ssd_manufacturer": "Samsung",
            "hdd_quantity": 1,
            "server_type": "rack",
            "psu_quantity": 2,
            "user_id": "1234567890",
            "usage": {
                "localisation": "NL",
                "lifespan": 5,
                "method": "Electricity",
                "avgConsumption": 100,
                "serverLoad": 50,
                "operatingCosts": 700
            }
        })
    assert res.status_code == 200
    data_regression.check(data_dict=res.json(), round_digits=1)

@pytest.mark.asyncio
@pytest.mark.parametrize("cloud_config", [aws_cloud_config, azure_cloud_config, gcp_cloud_config])
async def test_post_results_cloud_configuration(data_regression, cloud_config):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.post('/v1/sustainability/cloud?verbose=true&costs=true', json=cloud_config)
    assert res.status_code == 200
    data_regression.check(data_dict=res.json(), round_digits=1)

@pytest.mark.asyncio
async def test_get_results_on_premise_configuration(data_regression, mock_configuration_service):
    # Setup mock return value
    mock_server = OnPremiseConfigurationModel(
        type="on-premise",
        name="R740",
        created="2023-01-01T00:00:00.000Z",
        cpu_quantity=2,
        cpu_core_units=24,
        cpu_tdp=120,
        cpu_architecture="SKYLAKE",
        ram_quantity=4,
        ram_capacity=32,
        ram_manufacturer="Micron",
        ssd_quantity=1,
        ssd_capacity=1000,
        ssd_manufacturer="samsung",
        hdd_quantity=1,
        server_type="rack",
        psu_quantity=2,
        user_id="1234567890",
        usage={
            "localisation": "NL",
            "lifespan": 43800,
            "method": "Electricity",
            "avgConsumption": 100,
            "serverLoad": 100,
            "operatingCosts": 700
        }
    )
    mock_configuration_service.get_by_id = AsyncMock(return_value= mock_server)

    transport = ASGITransport(app=app)

    # Use a valid ObjectId format for the ID
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        res = await ac.get('/v1/sustainability/on-premise/507f1f77bcf86cd799439011?verbose=true&costs=true')
    
    assert res.status_code == 200
    data_regression.check(data_dict=res.json(), round_digits=1)

@pytest.mark.asyncio
@pytest.mark.parametrize('cloud_config', [aws_cloud_config, azure_cloud_config, gcp_cloud_config])
async def test_get_results_cloud_configuration(data_regression, mock_configuration_service, cloud_config):
    # Setup mock return value
    mock_cloud = CloudConfigurationModel.model_validate(cloud_config)
    # mock_cloud = CloudConfigurationModel(
    #     type="cloud",
    #     name="Development Cloud",
    #     created="2023-01-01T00:00:00.000Z",
    #     cloud_provider="AWS",
    #     instance_type="a1.medium",
    #     user_id="1234567890",
    #     usage={
    #         "localisation": "NL",
    #         "lifespan": 1000,
    #         "method": "Load",
    #         "serverLoad": 100,
    #         "instancePricingType": "OnDemand",
    #         "reservedPlan": "yrTerm1Standard.noUpfront"
    #     }
    # )
    mock_configuration_service.get_by_id = AsyncMock(return_value= mock_cloud)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Use a valid ObjectId format for the ID
        res = await ac.get('/v1/sustainability/cloud/507f1f77bcf86cd799439011?verbose=true&costs=true')

    assert res.status_code == 200
    data_regression.check(data_dict=res.json(), round_digits=1)
