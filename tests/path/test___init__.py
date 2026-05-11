"""Tests for path modules."""

from textwrap import dedent
from typing import TYPE_CHECKING

from invokelint.path import debug

if TYPE_CHECKING:
    import pytest
    from invoke import Context


def test(context: "Context", capsys: "pytest.CaptureFixture[str]") -> None:
    """Function: debug() should print packages and root packages."""
    # Reason: Black <=23.x (Python 3.9-) splits closing `"""` onto its own line, triggering ruff COM812.
    # fmt: off
    expected = dedent("""\
        Setuptools detected packages: ['invokelint', 'invokelint.path']
        Root packages: ['invokelint']
        Setuptools detected Python modules: ['setup', 'tasks']
        Existing test packages: ['tests']
        Python file or directories to lint: ['invokelint', 'setup.py', 'tasks.py', 'tests']
        Python file or directories to lint excluding test packages: ['invokelint', 'setup.py', 'tasks.py']
    """)
    # fmt: on
    debug(context)
    captured = capsys.readouterr()
    assert captured.out == expected
    assert not captured.err
