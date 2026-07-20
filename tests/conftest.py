"""Shared test fixtures for Mealie Mcp."""

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set standard test environment variables."""
    monkeypatch.setenv("MEALIE_URL", "https://test.example.com")
    monkeypatch.setenv("MEALIE_TOKEN", "test-token-12345")
