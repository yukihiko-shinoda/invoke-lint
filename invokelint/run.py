"""Functions to run tasks."""
import platform
from typing import Any, Callable, cast, List

from invoke import Context, Result, UnexpectedExit


def run_in_pty(context: Context, command: str, **kwargs: Any) -> Result:
    return cast(Result, context.run(command, pty=platform.system() != "Windows", **kwargs))


def run_in_order(list_task: List[Callable[[Context], Result]], context: Context, *args: Any) -> List[Result]:
    list_result = []
    for each_task in list_task:
        list_result.append(each_task(context, *args))
    return list_result


def run_all(list_task: List[Callable[[Context], Result]], context: Context) -> List[Result]:
    """Runs all commands even if failure."""
    list_unexpected_exit = []
    list_result = []
    for each_task in list_task:
        try:
            list_result.append(each_task(context))
        except UnexpectedExit as error:
            list_unexpected_exit.append(error)
    if list_unexpected_exit:
        raise list_unexpected_exit[0]
    return list_result
