import pytest
from pydantic_settings import BaseSettings


@pytest.fixture(autouse=True)
def _speech_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide required settings via env vars and never load a local .env."""
    monkeypatch.setenv(
        "SPEECH_ENDPOINT", "https://test-resource.cognitiveservices.azure.com/"
    )
    monkeypatch.setattr(
        BaseSettings,
        "model_config",
        {"env_file": None, "extra": "ignore"},
        raising=False,
    )
