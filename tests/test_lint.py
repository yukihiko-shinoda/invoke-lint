"""Tests for `lint` package."""
from invoke import Context
import pytest

from invokelint.lint import (
    bandit,
    cohesion,
    deep,
    dodgy,
    fast,
    flake8,
    mypy,
    pydocstyle,
    pylint,
    radon,
    radon_cc,
    radon_mi,
    xenon,
)
from tests.test_style import LIST_COMMAND_EXPECTED_STYLE
from tests.testlibraries import check_list_result, check_result

PYTHON_DIR = "invokelint setup.py tasks.py tests"
COMMAND_EXPECTED_RADON_CC = f"radon cc {PYTHON_DIR}"
COMMAND_EXPECTED_RADON_MI = f"radon mi {PYTHON_DIR}"
COMMAND_EXPECTED_BANDIT = "bandit --recursive --skip B101 tests"
COMMAND_EXPECTED_DODGY = "dodgy --ignore-paths csvinput"
COMMAND_EXPECTED_FLAKE8 = f"flake8 --radon-show-closures {PYTHON_DIR}"
COMMAND_EXPECTED_PYDOCSTYLE = f"pydocstyle {PYTHON_DIR}"
COMMAND_EXPECTED_XENON = f"xenon --max-absolute A --max-modules A --max-average A {PYTHON_DIR}"
COMMAND_EXPECTED_MYPY = f"mypy {PYTHON_DIR}"
COMMAND_EXPECTED_PYLINT = f"pylint {PYTHON_DIR}"


def test_radon_cc(context: Context) -> None:
    check_result(radon_cc(context), COMMAND_EXPECTED_RADON_CC)


def test_radon_mi(context: Context) -> None:
    check_result(radon_mi(context), COMMAND_EXPECTED_RADON_MI)


def test_radon(context: Context) -> None:
    list_command_expected = [COMMAND_EXPECTED_RADON_CC, COMMAND_EXPECTED_RADON_MI]
    list_result = radon(context)
    check_list_result(list_result, list_command_expected)


def test_cohesion(context: Context) -> None:
    """Function: cohesion() should run appropriate commands."""
    list_command_expected = [
        "cohesion --directory invokelint",
        "cohesion --directory setup.py",
        "cohesion --directory tasks.py",
        "cohesion --directory tests",
    ]
    list_result = cohesion(context)
    check_list_result(list_result, list_command_expected)


def test_bandit(context: Context) -> None:
    check_result(bandit(context), COMMAND_EXPECTED_BANDIT)


def test_dodgy(context: Context) -> None:
    check_result(dodgy(context), COMMAND_EXPECTED_DODGY)


def test_flake8(context: Context) -> None:
    check_result(flake8(context), COMMAND_EXPECTED_FLAKE8)


def test_pydocstyle(context: Context) -> None:
    check_result(pydocstyle(context), COMMAND_EXPECTED_PYDOCSTYLE)


def test_xenon(context: Context) -> None:
    check_result(xenon(context), COMMAND_EXPECTED_XENON)


LIST_COMMAND_EXPECTED = [
    COMMAND_EXPECTED_BANDIT,
    COMMAND_EXPECTED_DODGY,
    COMMAND_EXPECTED_FLAKE8,
    COMMAND_EXPECTED_PYDOCSTYLE,
    COMMAND_EXPECTED_XENON,
]


def test_fast(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_result = fast(context)
    check_list_result(list_result, LIST_COMMAND_EXPECTED_STYLE + LIST_COMMAND_EXPECTED)


def test_fast_skip_format(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_result = fast(context, True)
    check_list_result(list_result, LIST_COMMAND_EXPECTED)


@pytest.mark.slow
def test_mypy(context: Context) -> None:
    check_result(mypy(context), COMMAND_EXPECTED_MYPY)


@pytest.mark.slow
def test_pylint(context: Context) -> None:
    check_result(pylint(context), COMMAND_EXPECTED_PYLINT)


@pytest.mark.slow
def test_deep(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [COMMAND_EXPECTED_MYPY, COMMAND_EXPECTED_PYLINT]
    list_result = deep(context)
    check_list_result(list_result, list_command_expected)
