"""Tests for `style` package."""

from typing import TYPE_CHECKING

from invokelint.style import fmt
from tests.testlibraries import check_list_result

if TYPE_CHECKING:
    from invoke import Context

PYTHON_DIR_EXCLUDING_TEST = "invokelint setup.py tasks.py"
PYTHON_DIR_TEST = "tests"
PYTHON_DIR = f"{PYTHON_DIR_EXCLUDING_TEST} {PYTHON_DIR_TEST}"

LIST_COMMAND_EXPECTED_STYLE_COMMON = [
    f"docformatter --recursive --in-place {PYTHON_DIR}",
    f"autoflake --recursive --in-place {PYTHON_DIR}",
]
LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF = [
    *LIST_COMMAND_EXPECTED_STYLE_COMMON,
    f"isort {PYTHON_DIR}",
    f"black {PYTHON_DIR}",
]
LIST_COMMAND_RUFF_CHECK = [
    f"ruff check --show-fixes {PYTHON_DIR_EXCLUDING_TEST}",
    f"ruff check --show-fixes --ignore S101 {PYTHON_DIR_TEST}",
]
LIST_COMMAND_RUFF_CHECK_FIX = [
    f"ruff check --fix --show-fixes {PYTHON_DIR_EXCLUDING_TEST}",
    f"ruff check --fix --show-fixes --ignore S101 {PYTHON_DIR_TEST}",
]
LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF_BY_RUFF = [
    *LIST_COMMAND_EXPECTED_STYLE_COMMON,
    f"ruff format --diff {PYTHON_DIR}",
    f"ruff format {PYTHON_DIR}",
    *LIST_COMMAND_RUFF_CHECK,
]
LIST_COMMAND_EXPECTED_STYLE = [
    *LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF,
    *LIST_COMMAND_RUFF_CHECK,
    *LIST_COMMAND_RUFF_CHECK_FIX,
]
LIST_COMMAND_EXPECTED_STYLE_BY_RUFF = [
    *LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF_BY_RUFF,
    *LIST_COMMAND_RUFF_CHECK_FIX,
]
LIST_COMMAND_EXPECTED_STYLE_CHECK_COMMON = [
    f"docformatter --recursive --check {PYTHON_DIR}",
    f"autoflake --recursive --check {PYTHON_DIR}",
]
LIST_COMMAND_EXPECTED_STYLE_CHECK = [
    *LIST_COMMAND_EXPECTED_STYLE_CHECK_COMMON,
    f"isort --check-only --diff {PYTHON_DIR}",
    f"black --check --diff {PYTHON_DIR}",
    *LIST_COMMAND_RUFF_CHECK,
]
LIST_COMMAND_EXPECTED_STYLE_CHECK_BY_RUFF = [
    *LIST_COMMAND_EXPECTED_STYLE_CHECK_COMMON,
    f"ruff format --diff {PYTHON_DIR}",
    *LIST_COMMAND_RUFF_CHECK,
]


def test_style(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context), LIST_COMMAND_EXPECTED_STYLE)


def test_style_by_ruff(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, by_ruff=True), LIST_COMMAND_EXPECTED_STYLE_BY_RUFF)


def test_style_check(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, check=True), LIST_COMMAND_EXPECTED_STYLE_CHECK)


def test_style_check_by_ruff(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, check=True, by_ruff=True), LIST_COMMAND_EXPECTED_STYLE_CHECK_BY_RUFF)


def test_style_ruff(context: "Context") -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, ruff=True), LIST_COMMAND_EXPECTED_STYLE_WITHOUT_RUFF)
