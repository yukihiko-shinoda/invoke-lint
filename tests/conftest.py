"""Configuration of pytest."""
from typing import Any, Generator, TYPE_CHECKING

from invoke import Config, Context
import pytest

if TYPE_CHECKING:
    from types import ModuleType

    from pytest_mock import MockerFixture


collect_ignore = ["setup.py"]


@pytest.fixture()
def context() -> Context:
    defaults = Config.global_defaults()  # type: ignore[no-untyped-call]
    defaults["run"]["pty"] = True
    defaults["run"]["in_stream"] = False
    return Context(config=Config(defaults=defaults))


@pytest.fixture()
def _package_build_not_exists(mocker: "MockerFixture") -> Generator[None, None, None]:
    """See:

    - Answer: python - How to mock an import - Stack Overflow
      https://stackoverflow.com/a/18481028/12721873
    """
    # Store original __import__
    orig_import = __import__

    # Reason: To follow specification of original function.
    def import_mock(name: str, *args: Any) -> "ModuleType":
        if name == "build":
            raise ModuleNotFoundError(name)
        return orig_import(name, *args)

    with mocker.patch("builtins.__import__", side_effect=import_mock):
        yield
