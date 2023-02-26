"""Tasks of test."""
from pathlib import Path
import platform
from typing import cast
import webbrowser

from invoke import Collection, Context, Result, task

from invokelint.path import SOURCE_DIRS

ns = Collection()


@task
def fast(context: Context) -> Result:
    """Runs fast tests (not mark @pytest.mark.slow)."""
    pty = platform.system() == "Linux"
    return cast(Result, context.run("pytest -m 'not slow' -vv", pty=pty))


ns.add_task(fast, default=True)


@task(name="all")
def run_test_all(context: Context) -> Result:
    """Runs all tests."""
    pty = platform.system() == "Linux"
    return cast(Result, context.run("pytest -vv", pty=pty))


ns.add_task(run_test_all)


@task(
    help={
        "publish": "Publish the result via coveralls",
        "xml": "Export report as xml format",
        "html": "Export report as html format and open it in browser",
    },
    aliases=("cov",),
)
def coverage(context: Context, publish: bool = False, xml: bool = False, html: bool = False) -> Result:
    """Runs all tests and report coverage (options for create xml / html available)."""
    pty = platform.system() == "Linux"
    context.run("coverage run --source {} -m pytest".format(" ".join(SOURCE_DIRS)), pty=pty)
    result = cast(Result, context.run("coverage report -m", pty=pty))
    if publish:
        # Publish the results via coveralls
        return cast(Result, context.run("coveralls", pty=pty))
    # Build a local report
    if xml:
        result = cast(Result, context.run("coverage xml", pty=pty))
    if html:
        result = cast(Result, context.run("coverage html", pty=pty))
        # as_url() with relative path raises following error:
        #   ValueError: relative path can't be expressed as a file URI
        # Path.absolute() for Python 3.9 or less in Windows.
        # see:
        # - Pathlib absolute() vs. resolve() - Python Help - Discussions on Python.org
        #   https://discuss.python.org/t/pathlib-absolute-vs-resolve/2573/18
        webbrowser.open(Path("index.html").absolute().resolve().as_uri())
    return result


ns.add_task(coverage)
