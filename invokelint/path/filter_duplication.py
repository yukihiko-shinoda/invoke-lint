"""Filter duplicated paths."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Modules:
    """Represents a pair of modules."""

    former: str
    later: str

    def former_is_sub_module_of_later(self) -> bool:
        return self.former.startswith(self.later)

    def later_is_sub_module_of_former(self) -> bool:
        return self.later.startswith(self.former)


def _append_module_and_unset_any_sub_modules(target_module: str, list_module: list[str]) -> None:
    """Add path and remove any sub modules."""
    for module in list_module:
        paths = Modules(target_module, module)
        if paths.former_is_sub_module_of_later():
            return
        if paths.later_is_sub_module_of_former():
            list_module.remove(module)
            break
    list_module.append(target_module)


def filter_out_sub_modules(list_module: list[str]) -> list[str]:
    """Filter out sub modules, keeping only the top-level packages."""
    # This function doesn't use comprehension for speed.
    # The base of loop is not the list of argument but new list
    # so the times of loop in the sub function is reduced.
    list_filtered: list[str] = []
    for module in list_module:
        _append_module_and_unset_any_sub_modules(module, list_filtered)
    return list_filtered
