import logging
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()
_logger = logging.getLogger(__name__)


class ApplicationContext:
    entsoe_api_key: str | None = None

    def load_secrets(self):
        # Check docker secrets first
        entsoe_api_key = "/run/secrets/ENTSOE_API_KEY"
        if os.path.exists(entsoe_api_key):
            with open(entsoe_api_key, "r") as f:
                self.entsoe_api_key = f.read().strip()
        # Maybe not containerized, check local env
        elif os.getenv("ENTSOE_API_KEY"):
            self.entsoe_api_key = os.getenv("ENTSOE_API_KEY")
        if not self.entsoe_api_key:
            _logger.error("No ENTSOE_API_KEY environment variable! Pricing services will not work!")


@lru_cache
def get_app_context() -> ApplicationContext:
    s = ApplicationContext()
    s.load_secrets()
    return s
