"""Tests for setuptools module."""

from pathlib import Path

from invokelint.path.setuptools import Setuptools


class TestSetuptools:
    """Tests for Setuptools."""

    def test_project_root(self) -> None:
        assert Setuptools().project_root == Path().absolute().resolve()

    def test_find_py_modules(self) -> None:
        expected = ["invokelint"]
        setuptools = Setuptools()
        setuptools.config_discovery.dist.py_modules = expected
        assert setuptools.find_py_modules([]) == expected
