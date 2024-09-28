import inspect

from vstools import CustomKeyError

__all__: list[str] = [
    'get_full_caller_stack',

    'get_caller_chain',

    'format_caller_stack',

    'get_caller_info',

    'summarize_stack',
]


def _remove_caller_formatting(stack: list[str]) -> list[str]:
    """
    Remove caller formatting functions from the stack.

    :param stack:   The original stack trace.

    :return:        A new stack trace with caller formatting functions removed.
    """

    current_module = inspect.getmodule(inspect.currentframe())

    if current_module:
        module_functions = [
            name for name, obj in inspect.getmembers(current_module)
            if inspect.isfunction(obj) and obj.__module__ == current_module.__name__
        ]
        return [
            caller for caller in stack
            if caller.split()[0] not in module_functions
        ]

    return stack


def get_full_caller_stack() -> list[str]:
    """
    Get a full stack of callers, excluding the current function.

    :return:    A list of strings representing the call stack, with each entry
                containing the function name, filename, and line number.
    """

    stack = []
    frame = inspect.currentframe()

    if frame:
        frame = frame.f_back

    while frame:
        caller_info = inspect.getframeinfo(frame)
        stack.append(f'{caller_info.function} in {caller_info.filename}:{caller_info.lineno}')
        frame = frame.f_back

    return stack


def get_caller_chain() -> str:
    """
    Get a chain of caller function names.

    :return:    A string representing the call chain with function names
                connected by arrows.
    """

    stack = get_full_caller_stack()
    function_names = [caller.split()[0] for caller in stack]

    return '→'.join(reversed(function_names))


def format_caller_stack(max_depth: int | None = None, include_line_numbers: bool = True) -> str:
    """
    Format the caller stack into a readable string.

    :param max_depth:               Maximum depth of the stack to display. If None, shows full stack.
    :param include_line_numbers:    Whether to include line numbers in the output.

    :return:                        A formatted string representing the call stack.
    """

    stack = _remove_caller_formatting(get_full_caller_stack())

    if max_depth is not None:
        stack = stack[:max_depth]

    max_depth = len(stack)

    formatted_stack = []

    for i, caller in enumerate(reversed(stack), 1):
        parts = caller.split(' in ')

        func_name = parts[0]
        location = parts[1] if include_line_numbers else parts[1].split(':')[0]

        formatted_stack.append(f'{i:0{len(str(max_depth))}d}. {func_name} - {location}')

    return '\n'.join(formatted_stack)


def get_caller_info(depth: int = 1) -> str:
    """
    Get information about a specific caller in the stack.

    :param depth:       The depth of the caller in the stack (1 is the immediate caller).

    :return:            A string with information about the specified caller.

    :raises CustomKeyError:     Invalid depth provided.
    """

    stack = _remove_caller_formatting(get_full_caller_stack())

    if depth < 1 or depth > len(stack):
        raise CustomKeyError(f'Invalid depth: {depth}. Stack depth is {len(stack)}', get_caller_info)

    caller = stack[depth - 1]
    parts = caller.split(' in ')

    return f'Caller at depth {depth}: {parts[0]} - {parts[1]}'


def summarize_stack(include_line_numbers: bool = False) -> str:
    """
    Provide a summary of the call stack.

    :param include_line_numbers:    Whether to include line numbers in the output.

    :return:                        A string summarizing the call stack.
    """

    stack = _remove_caller_formatting(get_full_caller_stack())

    total_calls = len(stack)
    unique_functions = len(set(caller.split()[0] for caller in stack))

    summary = f'Total function calls: {total_calls}\n'
    summary += f'Unique functions called: {unique_functions}\n'
    summary += f'Deepest call: {stack[0].split()[0]}\n'
    summary += f'Entry point: {stack[-1].split()[0]}'

    if include_line_numbers:
        summary += f' at {stack[-1].split(":")[-1]}'

    return summary
