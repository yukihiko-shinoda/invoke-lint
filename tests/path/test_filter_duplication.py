"""Tests for filter_duplication."""

import pytest

from invokelint.path.filter_duplication import _check_subpath, _update_list, filter_duplication


@pytest.mark.parametrize(
    "path_a, path_b, expected",
    [
        ("foo.bar", "foo", 1),
        ("foo", "foo.bar", -1),
        ("foo", "bar", 0),
    ],
)
def test_check_subpath(path_a: str, path_b: str, expected: int) -> None:
    """Function: _check_subpath() should return appropriate integer."""
    assert _check_subpath(path_a, path_b) == expected


def test_update_list() -> None:
    list_filtered = ["pyvelocity.configurations"]
    _update_list("pyvelocity", list_filtered)
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
    assert filter_duplication(list_path) == ["pyvelocity"]
