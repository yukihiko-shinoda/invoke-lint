"""Tests for setuptools module."""
from pathlib import Path

from invokelint.path.setuptools import Setuptools


def test() -> None:
    assert Setuptools().project_root == Path(".").absolute().resolve()
