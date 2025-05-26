"""Test libraries."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from invoke import Result


def check_list_result(list_result: list[Result], list_command_expected: list[str]) -> None:
    """Checks the results of a list of commands against expected commands."""
    assert len(list_result) == len(
        list_command_expected,
    ), "len(list_result): {}, len(list_command_expected): {}, \nresult.command:\n{}\ncommand_expected:\n{}".format(
        len(list_result),
        len(list_command_expected),
        "\n".join(result.command for result in list_result),
        "\n".join(command for command in list_command_expected),
    )
    for result, command_expected in zip(list_result, list_command_expected):
        check_result(result, command_expected)


def check_result(result: Result, command_expected: str) -> None:
    assert result.ok
    assert result.exited == 0
    assert result.command == command_expected, build_message(result, command_expected)


def build_message(result: Result, command_expected: str) -> str:
    """Builds a message for debug."""
    return (
        f"result.command: {result.command}, "
        f"command_expected: {command_expected}, "
        f"result.stdout: {result.stdout}, "
        f"result.stderr: {result.stderr}"
    )
