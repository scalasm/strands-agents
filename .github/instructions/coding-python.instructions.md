---
description: "Use when creating or modifying Python code. Defines repository Python standards for typing, naming, imports, docstrings, exceptions, testing patterns, and ruff/mypy/pytest-aligned practices."
applyTo: "**/*.py"
---
# Python Coding Instructions

Source of truth for Python code quality conventions in this repository.

## Rule Strength

- MUST: Required for all production-quality changes.
- SHOULD: Strong default; deviate only with a clear reason.

## General Principles

- MUST prefer clear code over clever code.
- MUST be explicit about behavior and intent.
- SHOULD keep solutions simple and maintainable.
- MUST follow existing patterns in the codebase unless there is a justified improvement.

## Type Hints (Mandatory)

- MUST add complete type hints to all function and method signatures.
- MUST use explicit `-> None` for functions with no return value.
- SHOULD use built-in generics (`list`, `dict`, `set`, `tuple`).
- SHOULD use `| None` instead of `Optional[T]` where appropriate.
- SHOULD use abstract collection types from `collections.abc` for interfaces (`Sequence`, `Iterable`, `Mapping`).

Example:

```python
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def first_item(items: Sequence[T]) -> T | None:
    """Return the first item or None if empty."""
    return items[0] if items else None
```

## Constants And Configuration

- MUST avoid unexplained magic numbers or string literals.
- SHOULD define reusable values as named module-level constants (`UPPER_CASE`).
- SHOULD use structured configuration objects, such as dataclasses, for grouped settings.

## Naming

- MUST use `snake_case` for functions, methods, and variables.
- MUST use `PascalCase` for classes and exception types.
- MUST use `UPPER_CASE_WITH_UNDERSCORES` for constants.
- SHOULD prefix internal/private members with `_`.

## Docstrings

- MUST use Google-style docstrings for public functions, classes, and methods.
- SHOULD include `Args`, `Returns`, and `Raises` sections where relevant.
- MUST document non-obvious behavior and constraints.

## Imports

- MUST organize imports into standard library, third-party, and local groups.
- SHOULD prefer absolute imports over relative imports in application code.
- MUST rely on Ruff for import ordering and normalization.

## Error Handling

- MUST catch specific exception types instead of broad `except:` blocks.
- SHOULD use custom exception classes for domain-specific failures.
- MUST preserve context with `raise NewError(...) from err`.

## Testing Patterns

- MUST keep test names descriptive: `test_<what>_<condition>_<expected_result>`.
- SHOULD use fixtures for shared setup and data.
- MUST avoid real Bedrock calls in unit tests.
- MUST mock `strands.Agent` (or wrappers around it) in unit tests.

Example:

```python
from unittest.mock import MagicMock, patch


def test_agent_logic() -> None:
    with patch("my_strands_agents.my_module.Agent") as mock_agent_class:
        mock_instance = MagicMock()
        mock_agent_class.return_value = mock_instance
        # Assertions here
```

## Tool-Aligned Style

- MUST keep line length within 128 characters.
- MUST use double quotes by default.
- SHOULD keep functions focused and reasonably small.
- SHOULD use `pathlib.Path` for path operations.

## Workflow Expectations

- MUST use `uv run` when invoking Python tooling directly.
- SHOULD validate changes with `make format`, `make lint`, `make type-check`, and relevant tests.
- MUST satisfy CI typing, linting, and coverage gates.
