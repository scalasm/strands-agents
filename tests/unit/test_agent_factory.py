from unittest.mock import MagicMock, patch

import pytest

from my_strands_agents.utils.agent_factory import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODEL_ID,
    DEFAULT_TEMPERATURE,
    create_openai_model,
)


@pytest.mark.unit
class TestCreateOpenAIModel:
    """Tests for OpenAI model factory behavior."""

    def test_create_openai_model_with_explicit_api_key_uses_defaults(self) -> None:
        """Create a model with explicit API key and default parameters."""
        with patch("my_strands_agents.utils.agent_factory.OpenAIModel") as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model

            result = create_openai_model(api_key="sk-explicit-key")

            assert result is mock_model
            mock_model_class.assert_called_once_with(
                client_args={"api_key": "sk-explicit-key"},
                model_id=DEFAULT_MODEL_ID,
                params={"max_tokens": DEFAULT_MAX_TOKENS, "temperature": DEFAULT_TEMPERATURE},
            )

    def test_create_openai_model_with_custom_parameters(self) -> None:
        """Pass custom values through to model construction."""
        with patch("my_strands_agents.utils.agent_factory.OpenAIModel") as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model

            result = create_openai_model(
                model_id="gpt-4o-mini",
                api_key="sk-custom-key",
                max_tokens=2048,
                temperature=0.3,
            )

            assert result is mock_model
            mock_model_class.assert_called_once_with(
                client_args={"api_key": "sk-custom-key"},
                model_id="gpt-4o-mini",
                params={"max_tokens": 2048, "temperature": 0.3},
            )

    def test_create_openai_model_uses_environment_api_key_when_missing_argument(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Use OPENAI_API_KEY when api_key argument is omitted."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-env-key")

        with patch("my_strands_agents.utils.agent_factory.OpenAIModel") as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model

            result = create_openai_model()

            assert result is mock_model
            mock_model_class.assert_called_once_with(
                client_args={"api_key": "sk-env-key"},
                model_id=DEFAULT_MODEL_ID,
                params={"max_tokens": DEFAULT_MAX_TOKENS, "temperature": DEFAULT_TEMPERATURE},
            )

    def test_create_openai_model_explicit_api_key_overrides_environment(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Prefer explicit API key over OPENAI_API_KEY environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "sk-env-key")

        with patch("my_strands_agents.utils.agent_factory.OpenAIModel") as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model

            result = create_openai_model(api_key="sk-explicit-key")

            assert result is mock_model
            mock_model_class.assert_called_once_with(
                client_args={"api_key": "sk-explicit-key"},
                model_id=DEFAULT_MODEL_ID,
                params={"max_tokens": DEFAULT_MAX_TOKENS, "temperature": DEFAULT_TEMPERATURE},
            )

    def test_create_openai_model_raises_when_api_key_missing_and_env_not_set(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Raise ValueError when no API key is available from args or environment."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(
            ValueError,
            match=r"API Key not passed and OPENAI_API_KEY environment variable is not set\.",
        ):
            create_openai_model(api_key=None)

    def test_create_openai_model_raises_when_api_key_is_empty_string(self) -> None:
        """Raise ValueError when the explicit API key is empty."""
        with pytest.raises(
            ValueError,
            match=r"API Key not passed and OPENAI_API_KEY environment variable is not set\.",
        ):
            create_openai_model(api_key="")
