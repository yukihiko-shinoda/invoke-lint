"""Tasks of format."""
from contextlib import suppress
from pathlib import Path
from typing import Any, Dict, List

from invoke import Collection, Context, Result, task, UnexpectedExit
import tomli

from invokelint.path import PYTHON_DIRS
from invokelint.ruff import execute
from invokelint.run import run_in_order, run_in_pty

ns = Collection()


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def docformatter(context: Context, *, check: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
    https://github.com/PyCQA/docformatter/pull/77
    """
    parsed_toml = tomli.loads(Path("pyproject.toml").read_text("UTF-8"))
    config = parsed_toml["tool"]["docformatter"]
    list_options = build_list_options_docformatter(config, check=check)
    docformatter_options = " {}".format(" ".join(list_options))
    return run_in_pty(context, "docformatter{} {}".format(docformatter_options, " ".join(PYTHON_DIRS)), warn=True)


# Reason: This is dataclass. pylint: disable=too-few-public-methods
class DocformatterOption:
    def __init__(self, list_str: List[str], *, enable: bool) -> None:
        self.list_str = list_str
        self.enable = enable


def build_list_options_docformatter(config: Dict[str, Any], *, check: bool) -> List[str]:
    """Builds list of docformatter options."""
    docformatter_options = (
        DocformatterOption(["--recursive"], enable="recursive" in config and config["recursive"]),
        DocformatterOption(["--wrap-summaries", str(config["wrap-summaries"])], enable="wrap-summaries" in config),
        DocformatterOption(
            ["--wrap-descriptions", str(config["wrap-descriptions"])],
            enable="wrap-descriptions" in config,
        ),
        DocformatterOption(["--check"], enable=check),
        DocformatterOption(["--in-place"], enable=not check),
    )
    return [
        item
        for docformatter_option in docformatter_options
        if docformatter_option.enable
        for item in docformatter_option.list_str
    ]


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def autoflake(context: Context, *, check: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    """Runs autoflake."""
    autoflake_options = " --recursive {}".format("--check" if check else "--in-place")
    return run_in_pty(context, "autoflake{} {}".format(autoflake_options, " ".join(PYTHON_DIRS)), warn=True)


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def isort(context: Context, *, check: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    """Runs isort."""
    isort_options = " --check-only --diff" if check else ""
    return run_in_pty(context, "isort{} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True)


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def black(context: Context, *, check: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    """Runs Black."""
    black_options = " --check --diff" if check else ""
    return run_in_pty(context, "black{} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True)


# Reason: Compatibility with semgrep task to be called from lint.fast().. pylint: disable=unused-argument
def call_ruff(context: Context, *, check: bool = False, **kwargs: Any) -> Result:  # noqa: ARG001
    if check:
        return execute(context, show_fixes=True)
    with suppress(UnexpectedExit):
        execute(context, show_fixes=True)
    return execute(context, fix=True, show_fixes=True)


@task(
    help={
        "check": "Checks if source is formatted without applying changes",
        "ruff": "Fix ruff warnings",
    },
)
def fmt(context: Context, *, check: bool = False, ruff: bool = False) -> List[Result]:
    """Formats code by docformatter, isort, autoflake, and Black (option for only check available)."""
    tasks = [docformatter, isort, autoflake, black]
    if check or ruff:
        tasks.append(call_ruff)
    return run_in_order(tasks, context, check=check)


ns.add_task(fmt, default=True)
