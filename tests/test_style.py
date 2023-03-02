"""Tests for `style` package."""
from invoke import Context

from invokelint.style import fmt
from tests.testlibraries import check_list_result

LIST_COMMAND_EXPECTED_STYLE = [
    "docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --in-place invokelint tasks.py tests",
    "isort invokelint tasks.py tests",
    "autoflake --recursive --in-place invokelint tasks.py tests",
    "black invokelint tasks.py tests",
]
LIST_COMMAND_EXPECTED_STYLE_CHECK = [
    "docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --check invokelint tasks.py tests",
    "isort --check-only --diff invokelint tasks.py tests",
    "autoflake --recursive --check invokelint tasks.py tests",
    "black --check --diff invokelint tasks.py tests",
]


def test_style(context: Context) -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context), LIST_COMMAND_EXPECTED_STYLE)


def test_style_check(context: Context) -> None:
    """Command should success and run appropriate commands."""
    check_list_result(fmt(context, True), LIST_COMMAND_EXPECTED_STYLE_CHECK)
