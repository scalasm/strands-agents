from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from my_strands_agents.hello_world import app


@pytest.mark.unit
class TestHelloWorldCLI:
    """Tests for the hello_world CLI command."""

    def test_main_runs_agent_with_default_prompt(self) -> None:
        """Test that the CLI invokes the agent with the default prompt."""
        runner = CliRunner()
        with patch("my_strands_agents.hello_world.Agent") as mock_agent_class:
            mock_instance = MagicMock()
            mock_agent_class.return_value = mock_instance

            result = runner.invoke(app, [])

            assert result.exit_code == 0
            mock_agent_class.assert_called_once_with()
            mock_instance.assert_called_once()

    def test_main_runs_agent_with_custom_prompt(self) -> None:
        """Test that the CLI passes a custom prompt to the agent."""
        runner = CliRunner()
        custom_prompt = "What is 2 + 2?"
        with patch("my_strands_agents.hello_world.Agent") as mock_agent_class:
            mock_instance = MagicMock()
            mock_agent_class.return_value = mock_instance

            result = runner.invoke(app, ["--prompt", custom_prompt])

            assert result.exit_code == 0
            mock_instance.assert_called_once_with(custom_prompt)
