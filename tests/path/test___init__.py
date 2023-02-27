"""Tests for path modules."""
from textwrap import dedent

from invoke import Context
from pytest import CaptureFixture

from invokelint.path import debug


def test(context: Context, capsys: CaptureFixture[str]) -> None:
    """Function: debug() should print packages and root packages."""
    expected = dedent(
        """\
            Packages: ['invokelint', 'invokelint.path']
            Root packages: ['invokelint']
        """
    )
    debug(context)
    captured = capsys.readouterr()
    assert captured.out == expected
    assert captured.err == ""
