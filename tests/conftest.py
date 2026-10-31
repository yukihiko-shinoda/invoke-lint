# Copyright (c) 2023 Yukihiko Shinoda
"""Configuration of pytest."""

from __future__ import annotations

import shutil
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
def _semgrep_rules_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SEMGREP_RULES", raising=False)


@pytest.fixture
def _semgrep_rules_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SEMGREP_RULES", "p/python p/secrets")


@pytest.fixture
def _semgrep_not_installed(mocker: MockerFixture) -> None:
    # Store original shutil.which
    orig_which = shutil.which

    # Reason: To follow specification of original function.
    def which_mock(cmd: str, *args: Any, **kwargs: Any) -> str | None:
        return None if cmd == "semgrep" else orig_which(cmd, *args, **kwargs)

    mocker.patch("shutil.which", side_effect=which_mock)


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
