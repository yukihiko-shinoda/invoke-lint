# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Invoke Lint is a Python package that orchestrates multiple Python development tools at once. It provides a unified interface via Invoke tasks to run linters, formatters, tests, and build tools for Python projects. The package is designed for both quick developer feedback and comprehensive CI checks.

## Core Architecture

### Module Structure
- **invokelint/**: Main package containing task collections
  - **lint.py**: Linting tasks (fast linters and deep analysis)
  - **style.py**: Code formatting tasks (docformatter, Ruff, autoflake, isort, Black)
  - **test.py**: Testing tasks (fast tests, coverage, HTML reports)
  - **dist.py**: Package building tasks
  - **_clean.py**: Cleanup tasks (exposed as `clean` namespace)
  - **path/**: Path discovery system — a single `__init__.py` that uses the external `packagediscovery` package to detect packages, test dirs, and root Python files
  - **run.py**: Task execution utilities with platform compatibility
  - **ruff.py**: Ruff-specific command implementations shared between lint and style

### Path Discovery System
The package uses `packagediscovery.Setuptools` (external dep) to automatically detect:
- Production packages from setuptools configuration
- Test directories and modules
- Additional directories to lint (examples, scripts, tools, etc.)
- Python files in the project root (setup.py, tasks.py, etc.)

Key path constants (from `invokelint/path/__init__.py`):
- `PRODUCTION_PACKAGES`: Root packages for production code
- `PYTHON_DIRS`: All Python directories/files to process
- `PYTHON_DIRS_EXCLUDING_TEST`: Production code only

### Task Organization
Tasks are organized into Invoke Collections (each module exports `ns`):
- **lint** (default: `fast`): Runs format then fast linters (Xenon, Ruff, Bandit, dodgy, Flake8). `lint.deep` runs mypy, Pylint, Semgrep. `lint.radon` reports complexity and maintainability index.
- **style** (default: `fmt`): Code formatting with Ruff (default) or legacy tools
- **test** (default: `fast`): Fast tests, `test.all` for all, `test.coverage`/`test.cov` for coverage
- **clean** (default: `all`): Removes build artifacts, pyc files, coverage data
- **dist**: Package building
- **path** (default: `debug`): Path discovery inspection

### Key Design Patterns
1. **Task Collections**: Each module exports a `ns = Collection()` and adds tasks to it, then `tasks.py` assembles them with namespace names
2. **Result Aggregation**: Tasks return `list[Result]` for consistent handling
3. **Error Handling**: `run_all()` runs all tasks even on failure; `run_in_order()` stops on first failure
4. **Platform Detection**: `run_in_pty()` enables PTY on non-Windows; `semgrep` is skipped on Windows
5. **Wrapper functions**: `call_*` wrapper functions (e.g. `call_xenon`) exist to normalize `**kwargs` for use in `run_in_order()` / `run_all()` task lists

## Development Commands

### Setup
```bash
uv sync                    # Install dependencies
source .venv/bin/activate  # Activate virtual environment
```

### Core Development Tasks
```bash
# Format code (uses Ruff by default)
uv run inv style

# Check formatting without changes
uv run inv style --check

# Use legacy formatters instead of Ruff
uv run inv style --no-ruff

# Run fast linters (also runs format first by default)
uv run inv lint

# Run fast linters without running format first
uv run inv lint --skip-format

# Enable pydocstyle in fast lint
uv run inv lint --pydocstyle

# Run comprehensive linters (slow)
uv run inv lint.deep

# Report code complexity and maintainability index (radon)
uv run inv lint.radon

# Run fast tests only (not marked @pytest.mark.slow)
uv run inv test

# Run all tests
uv run inv test.all

# Run tests with coverage
uv run inv test.cov

# Generate HTML coverage report
uv run inv test.cov --html

# Build distribution packages
uv run inv dist

# Clean build artifacts
uv run inv clean

# Debug path discovery
uv run inv path
```

### Single Test Execution
```bash
# Run specific test file
uv run pytest tests/test_lint.py -vv

# Run with specific markers
uv run pytest -m "not slow" -vv

# Run single test method
uv run pytest tests/test_lint.py::TestLint::test_method -vv
```

### Version Management
```bash
# Bump version (uses bump-my-version)
bump-my-version bump patch  # or minor, major
git push --tags
```

## Pip Extras

The package exposes optional dependency groups via `[project.optional-dependencies]` so consumers can install only what they need:

| Extra | Tools installed |
| --- | --- |
| `lint` | Ruff, Bandit, Cohesion, dodgy, Flake8 + plugins |
| `lint-deep` | mypy, Pylint, Semgrep |
| `style` | docformatter, Ruff |
| `style-legacy` | autoflake, Black, isort, pydocstyle |
| `test` | pytest, Coverage.py |
| `dist` | build |
| `xenon` | Xenon, radon |
| `basic` | Alias for `lint + lint-deep + style + test + dist` |

The project's own `dev` dependency group installs itself with all extras:

```text
invokelint[lint,lint-deep,style,style-legacy,test,dist,xenon]
```

## Tool Configuration

The project uses pyproject.toml for all tool configurations:
- **Ruff**: Line length 119, `select = ["ALL"]` with specific ignores, `max-complexity = 5`
- **Black**: Line length 119 (legacy mode)
- **Flake8**: Max line length 108 (B950 replaces E501), compatible with Black
- **mypy**: Strict mode enabled
- **Pylint**: `min-public-methods = 1`, max line length 119, `docstring-min-length = 7`
- **Coverage**: Excludes `TYPE_CHECKING` blocks and `raise NotImplementedError`
- **pytest**: Defines `slow` marker; deselect with `-m "not slow"`
- **Bandit**: `assert_used` skips `tests/*`

## Platform Compatibility

- PTY is enabled on non-Windows only (via `run_in_pty`)
- `semgrep` task is skipped on Windows in `lint.deep`
- `inv dist` does not support Windows
