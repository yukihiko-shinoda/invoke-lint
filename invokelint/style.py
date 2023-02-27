"""Tasks of format."""
from pathlib import Path
from typing import Any, Dict, List

from invoke import Collection, Context, Result, task
import tomli

from invokelint.path import PYTHON_DIRS
from invokelint.run import run_in_order, run_in_pty

ns = Collection()


def docformatter(context: Context, check: bool = False) -> Result:
    """Runs docformatter.

    This function includes hard coding of line length.
    see:
    - Add pyproject.toml support for config (Issue #10) by weibullguy · Pull Request #77 · PyCQA/docformatter
    https://github.com/PyCQA/docformatter/pull/77
    """
    parsed_toml = tomli.loads(Path("pyproject.toml").read_text("UTF-8"))
    config = parsed_toml["tool"]["docformatter"]
    list_options = build_list_options_docformatter(config, check)
    docformatter_options = " {}".format(" ".join(list_options))
    return run_in_pty(context, "docformatter{} {}".format(docformatter_options, " ".join(PYTHON_DIRS)), warn=True)


# Reason: This is dataclass. pylint: disable=too-few-public-methods
class DocformatterOption:
    def __init__(self, list_str: List[str], enable: bool) -> None:
        self.list_str = list_str
        self.enable = enable


def build_list_options_docformatter(config: Dict[str, Any], check: bool) -> List[str]:
    """Builds list of docformatter options."""
    docformatter_options = (
        DocformatterOption(["--recursive"], "recursive" in config and config["recursive"]),
        DocformatterOption(["--wrap-summaries", str(config["wrap-summaries"])], "wrap-summaries" in config),
        DocformatterOption(["--wrap-descriptions", str(config["wrap-descriptions"])], "wrap-descriptions" in config),
        DocformatterOption(["--check"], check),
        DocformatterOption(["--in-place"], not check),
    )
    return [
        item
        for docformatter_option in docformatter_options
        if docformatter_option.enable
        for item in docformatter_option.list_str
    ]


def autoflake(context: Context, check: bool = False) -> Result:
    """Runs autoflake."""
    autoflake_options = " --recursive {}".format("--check" if check else "--in-place")
    return run_in_pty(context, "autoflake{} {}".format(autoflake_options, " ".join(PYTHON_DIRS)), warn=True)


def isort(context: Context, check: bool = False) -> Result:
    """Runs isort."""
    isort_options = " --check-only --diff" if check else ""
    return run_in_pty(context, "isort{} {}".format(isort_options, " ".join(PYTHON_DIRS)), warn=True)


def black(context: Context, check: bool = False) -> Result:
    """Runs Black."""
    black_options = " --check --diff" if check else ""
    return run_in_pty(context, "black{} {}".format(black_options, " ".join(PYTHON_DIRS)), warn=True)


@task(help={"check": "Checks if source is formatted without applying changes"})
def fmt(context: Context, check: bool = False) -> List[Result]:
    """Formats code by docformatter, isort, autoflake, and Black (option for only check available)."""
    return run_in_order([docformatter, isort, autoflake, black], context, check)


ns.add_task(fmt, default=True)
