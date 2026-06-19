# Strands Agents - Workspace Instructions

AI coding assistant instructions for the Strands Agents learning and experimentation project.

## Project Overview

Modern Python 3.14+ project for learning and experimenting with Amazon Strands Agents. Emphasizes **type safety**, **code quality**, and **comprehensive testing** with a clean, maintainable architecture.

## Core Technologies

- **Python 3.14+** - Latest Python with modern syntax
- **Amazon Strands Agents SDK** - Agent framework backed by Amazon Bedrock
- **UV** - Fast, reliable dependency and environment management (replaces pip/poetry)
- **Ruff** - Lightning-fast linting and formatting (replaces black/flake8/isort)
- **mypy** - Strict static type checking
- **pytest** - Testing framework with three-tier organization (unit/integration/e2e)
- **pre-commit** - Automated code quality checks
- **Typer** - CLI framework for command-line interfaces

## Essential Commands

### Build & Dependencies
```bash
uv sync                    # Install/sync dependencies from lockfile
uv add <package>           # Add new dependency
uv run <command>           # Run command in project venv (auto-activates)
```

### Development Workflow
```bash
make ci                    # Run ALL checks (what CI runs - do this before PRs!)
make format                # Auto-format code with ruff
make lint                  # Lint and auto-fix with ruff
make type-check            # Type check with mypy
make test-all              # Run all tests with coverage
make test-unit             # Run unit tests only
make coverage              # Generate detailed HTML coverage report
```

### Pre-commit
```bash
uv run pre-commit run --all-files    # Run all hooks manually
```
Note: Pre-commit hooks run automatically on `git commit` - they MUST pass before code can be committed.

## AWS Credentials & Model

Strands Agents defaults to **Amazon Bedrock** (Claude Sonnet 4). Credentials are configured via:
1. `~/.aws/` credentials file (mounted into devcontainer automatically)
2. `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` environment variables
3. IAM roles when running on AWS

Enable model access in Amazon Bedrock for `anthropic.claude-sonnet-4` in your target region before running agents.

## Code Quality Standards

### Type Hints (MANDATORY)
**All functions and methods MUST have complete type hints.** Enforced by mypy with `disallow_untyped_defs = true`.

```python
# ✅ CORRECT
def process_items(items: list[str], limit: int = 10) -> dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items[:limit]}

# ❌ WRONG - will fail mypy
def process_items(items, limit=10):
    return {item: len(item) for item in items[:limit]}
```

- Use built-in generics: `list[T]`, `dict[K, V]` (not `List`, `Dict` from typing)
- Explicit `None` return types: `-> None` for functions without return values
- Use `| None` instead of `Optional[T]` (Python 3.10+ style)
- Import from `collections.abc` for abstract types: `Sequence`, `Iterable`, `Mapping`

### Formatting & Linting
- **Line length:** 128 characters max
- **Quotes:** Double quotes (`"`) for strings
- **Import order:** Automatic via ruff's isort integration

### Code Style Principles
1. **No magic numbers** - Use named constants (ALL_CAPS)
2. **Explicit over implicit** - Clear variable/function names
3. **Type hints everywhere** - Function signatures must be typed
4. **Docstrings for public APIs** - Use Google-style docstrings
5. **DRY (Don't Repeat Yourself)** - Extract common patterns

## Testing Strategy

### Three-Tier Test Organization
```
tests/
├── unit/           # Fast, isolated, no external dependencies
├── integration/    # Requires local services
└── e2e/            # Requires AWS Bedrock (runs on main branch only)
```

### Coverage Requirements
- **Minimum 80% coverage** enforced by CI
- Command: `make coverage` for detailed HTML report

### Mocking Agents in Unit Tests
Mock the `Agent` class to avoid hitting Bedrock in unit tests:
```python
from unittest.mock import MagicMock, patch

def test_my_agent_logic() -> None:
    with patch("my_strands_agents.my_module.Agent") as mock_agent_class:
        mock_instance = MagicMock()
        mock_agent_class.return_value = mock_instance
        # ... test your code
```

## Project Structure

```
strands-agents/
├── src/
│   └── my_strands_agents/      # Main package
│       ├── __init__.py
│       ├── hello_world.py      # Demo: CLI with Typer + Strands Agent
│       └── py.typed            # PEP 561 type stub marker
├── tests/
│   ├── conftest.py             # Shared fixtures
│   ├── unit/                   # Unit tests (fast, isolated)
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests (AWS Bedrock required)
├── docs/
│   └── CODING_CONVENTIONS.md   # Detailed coding standards
├── .github/
│   └── workflows/ci.yml        # CI/CD pipeline
├── pyproject.toml              # Project config, dependencies, tool settings
├── Makefile                    # Development commands
└── README.md
```

## Dependency Management with UV

```bash
uv sync                        # Install deps from uv.lock (reproducible)
uv add <package>               # Add to dependencies
uv add --dev <package>         # Add to dev dependencies
uv run <command>               # Run in venv (no manual activation needed)
uv python install 3.14         # Install Python 3.14
```

## Common Pitfalls & Solutions

### ❌ Pitfall: Untyped function signatures
```python
def process(data):  # ❌ mypy will fail
    return data.upper()
```
**Solution:**
```python
def process(data: str) -> str:  # ✅
    return data.upper()
```

### ❌ Pitfall: Running commands without `uv run`
```bash
pytest tests/  # ❌ May use wrong Python/venv
```
**Solution:**
```bash
uv run pytest tests/  # ✅
```

### ❌ Pitfall: Calling Bedrock in unit tests
Unit tests must mock `Agent` to avoid real API calls.

## References

- **Strands Agents docs:** https://strandsagents.com/docs/user-guide/quickstart/python/
- **Detailed coding standards:** [docs/CODING_CONVENTIONS.md](docs/CODING_CONVENTIONS.md)
- **UV documentation:** https://docs.astral.sh/uv/
- **Ruff rules:** https://docs.astral.sh/ruff/rules/

---

**Quick Start for AI Agents:**
1. Use `uv run` prefix for all commands
2. Add type hints to everything (except test implementations)
3. Run `make format && make lint` before analysis/commits
4. Maintain 80%+ test coverage
5. Follow three-tier test structure (unit/integration/e2e)
6. Run `make ci` before creating PRs
7. Mock `Agent` in unit tests to avoid Bedrock calls
