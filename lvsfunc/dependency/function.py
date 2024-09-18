from functools import wraps
from typing import Any, Callable

from vstools import FuncExceptT, core, fallback

from .exceptions import MissingPluginFunctionsError
from .plugin import check_installed_plugins
from .types import F

__all__: list[str] = [
    'check_installed_plugin_functions',
    'required_plugin_functions'
]


def check_installed_plugin_functions(
    plugin: str,
    functions: str | list[str] = [],
    strict: bool = True,
    func_except: FuncExceptT | None = None
) -> list[str]:
    """
    Check if the given plugins are installed.

    Example usage:

    .. code-block:: python

        >>> check_installed_plugin_functions('descale', ['Bicubic', 'Debicubic'])

        >>> if check_installed_plugins('descale', ['Bicubic', 'Debicubic'], strict=False):
        ...     print('Missing functions for plugin! Please update!')

    :param plugin:          The plugin to check.
    :param plugins:         A list of functions to check for.
    :param strict:          If True, raises an error if any of the plugins are missing.
                            Default: True.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                A list of all missing functions if strict=False, else raises an error.
    """

    if not functions:
        return list[str]()

    func = fallback(func_except, check_installed_plugin_functions)

    check_installed_plugins(plugin, True, func)

    if isinstance(functions, str):
        functions = [functions]

    plg = getattr(core, plugin)  # type:ignore

    missing = [
        plugin_func for plugin_func in functions if not hasattr(plg, plugin_func)
    ]

    if not missing or not strict:
        return missing

    raise MissingPluginFunctionsError(func, plugin, missing, reason=f"{strict=}")


def required_plugin_functions(
    plugin: str, functions: list[str] = [],
    func_except: FuncExceptT | None = None
) -> Callable[[F], F]:
    """
    Decorator to ensure that the specified plugin has specific functions.

    The plugin and list of functions will be stored in the function's `required_plugin_functions` attribute.

    Example usage:

    .. code-block:: python

        >>> @required_plugin_functions('descale', ['Bicubic', 'Debicubic'])
        >>> def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

        >>> print(func.required_plugin_functions)
        ... ('descale', ['Bicubic', 'Debicubic'])

    For more information, see :py:func:`check_installed_plugin_functions`.

    :param plugin:          The plugin to check.
    :param functions:       A list of functions to check for.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            check_installed_plugin_functions(plugin, functions, True, fallback(func_except, func))
            func.required_plugin_functions = (plugin, functions)  # type:ignore

            return func(*args, **kwargs)

        return wrapper  # type:ignore

    return decorator
