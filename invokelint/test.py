"""Tasks of test."""
from pathlib import Path
import webbrowser

from invoke import Collection, Context, Result, task

from invokelint.path import SOURCE_DIRS
from invokelint.run import run_in_pty

ns = Collection()


@task
def fast(context: Context) -> Result:
    """Runs fast tests (not mark @pytest.mark.slow)."""
    # Windows cmd.exe requires to so surround "not slow" by double quote,
    # otherwise, following error raised:
    #   ERROR: file or directory not found: slow'
    # - Answer: cmd - What does single-quoting do in Windows batch files? - Stack Overflow
    #   https://stackoverflow.com/a/24181667/12721873
    return run_in_pty(context, 'pytest -m "not slow" -vv')


ns.add_task(fast, default=True)


@task(name="all")
def run_test_all(context: Context) -> Result:
    """Runs all tests."""
    return run_in_pty(context, "pytest -vv")


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
    # Coverage.py Currently can't apply any options including --source when multiprocessing:
    #   Options affecting multiprocessing must only be specified in a configuration file.
    #   Remove --source from the command line.
    #   Use 'coverage help' for help.
    #   Full documentation is at https://coverage.readthedocs.io
    # command = "coverage run --concurrency=multiprocessing --source {} -m pytest".format(" ".join(SOURCE_DIRS))
    command = "coverage run --source {} -m pytest".format(" ".join(SOURCE_DIRS))
    run_in_pty(context, command)
    # result = run_in_pty(context, "coverage combine")
    result = run_in_pty(context, "coverage report -m")
    if publish:
        # Publish the results via coveralls
        return run_in_pty(context, "coveralls")
    # Build a local report
    if xml:
        result = run_in_pty(context, "coverage xml")
    if html:
        result = run_in_pty(context, "coverage html")
        # as_url() with relative path raises following error:
        #   ValueError: relative path can't be expressed as a file URI
        # Path.absolute() for Python 3.9 or less in Windows.
        # see:
        # - Pathlib absolute() vs. resolve() - Python Help - Discussions on Python.org
        #   https://discuss.python.org/t/pathlib-absolute-vs-resolve/2573/18
        webbrowser.open(Path("index.html").absolute().resolve().as_uri())
    return result


ns.add_task(coverage)
