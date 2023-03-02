"""Tests for path modules."""
from textwrap import dedent

from invoke import Context
from pytest import CaptureFixture

from invokelint.path import debug


def test(context: Context, capsys: CaptureFixture[str]) -> None:
    """Function: debug() should print packages and root packages."""
    expected = dedent(
        """\
            Setuptools detected packages: ['invokelint', 'invokelint.path']
            Root packages: ['invokelint']
            Setuptools detected Python modules: ['tasks', 'setup']
            Existing test packages: ['tests']
            Python file or directories to lint: ['invokelint', 'tasks.py', 'setup.py', 'tests']
            Python file or directories to lint excluding test packages: ['invokelint', 'tasks.py', 'setup.py']
        """
    )
    debug(context)
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""
