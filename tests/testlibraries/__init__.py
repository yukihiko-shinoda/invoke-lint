"""Test libraries."""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from invoke import Result


def check_list_result(list_result: "List[Result]", list_command_expected: List[str]) -> None:
    assert len(list_result) == len(
        list_command_expected,
    ), "len(list_result): {}, len(list_command_expected): {}".format(len(list_result), len(list_command_expected))
    for result, command_expected in zip(list_result, list_command_expected):
        check_result(result, command_expected)


def check_result(result: "Result", command_expected: str) -> None:
    assert result.ok
    assert result.exited == 0
    assert result.command == command_expected, "result.command: {}, command_expected: {}".format(
        result.command,
        command_expected,
    )
