"""Filter duplicated paths."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PairModule:
    """Represents a pair of modules."""

    former: str
    later: str

    def former_is_sub_module_of_later(self) -> bool:
        return self.former.startswith(self.later)

    def later_is_sub_module_of_former(self) -> bool:
        return self.later.startswith(self.former)


class Modules:
    def __init__(self, list_module: list[str]) -> None:
        self.list_module = list_module
        self._list_filtered: list[str] = []

    @property
    def list_roots_only(self) -> list[str]:
        if not self._list_filtered:
            self.filter_out_sub_modules()
        return self._list_filtered

    def filter_out_sub_modules(self) -> None:
        """Filter out sub modules, keeping only the top-level packages."""
        # This function doesn't use comprehension for speed.
        # The base of loop is not the list of argument but new list
        # so the times of loop in the sub function is reduced.
        for module in self.list_module:
            self.append_module_and_unset_any_sub_modules(module)

    def append_module_and_unset_any_sub_modules(self, target_module: str) -> None:
        """Add path and remove any sub modules."""
        for module in self._list_filtered:
            paths = PairModule(target_module, module)
            if paths.former_is_sub_module_of_later():
                return
            if paths.later_is_sub_module_of_former():
                self._list_filtered.remove(module)
                break
        self._list_filtered.append(target_module)
