"""Tasks of build."""

from invoke import Collection, Context, Result, task

from invokelint._clean import clean_all
from invokelint.run import run_in_pty

ns = Collection()


def module_build_exists() -> bool:
    """To minimize try block."""
    try:
        # Reason: Just check existence, use it via command line.
        import build  # noqa: F401 pylint: disable=import-outside-toplevel,unused-import

        return True
    except ModuleNotFoundError:
        return False


@task(clean_all)
def dist(context: Context) -> Result:
    """Builds source and wheel packages into dist/ directory."""
    if module_build_exists():
        return run_in_pty(context, "python -m build")
    run_in_pty(context, "python setup.py sdist")
    return run_in_pty(context, "python setup.py bdist_wheel")


ns.add_task(dist, default=True)
