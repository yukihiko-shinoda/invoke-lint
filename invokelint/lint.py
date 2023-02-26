"""Tasks of lint."""
from typing import cast, List

from invoke import Collection, Context, Result, task

from invokelint.path import PYTHON_DIRS, SOURCE_DIRS, TASKS_PY, TEST_DIR
from invokelint.run import run_all, run_in_order

ns = Collection()


@task
def radon_cc(context: Context) -> Result:
    """Reports code complexity."""
    return cast(Result, context.run("radon cc {}".format(" ".join(PYTHON_DIRS))))


@task
def radon_mi(context: Context) -> Result:
    """Reports maintainability index."""
    return cast(Result, context.run("radon mi {}".format(" ".join(PYTHON_DIRS))))


@task
def radon(context: Context) -> List[Result]:
    """Reports radon both code complexity and maintainability index."""
    return run_all([radon_cc, radon_mi], context)


ns.add_task(radon_cc)
ns.add_task(radon_mi)
ns.add_task(radon)


@task
def bandit(context: Context) -> Result:
    """Lints code with bandit."""
    space = " "
    context.run("bandit --recursive {}".format(space.join([str(p) for p in [*SOURCE_DIRS, TASKS_PY]])), pty=True)
    return cast(Result, context.run("bandit --recursive --skip B101 {}".format(TEST_DIR), pty=True))


@task
def dodgy(context: Context) -> Result:
    """Lints code with dodgy."""
    return cast(Result, context.run("dodgy --ignore-paths csvinput", pty=True))


@task
def flake8(context: Context) -> Result:
    """Lints code with flake8."""
    return cast(Result, context.run("flake8 {} {}".format("--radon-show-closures", " ".join(PYTHON_DIRS))))


@task
def pydocstyle(context: Context) -> Result:
    """Lints code with pydocstyle."""
    return cast(Result, context.run("pydocstyle .", pty=True))


@task
def xenon(context: Context) -> Result:
    """Checks code complexity."""
    command = ("xenon" " --max-absolute A" "--max-modules A" "--max-average A" "{}").format(" ".join(PYTHON_DIRS))
    return cast(Result, context.run(command))


@task
def fast(context: Context) -> List[Result]:
    """Runs fast linting (bandit, dodgy, flake8, pydocstyle, xenon)."""
    return run_in_order([bandit, dodgy, flake8, pydocstyle, xenon], context)


ns.add_task(bandit)
ns.add_task(dodgy)
ns.add_task(flake8)
ns.add_task(pydocstyle)
ns.add_task(xenon)
ns.add_task(fast, default=True)


@task
def mypy(context: Context) -> Result:
    """Lints code with mypy."""
    return cast(Result, context.run("mypy {}".format(" ".join(PYTHON_DIRS))))


@task
def pylint(context: Context) -> Result:
    """Lints code with Pylint."""
    return cast(Result, context.run("pylint {}".format(" ".join(PYTHON_DIRS))))


@task
def deep(context: Context) -> List[Result]:
    """Runs slow but detailed linting (mypy, Pylint)."""
    return run_in_order([mypy, pylint], context)


ns.add_task(mypy)
ns.add_task(pylint)
ns.add_task(deep)
