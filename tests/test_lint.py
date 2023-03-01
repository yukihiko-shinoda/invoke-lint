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
from tests.testlibraries import check_list_result, check_result


def test_radon_cc(context: Context) -> None:
    check_result(radon_cc(context), "radon cc invokelint tasks.py tests")


def test_radon_mi(context: Context) -> None:
    check_result(radon_mi(context), "radon mi invokelint tasks.py tests")


def test_radon(context: Context) -> None:
    list_command_expected = [
        "radon cc invokelint tasks.py tests",
        "radon mi invokelint tasks.py tests",
    ]
    list_result = radon(context)
    check_list_result(list_result, list_command_expected)


def test_cohesion(context: Context) -> None:
    """Function: cohesion() should run appropriate commands."""
    list_command_expected = [
        "cohesion --directory invokelint",
        "cohesion --directory tasks.py",
        "cohesion --directory tests",
    ]
    list_result = cohesion(context)
    check_list_result(list_result, list_command_expected)


def test_bandit(context: Context) -> None:
    check_result(bandit(context), "bandit --recursive --skip B101 tests")


def test_dodgy(context: Context) -> None:
    check_result(dodgy(context), "dodgy --ignore-paths csvinput")


def test_flake8(context: Context) -> None:
    check_result(flake8(context), "flake8 --radon-show-closures invokelint tasks.py tests")


def test_pydocstyle(context: Context) -> None:
    check_result(pydocstyle(context), "pydocstyle invokelint tasks.py tests")


def test_xenon(context: Context) -> None:
    check_result(xenon(context), "xenon --max-absolute A --max-modules A --max-average A invokelint tasks.py tests")


def test_fast(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [
        "bandit --recursive --skip B101 tests",
        "dodgy --ignore-paths csvinput",
        "flake8 --radon-show-closures invokelint tasks.py tests",
        "pydocstyle invokelint tasks.py tests",
        "xenon --max-absolute A --max-modules A --max-average A invokelint tasks.py tests",
    ]
    list_result = fast(context)
    check_list_result(list_result, list_command_expected)


@pytest.mark.slow
def test_pylint(context: Context) -> None:
    check_result(pylint(context), "pylint invokelint tasks.py tests")


@pytest.mark.slow
def test_mypy(context: Context) -> None:
    check_result(mypy(context), "mypy invokelint tasks.py tests")


@pytest.mark.slow
def test_deep(context: Context) -> None:
    """Command should success and run appropriate commands."""
    list_command_expected = [
        "mypy invokelint tasks.py tests",
        "pylint invokelint tasks.py tests",
    ]
    list_result = deep(context)
    check_list_result(list_result, list_command_expected)
