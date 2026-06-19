import pytest
from typer.testing import CliRunner

from my_strands_agents.hello_world import app


@pytest.mark.unit
class TestHelloWorldCLI:
    """Tests for the hello_world CLI command."""

    def test_main_runs_with_default_prompt(self) -> None:
        """Test that the CLI prints the default prompt."""
        runner = CliRunner()
        result = runner.invoke(app, [])
        assert result.exit_code == 0
        assert "Hello world!" in result.output

    def test_main_runs_with_custom_prompt(self) -> None:
        """Test that the CLI prints the custom prompt."""
        runner = CliRunner()
        result = runner.invoke(app, ["--prompt", "What is 2 + 2?"])
        assert result.exit_code == 0
        assert "What is 2 + 2?" in result.output
