"""Tests for `dist` package."""
from invoke import Context
import pytest

from invokelint.dist import dist
from tests.testlibraries import check_result


@pytest.mark.slow
def test_dist(context: Context) -> None:
    check_result(dist(context), "python -m build")
