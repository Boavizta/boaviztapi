import logging
import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure

_logger = logging.getLogger(__name__)

class ApplicationContext:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        load_dotenv()

    ENTSOE_API_KEY: str | None = None
    ELECTRICITYMAPS_API_KEY: str | None = None
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    SESSION_MIDDLEWARE_SECRET_KEY: str | None = None
    mongodb_client: AsyncMongoClient | None = None
    database_name: str = None

    dependencies = ["ENTSOE_API_KEY", "ELECTRICITYMAPS_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET",
                    "SESSION_MIDDLEWARE_SECRET_KEY"]

    def load_secrets(self):
        # Check docker secrets first
        for dep in self.dependencies:
            dep_path = f"/run/secrets/{dep}"
            if os.path.exists(dep_path):
                with open(dep_path, "r") as f:
                    _logger.info(f"Loading {dep} from {dep_path}")
                    setattr(self, dep, f.read().strip())

            # Maybe not containerized, check local env
            elif os.getenv(dep):
                _logger.info(f"Loading {dep} from env")
                setattr(self, dep, os.getenv(dep))
            # Not found in secrets or env
            if not getattr(self, dep):
                _logger.error(f"No {dep} environment variable! Related services may not work!")

    async def create_db_connection(self):
        self.mongodb_client = AsyncMongoClient(os.getenv("MONGODB_URL"))
        _logger.info(f"Checking if the MongoDB server is reachable at {os.getenv('MONGODB_URL')}")
        try:
            await self.mongodb_client.admin.command('ping')
            _logger.info("The MongoDB server is available. Continuing start-up...")
            self.database_name = os.getenv("MONGODB_DATABASE")
            if not self.database_name:
                raise RuntimeError("Database name is not set! Please set it in the environment variables")
        except ConnectionFailure as e:
            _logger.error("The MongoDB server is not reachable. Shutting down the server...", e)
            exit(1)

    async def close_db_connection(self):
        await self.mongodb_client.close()


def get_app_context() -> ApplicationContext:
    return ApplicationContext()
