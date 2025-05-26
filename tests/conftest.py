"""Configuration of pytest."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Generator

import pytest
from invoke import Config
from invoke import Context

if TYPE_CHECKING:
    from types import ModuleType

    from pytest_mock import MockerFixture


collect_ignore = ["setup.py"]


@pytest.fixture
def context() -> Context:
    defaults = Config.global_defaults()  # type: ignore[no-untyped-call]
    defaults["run"]["pty"] = True
    defaults["run"]["in_stream"] = False
    return Context(config=Config(defaults=defaults))


@pytest.fixture
def _package_not_exists(mocker: MockerFixture, package_names: list[str]) -> Generator[None, None, None]:
    """See:

    - Answer: python - How to mock an import - Stack Overflow
      https://stackoverflow.com/a/18481028/12721873
    """
    # Store original __import__
    orig_import = __import__

    # Reason: To follow specification of original function.
    def import_mock(name: str, *args: Any) -> ModuleType:
        if name in package_names:
            raise ModuleNotFoundError(name)
        return orig_import(name, *args)

    with mocker.patch("builtins.__import__", side_effect=import_mock):
        yield
