from functools import wraps
from typing import Any, Callable

from vstools import FuncExceptT, core, fallback

from .exceptions import MissingPluginsError
from .types import DEP_URL, F

__all__: list[str] = [
    'check_installed_plugins',
    'required_plugins'
]


def check_installed_plugins(
    plugins: str | list[str] | dict[str, DEP_URL] = [],
    strict: bool = True,
    func_except: FuncExceptT | None = None
) -> list[str]:
    """
    Check if the given plugins are installed.

    Example usage:

    .. code-block:: python

        >>> check_installed_plugins(['resize', 'descale'])

        >>> check_installed_plugins({'descale': 'https://github.com/Jaded-Encoding-Thaumaturgy/vapoursynth-descale'})

        >>> if check_installed_plugins(['resize', 'descale'], strict=False):
        ...     print('Missing plugins!')

    :param plugins:         A list of plugins to check for. If a dict is passed,
                            the values are treated as URLs to download the plugin.
    :param strict:          If True, raises an error if any of the plugins are missing.
                            Default: True.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                A list of all missing plugins if strict=False, else raises an error.
    """

    if not plugins:
        return list[str]()

    if isinstance(plugins, str):
        plugins = [plugins]

    missing = [
        f"{plugin} ({plugins[plugin]})" if isinstance(plugins, dict) else plugin
        for plugin in (plugins.keys() if isinstance(plugins, dict) else plugins)
        if not hasattr(core, plugin)
    ]

    if not missing or not strict:
        return missing

    raise MissingPluginsError(fallback(func_except, check_installed_plugins), missing, reason=f"{strict=}")


def required_plugins(
    plugins: list[str] | dict[str, DEP_URL] = [],
    func_except: FuncExceptT | None = None
) -> Callable[[F], F]:
    """
    Decorator to ensure that specified plugins are installed.

    The list of plugins will be stored in the function's `required_plugins` attribute.

    Example usage:

    .. code-block:: python

        >>> @required_plugins(['resize', 'descale'])
        >>> def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

        >>> print(func.required_plugins)
        ... ['resize', 'descale']

        >>> @required_plugins({'descale': 'https://github.com/Jaded-Encoding-Thaumaturgy/vapoursynth-descale'})
        >>> def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

    For more information, see :py:func:`check_installed_plugins`.

    :param plugins:         A list of plugins to check for. If a dict is passed,
                            the values are treated as URLs to download the plugin.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            check_installed_plugins(plugins, True, fallback(func_except, func))
            func.required_plugins = plugins  # type:ignore

            return func(*args, **kwargs)

        return wrapper  # type:ignore

    return decorator
