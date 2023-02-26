"""Tasks of clean."""
from pathlib import Path
import shutil
import sys
from typing import cast, List

from invoke import Collection, Context, Result, task

from invokelint.run import run_all

ROOT_DIR = Path(__file__).parent
COVERAGE_FILE = ROOT_DIR.joinpath(".coverage")
COVERAGE_DIR = ROOT_DIR.joinpath("htmlcov")

ns = Collection()


@task
def dist(context: Context) -> Result:
    """Cleans up files from package building."""
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    return cast(Result, context.run("find . -name '*.egg' -exec rm -f {} +"))


ns.add_task(dist)


@task
def python(context: Context) -> Result:
    """Cleans up python file artifacts."""
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    return cast(Result, context.run("find . -name '__pycache__' -exec rm -fr {} +"))


ns.add_task(python)


def _delete_file(file: Path) -> None:
    if sys.version_info >= (3, 8):
        return file.unlink(missing_ok=True)
    return _delete_file_legacy(file)  # pragma: no cover


def _delete_file_legacy(file: Path) -> None:  # pragma: no cover
    try:
        file.unlink()
    # Reason: The command doesn't expects file exists.
    except FileNotFoundError:
        pass


@task
def tests(_context: Context) -> Result:
    """Cleans up files from testing."""
    _delete_file(COVERAGE_FILE)
    shutil.rmtree(COVERAGE_DIR, ignore_errors=True)
    return Result()


ns.add_task(tests)


@task(name="all")
def clean_all(context: Context) -> List[Result]:
    """Cleans up all."""
    return run_all([dist, python, tests], context)


ns.add_task(clean_all, default=True)
