import importlib.util
from functools import wraps
from typing import Any, Callable, Literal

from vstools import FuncExceptT

from .exceptions import MissingPackagesError
from .types import DEP_URL, F

__all__: list[str] = [
    'check_installed_packages',
    'required_packages'
]


def check_installed_packages(
    packages: list[str] | dict[str, DEP_URL] = [],
    strict: bool = True,
    func_except: FuncExceptT | None = None
) -> Literal[True] | list[str]:
    """
    Check if the given packages are installed.

    Example usage:

    .. code-block:: python

        >>> check_installed_packages(['lvsfunc', 'vstools'])

        >>> check_installed_packages({'lvsfunc': 'pip install lvsfunc})

    :param packages:        A list of packages to check for. If a dict is passed,
                            the values are treated as either a URL or a pip command to download the package.
    :param strict:          If True, raises an error if any of the packages are missing.
                            Default: True.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                True if all packages are installed if strict=False, else raises an error.
                            If strict=False and packages are missing, returns a list of missing packages.
    """

    if not packages:
        return True

    packages_to_check, formatter = (
        (packages.keys(), lambda pkg: f"{pkg} ({packages[pkg]})")
        if isinstance(packages, dict) else (packages, lambda pkg: pkg)
    )

    missing = [
        formatter(pkg) for pkg in packages_to_check if importlib.util.find_spec(pkg) is None
    ]

    if not missing:
        return True

    if not strict:
        return missing

    raise MissingPackagesError(func_except or check_installed_packages, missing, reason=f"{strict=}")


def required_packages(
    plugins: list[str] | dict[str, DEP_URL] = [],
    func_except: FuncExceptT | None = None
) -> Callable[[F], F]:
    """
    Decorator to ensure that specified plugins are installed.

    Example usage:

    .. code-block:: python

        >>> @required_packages(['lvsfunc', 'vstools'])
        ... def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

        >>> @required_packages({'lvsfunc': 'pip install lvsfunc})
        ... def func(clip: vs.VideoNode) -> vs.VideoNode:
        ...     return clip

    For more information, see :py:func:`check_installed_packages`.

    :param packages:        A list of packages to check for. If a dict is passed,
                            the values are treated as either a URL or a pip command to download the package.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            check_installed_packages(plugins, True, func_except or required_packages)

            return func(*args, **kwargs)

        return wrapper  # type:ignore

    return decorator
