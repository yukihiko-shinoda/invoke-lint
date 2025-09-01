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
  - **_clean.py**: Cleanup tasks
  - **path/**: Path discovery system using setuptools integration
    - **setuptools.py**: Setuptools integration for package discovery
    - **packages.py**: Package handling utilities
  - **run.py**: Task execution utilities with platform compatibility
  - **ruff.py**: Ruff-specific command implementations

### Path Discovery System
The package uses a sophisticated path discovery system that integrates with setuptools to automatically detect:
- Production packages from setuptools configuration
- Test directories and modules 
- Additional directories to lint (examples, scripts, tools, etc.)
- Python files in the project root (setup.py, tasks.py, etc.)

Key path constants:
- `PRODUCTION_PACKAGES`: Root packages for production code
- `PYTHON_DIRS`: All Python directories/files to process
- `PYTHON_DIRS_EXCLUDING_TEST`: Production code only

### Task Organization
Tasks are organized into collections that can be namespaced:
- **lint**: Fast linters (Xenon, Ruff, Bandit, dodgy, Flake8, pydocstyle)
- **lint.deep**: Slow but thorough linters (mypy, Pylint, Semgrep)
- **style**: Code formatting with Ruff (default) or legacy tools
- **test**: Fast tests, coverage, and reporting
- **dist**: Package building
- **path**: Path discovery debugging

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

# Run fast linters
uv run inv lint

# Run comprehensive linters (slow)
uv run inv lint.deep

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
bump2version patch  # or minor, major
git push --tags
```

## Tool Configuration

The project uses pyproject.toml for all tool configurations:
- **Ruff**: Line length 119, comprehensive rule set with specific ignores
- **Black**: Line length 119 (legacy mode)
- **Flake8**: Compatible with Black, max line length 108
- **mypy**: Strict mode enabled
- **Pylint**: Minimal public methods = 1, max line length 119
- **Coverage**: Excludes TYPE_CHECKING blocks and NotImplementedError
- **pytest**: Uses markers for slow tests

## Platform Compatibility

The codebase includes Windows compatibility considerations:
- PTY handling differs between Windows and Unix systems
- Command quoting strategies for different shells
- Path separators handled via os.sep

## Key Design Patterns

1. **Task Collections**: Each module exports a Collection (ns) that can be imported and namespaced
2. **Result Aggregation**: Tasks return list[Result] for consistent handling
3. **Error Handling**: Uses run_all() vs run_in_order() for different failure behaviors
4. **Platform Detection**: Conditional logic for Windows vs Unix environments
5. **Setuptools Integration**: Automatic discovery of packages and modules to process