"""Paths."""
import os

from invoke import Collection, Context, task

from invokelint.path.filter_duplication import filter_duplication
from invokelint.path.setuptools import Setuptools

setuptools = Setuptools()
SOURCE_DIRS = filter_duplication([package.replace(".", os.sep) for package in setuptools.packages])
TASKS_PY = "tasks.py"
TEST_DIR = "tests"
PYTHON_DIRS = [*SOURCE_DIRS, TASKS_PY, TEST_DIR]

ns = Collection()


@task
def debug(_context: Context) -> None:
    """Builds source and wheel packages into dist/ directory."""
    print(f"Packages: {setuptools.packages}")
    print(f"Root packages: {SOURCE_DIRS}")


ns.add_task(debug, default=True)
