"""Configuration of pytest."""
from invoke import Config, Context
import pytest

collect_ignore = ["setup.py"]


@pytest.fixture
def context() -> Context:
    defaults = Config.global_defaults()  # type: ignore[no-untyped-call]
    defaults["run"]["pty"] = True
    defaults["run"]["in_stream"] = False
    return Context(config=Config(defaults=defaults))
