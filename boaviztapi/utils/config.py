from typing import List, Optional

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized configuration for BoaviztAPI."""

    model_config = SettingsConfigDict(
        env_prefix="BOAVIZTA_",
        env_file=".env",
        extra="ignore",
    )

    # Location and usage defaults
    default_location: str = "EEE"
    default_usage: str = "DEFAULT"

    # Component defaults
    default_cpu: str = "DEFAULT"
    default_gpu: str = "DEFAULT"
    default_ram: str = "DEFAULT"
    default_ssd: str = "DEFAULT"
    default_hdd: str = "DEFAULT"
    default_power_supply: str = "DEFAULT"
    default_case: str = "rack"
    default_assembly: str = "DEFAULT"
    default_motherboard: str = "DEFAULT"

    # Server defaults
    default_server: str = "platform_compute_medium"

    # Cloud defaults
    default_cloud_instance: str = "a1.4xlarge"
    default_cloud_provider: str = "aws"

    # End-user device defaults
    default_laptop: str = "laptop-pro"
    default_desktop: str = "desktop-pro"
    default_smartphone: str = "smartphone-default"
    default_tablet: str = "tablet-default"
    default_television: str = "tv-pro"
    default_monitor: str = "monitor-default"
    default_smartwatch: str = "smartwatch-default"
    default_box: str = "box-default"
    default_usb_stick: str = "usb-stick-default"
    default_external_ssd: str = "external-ssd-default"
    default_external_hdd: str = "hdd-default"
    default_iot_device: str = "iot-device-default"
    default_vr_headset: str = "vr-headset-lcd"
    default_vr_controller: str = "vr-controller-default"

    # Criteria defaults
    default_criteria: List[str] = ["gwp", "adp", "pe"]
    default_gpu_criteria: List[str] = ["gwp", "adpe", "wu"]

    # Duration default (None means not set)
    default_duration: Optional[float] = None

    # Rounding and precision
    uncertainty: int = 10
    max_sig_fig: int = 4
    min_sig_fig: int = 1

    # Fuzzy matching
    cpu_name_fuzzymatch_threshold: int = 80

    # Application settings (support both BOAVIZTA_ prefix and legacy non-prefixed)
    allowed_origins: List[str] = Field(
        default=["*"],
        validation_alias=AliasChoices("BOAVIZTA_ALLOWED_ORIGINS", "ALLOWED_ORIGINS"),
    )
    special_message: str = Field(
        default="",
        validation_alias=AliasChoices("BOAVIZTA_SPECIAL_MESSAGE", "SPECIAL_MESSAGE"),
    )


config = Settings()
