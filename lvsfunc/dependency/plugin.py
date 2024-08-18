from functools import wraps
from typing import Any, Callable, Literal

from vstools import FuncExceptT, core

from .exceptions import MissingPluginsError
from .types import DEP_URL, F

__all__: list[str] = [
    'check_installed_plugins',
    'required_plugins'
]


def check_installed_plugins(
    plugins: list[str] | dict[str, DEP_URL] = [],
    strict: bool = True,
    func_except: FuncExceptT | None = None
) -> Literal[True] | list[str]:
    """
    Check if the given plugins are installed.

    Example usage:

    .. code-block:: python

        >>> check_installed_plugins(['resize', 'descale'])

        >>> check_installed_plugins({'descale': 'https://github.com/Jaded-Encoding-Thaumaturgy/vapoursynth-descale'})

    :param plugins:         A list of plugins to check for. If a dict is passed,
                            the values are treated as URLs to download the plugin.
    :param strict:          If True, raises an error if any of the plugins are missing.
                            Default: True.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                True if all plugins are installed if strict=False, else raises an error.
                            If strict=False and plugins are missing, returns a list of missing plugins.
    """

    if not plugins:
        return True

    missing = [
        f"{plugin} ({plugins[plugin]})" if isinstance(plugins, dict) else plugin
        for plugin in (plugins.keys() if isinstance(plugins, dict) else plugins)
        if not hasattr(core, plugin)
    ]

    if not missing:
        return True

    if not strict:
        return missing

    raise MissingPluginsError(func_except or check_installed_plugins, missing, reason=f"{strict=}")


def required_plugins(
    plugins: list[str] | dict[str, DEP_URL] = [],
    strict: bool = True,
    func_except: FuncExceptT | None = None
) -> Callable[[F], F]:
    """
    Decorator to ensure that specified plugins are installed.

    Example usage:

    .. code-block:: python

        >>> @required_plugins(['resize', 'descale'])
        ... def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

        >>> @required_plugins({'descale': 'https://github.com/Jaded-Encoding-Thaumaturgy/vapoursynth-descale'})
        ... def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

    For more information, see :py:func:`check_installed_plugins`.

    :param plugins:         A list of plugins to check for. If a dict is passed,
                            the values are treated as URLs to download the plugin.
    :param strict:          If True, raises an error if any of the plugins are missing.
                            Default: True.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            check_installed_plugins(plugins, strict, func_except or required_plugins)

            return func(*args, **kwargs)

        return wrapper  # type:ignore

    return decorator
