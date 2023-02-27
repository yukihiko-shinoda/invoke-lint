"""Tasks of build."""

from invoke import Collection, Context, Result, task

from invokelint._clean import clean_all
from invokelint.run import run_in_pty

ns = Collection()


@task(clean_all)
def dist(context: Context) -> Result:
    """Builds source and wheel packages into dist/ directory."""
    return run_in_pty(context, "python -m build")


ns.add_task(dist, default=True)
