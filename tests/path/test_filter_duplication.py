"""Tests for filter_duplication."""

import pytest

from invokelint.path.filter_duplication import Modules
from invokelint.path.filter_duplication import _append_module_and_unset_any_sub_modules
from invokelint.path.filter_duplication import filter_out_sub_modules


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        (Modules("foo.bar", "foo"), True),
        (Modules("foo", "foo.bar"), False),
        (Modules("foo", "bar"), False),
    ],
)
def test_check_former_is_subpath(paths: Modules, *, expected: bool) -> None:
    """Function: former_is_subpath should return appropriate boolean."""
    assert paths.former_is_sub_module_of_later() == expected


@pytest.mark.parametrize(
    ("paths", "expected"),
    [
        (Modules("foo.bar", "foo"), False),
        (Modules("foo", "foo.bar"), True),
        (Modules("foo", "bar"), False),
    ],
)
def test_check_later_is_subpath(paths: Modules, *, expected: bool) -> None:
    """Function: later_is_subpath should return appropriate boolean."""
    assert paths.later_is_sub_module_of_former() == expected


def test_update_list() -> None:
    list_filtered = ["pyvelocity.configurations"]
    _append_module_and_unset_any_sub_modules("pyvelocity", list_filtered)
    assert list_filtered == ["pyvelocity"]


def test_filter_duplication() -> None:
    """Method: filter_duplication() should return only top package."""
    list_path = [
        "pyvelocity",
        "pyvelocity.checks",
        "pyvelocity.configurations",
        "pyvelocity.configurations.files",
        "pyvelocity.configurations.files.sections",
        "pyvelocity.configurations.files.sections.pylint",
        "pyvelocity.configurations.tools",
        "pyvelocity.configurations.files.sections.pylint",
        "pyvelocity.configurations.files.sections",
        "pyvelocity.configurations.files",
        "pyvelocity.checks",
        "pyvelocity.configurations.tools",
        "pyvelocity.configurations",
    ]
    assert filter_out_sub_modules(list_path) == ["pyvelocity"]
