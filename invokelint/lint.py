"""Tasks of lint."""
import platform
from typing import Any, cast, List, TYPE_CHECKING

from invoke import Collection, Context, Result, task

from invokelint.path import EXISTING_TEST_PACKAGES, PYTHON_DIRS, PYTHON_DIRS_EXCLUDING_TEST
from invokelint.run import run_all, run_in_order, run_in_pty
from invokelint.style import fmt

if TYPE_CHECKING:
    from invokelint.run import TaskFunction

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
def cohesion(context: Context) -> List[Result]:
    """Lints code with Cohesion."""
    # 2021-10-24:
    # Cohesion doesn't support multiple directories in 1 command.
    # Only the last directory enables when supply multiple --directory options.
    list_result = []
    for directory in PYTHON_DIRS:
        list_result.append(run_in_pty(context, "cohesion --directory {}".format(directory)))
    return list_result


ns.add_task(cohesion)


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def ruff(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with Ruff."""
    run_in_pty(context, "ruff {}".format(" ".join(PYTHON_DIRS_EXCLUDING_TEST)))
    return run_in_pty(context, "ruff --ignore S101 {}".format(" ".join(EXISTING_TEST_PACKAGES)))


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def bandit(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with bandit."""
    space = " "
    run_in_pty(context, "bandit --recursive {}".format(space.join(PYTHON_DIRS_EXCLUDING_TEST)))
    return run_in_pty(context, "bandit --recursive --skip B101 {}".format(space.join(EXISTING_TEST_PACKAGES)))


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def dodgy(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with dodgy."""
    return run_in_pty(context, "dodgy --ignore-paths csvinput")


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def flake8(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with flake8."""
    return run_in_pty(context, "flake8 {} {}".format("--radon-show-closures", " ".join(PYTHON_DIRS)))


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def pydocstyle(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with pydocstyle."""
    return run_in_pty(context, "pydocstyle {}".format(" ".join(PYTHON_DIRS)))


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def xenon(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Checks code complexity."""
    command = ("xenon --max-absolute A --max-modules A --max-average A {}").format(" ".join(PYTHON_DIRS))
    return run_in_pty(context, command)


@task(help={"skip_format": "Lints without format style."})
def fast(context: Context, *, skip_format: bool = False) -> List[Result]:
    """Runs fast linting (ruff, bandit, dodgy, flake8, pydocstyle, xenon)."""
    list_result = [] if skip_format else fmt(context)
    list_result.extend(run_in_order([ruff, bandit, dodgy, flake8, pydocstyle, xenon], context))
    return list_result


ns.add_task(ruff)
ns.add_task(bandit)
ns.add_task(dodgy)
ns.add_task(flake8)
ns.add_task(pydocstyle)
ns.add_task(xenon)
ns.add_task(fast, default=True)


@task
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def mypy(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with mypy."""
    return run_in_pty(context, "mypy {}".format(" ".join(PYTHON_DIRS)))


@task
# Reason: Compatibility with semgrep task to be called from deep(). pylint: disable=unused-argument
def pylint(context: Context, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with Pylint."""
    return run_in_pty(context, "pylint {}".format(" ".join(PYTHON_DIRS)))


@task(help={"ci": "Run as CI mode."})
# Reason: Compatibility with semgrep task to be called from deep().. pylint: disable=unused-argument
def semgrep(context: Context, *, ci: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    """Lints code with Semgrep."""
    command = "ci" if ci else "scan"
    return run_in_pty(
        context,
        "semgrep {} --config auto --include {}".format(command, " --include ".join(PYTHON_DIRS)),
    )


@task(help={"ci": "Run as CI mode."})
def deep(context: Context, *, ci: bool = False) -> List[Result]:
    """Runs slow but detailed linting (mypy, Pylint, semgrep)."""
    list_task: "List[TaskFunction]" = [mypy, pylint]
    if platform.system() != "Windows":
        list_task.append(semgrep)
    return run_in_order(list_task, context, ci=ci)


ns.add_task(mypy)
ns.add_task(pylint)
ns.add_task(semgrep)
ns.add_task(deep)
