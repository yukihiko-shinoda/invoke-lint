"""Tests for `style` package."""
from invoke import Context

from invokelint.style import fmt
from tests.testlibraries import check_list_result


def test_style(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [
        "docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --in-place invokelint tasks.py tests",
        "isort invokelint tasks.py tests",
        "autoflake --recursive --in-place invokelint tasks.py tests",
        "black invokelint tasks.py tests",
    ]
    check_list_result(fmt(context), list_command_expected)


def test_style_check(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [
        "docformatter --recursive --wrap-summaries 119 --wrap-descriptions 119 --check invokelint tasks.py tests",
        "isort --check-only --diff invokelint tasks.py tests",
        "autoflake --recursive --check invokelint tasks.py tests",
        "black --check --diff invokelint tasks.py tests",
    ]
    check_list_result(fmt(context, True), list_command_expected)
