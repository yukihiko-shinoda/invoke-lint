"""To unify executing ruff from style and from lint."""

from typing import TYPE_CHECKING

from invokelint.path import EXISTING_TEST_PACKAGES, PYTHON_DIRS, PYTHON_DIRS_EXCLUDING_TEST
from invokelint.run import run_in_pty

if TYPE_CHECKING:
    from invoke import Context, Result


def chk(context: "Context", *, fix: bool = False, show_fixes: bool = False, warn: bool = False) -> list["Result"]:
    """Lints code with Ruff."""
    list_options = []
    if fix:
        list_options.append("--fix")
    if show_fixes:
        list_options.append("--show-fixes")
    options = " " + " ".join(list_options) if list_options else ""
    result = []
    command = "ruff check{} {}".format(options, " ".join(PYTHON_DIRS_EXCLUDING_TEST))
    result.append(run_in_pty(context, command, warn=warn))
    command = "ruff check{} --ignore S101 {}".format(options, " ".join(EXISTING_TEST_PACKAGES))
    result.append(run_in_pty(context, command, warn=warn))
    return result


def fmt(context: "Context", *, diff: bool = False, warn: bool = False) -> list["Result"]:
    """Lints code with Ruff."""
    list_options = []
    if diff:
        list_options.append("--diff")
    options = " " + " ".join(list_options) if list_options else ""
    return [run_in_pty(context, "ruff format{} {}".format(options, " ".join(PYTHON_DIRS)), warn=warn)]
