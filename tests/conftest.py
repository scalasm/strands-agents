import pytest


@pytest.fixture(autouse=True)
def _reset_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure environment variable changes are isolated between tests."""
