import logging
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()
_logger = logging.getLogger(__name__)


class ApplicationContext:
    ENTSOE_API_KEY: str | None = None
    ELECTRICITYMAPS_API_KEY: str | None = None
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    SESSION_MIDDLEWARE_SECRET_KEY: str | None = None

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


@lru_cache
def get_app_context() -> ApplicationContext:
    s = ApplicationContext()
    s.load_secrets()
    return s
