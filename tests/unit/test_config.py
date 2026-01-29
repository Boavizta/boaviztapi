import os

import pytest

from boaviztapi.utils.config import Settings


class TestConfigDefaults:
    def test_default_server(self):
        settings = Settings()
        assert settings.default_server == "platform_compute_medium"

    def test_default_criteria(self):
        settings = Settings()
        assert settings.default_criteria == ["gwp", "adp", "pe"]

    def test_default_allowed_origins(self):
        settings = Settings()
        assert settings.allowed_origins == ["*"]

    def test_default_special_message(self):
        settings = Settings()
        assert settings.special_message == ""


class TestConfigEnvVarOverrideWithPrefix:
    def test_override_default_server(self, monkeypatch):
        monkeypatch.setenv("BOAVIZTA_DEFAULT_SERVER", "custom-server")
        settings = Settings()
        assert settings.default_server == "custom-server"

    def test_override_default_criteria(self, monkeypatch):
        monkeypatch.setenv("BOAVIZTA_DEFAULT_CRITERIA", '["gwp", "pe"]')
        settings = Settings()
        assert settings.default_criteria == ["gwp", "pe"]

    def test_override_allowed_origins_with_prefix(self, monkeypatch):
        monkeypatch.setenv("BOAVIZTA_ALLOWED_ORIGINS", '["https://api.example.com"]')
        settings = Settings()
        assert settings.allowed_origins == ["https://api.example.com"]

    def test_override_special_message_with_prefix(self, monkeypatch):
        monkeypatch.setenv("BOAVIZTA_SPECIAL_MESSAGE", "Prefixed message")
        settings = Settings()
        assert settings.special_message == "Prefixed message"

    def test_prefixed_takes_precedence_over_non_prefixed(self, monkeypatch):
        monkeypatch.setenv("ALLOWED_ORIGINS", '["http://legacy.com"]')
        monkeypatch.setenv("BOAVIZTA_ALLOWED_ORIGINS", '["http://preferred.com"]')
        settings = Settings()
        assert settings.allowed_origins == ["http://preferred.com"]


class TestConfigEnvVarOverrideWithoutPrefix:
    def test_override_allowed_origins_single(self, monkeypatch):
        monkeypatch.setenv("ALLOWED_ORIGINS", '["http://localhost:3000"]')
        settings = Settings()
        assert settings.allowed_origins == ["http://localhost:3000"]

    def test_override_allowed_origins_multiple(self, monkeypatch):
        monkeypatch.setenv(
            "ALLOWED_ORIGINS", '["http://localhost:3000", "https://example.com"]'
        )
        settings = Settings()
        assert settings.allowed_origins == [
            "http://localhost:3000",
            "https://example.com",
        ]

    def test_override_special_message(self, monkeypatch):
        monkeypatch.setenv("SPECIAL_MESSAGE", "Hello from tests!")
        settings = Settings()
        assert settings.special_message == "Hello from tests!"

    def test_override_special_message_with_html(self, monkeypatch):
        monkeypatch.setenv("SPECIAL_MESSAGE", "<h4>Maintenance scheduled</h4>")
        settings = Settings()
        assert settings.special_message == "<h4>Maintenance scheduled</h4>"
