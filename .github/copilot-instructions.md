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

## Python Coding Guidance

Detailed Python conventions and patterns now live in:

- [`.github/instructions/coding-python.instructions.md`](.github/instructions/coding-python.instructions.md)

Use that file for type hints, naming, imports, docstrings, error handling, testing patterns, and style/tool expectations.

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
├── .github/
│   ├── instructions/
│   │   └── coding-python.instructions.md  # Python coding conventions and patterns
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

### ❌ Pitfall: Running commands without `uv run`
```bash
pytest tests/  # ❌ May use wrong Python/venv
```
**Solution:**
```bash
uv run pytest tests/  # ✅
```

## References

- **Strands Agents docs:** https://strandsagents.com/docs/user-guide/quickstart/python/
- **Python coding instructions:** [.github/instructions/coding-python.instructions.md](.github/instructions/coding-python.instructions.md)
- **UV documentation:** https://docs.astral.sh/uv/
- **Ruff rules:** https://docs.astral.sh/ruff/rules/

---

**Quick Start for AI Agents:**
1. Use `uv run` prefix for all commands
2. Follow Python conventions in `.github/instructions/coding-python.instructions.md`
3. Run `make format && make lint` before analysis/commits
4. Maintain 80%+ test coverage
5. Run `make ci` before creating PRs
