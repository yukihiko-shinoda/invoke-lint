"""Tasks of build."""
from typing import cast

from invoke import Collection, Context, Result, task

from invokelint._clean import clean_all

ns = Collection()


@task(clean_all)
def dist(context: Context) -> Result:
    """Builds source and wheel packages into dist/ directory."""
    return cast(Result, context.run("python -m build"))


ns.add_task(dist, default=True)
