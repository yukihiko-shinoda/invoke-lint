"""Tests for `dist` package."""

from typing import TYPE_CHECKING

import pytest

from invokelint.dist import dist, module_build_exists
from tests.testlibraries import check_result

if TYPE_CHECKING:
    from invoke import Context


@pytest.mark.usefixtures("_package_build_not_exists")
def test_module_build_exists() -> None:
    """Function: module_build_exists() should return False if fail to import build module."""
    assert not module_build_exists()


@pytest.mark.slow()
def test_dist_build(context: "Context") -> None:
    check_result(dist(context), "python -m build")


@pytest.mark.slow()
@pytest.mark.usefixtures("_package_build_not_exists")
def test_dist_setup_py(context: "Context") -> None:
    check_result(dist(context), "python setup.py bdist_wheel")
