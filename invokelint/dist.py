"""Tasks of build."""

from invoke import Collection, Context, Result, task

from invokelint._clean import clean_all
from invokelint.run import run_in_pty

ns = Collection()


def module_build_exists() -> bool:
    """To minimize try block."""
    try:
        # Reason:
        #   F401: Just check existence, use it via command line.
        #   RUF100: Ruff 0.0.254 started to report that unused: `F401`,
        #           however Flake8 running in Python still requires `F401`.
        import build  # noqa: F401,RUF100 pylint: disable=import-outside-toplevel,unused-import
    except ModuleNotFoundError:
        return False
    return True


@task(clean_all)
def dist(context: Context) -> Result:
    """Builds source and wheel packages into dist/ directory."""
    if module_build_exists():
        return run_in_pty(context, "python -m build")
    run_in_pty(context, "python setup.py sdist")
    return run_in_pty(context, "python setup.py bdist_wheel")


ns.add_task(dist, default=True)
