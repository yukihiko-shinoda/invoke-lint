"""Tests for `style` package."""
from invoke import Context

from invokelint.style import fmt
from tests.testlibraries import check_list_result

PYTHON_DIR = "invokelint setup.py tasks.py tests"

LIST_COMMAND_EXPECTED_STYLE = [
    f"docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --in-place {PYTHON_DIR}",
    f"isort {PYTHON_DIR}",
    f"autoflake --recursive --in-place {PYTHON_DIR}",
    f"black {PYTHON_DIR}",
]
LIST_COMMAND_EXPECTED_STYLE_CHECK = [
    f"docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --check {PYTHON_DIR}",
    f"isort --check-only --diff {PYTHON_DIR}",
    f"autoflake --recursive --check {PYTHON_DIR}",
    f"black --check --diff {PYTHON_DIR}",
]


def test_style(context: Context) -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context), LIST_COMMAND_EXPECTED_STYLE)


def test_style_check(context: Context) -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, True), LIST_COMMAND_EXPECTED_STYLE_CHECK)
