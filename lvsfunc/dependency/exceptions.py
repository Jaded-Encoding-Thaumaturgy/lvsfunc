from typing import Any

from vstools import CustomError, FuncExceptT, SupportsString

__all__: list[str] = [
    'CustomDependencyError',
    'MissingPluginsError', 'MissingPluginFunctionsError',
    'MissingPackagesError'
]


class CustomDependencyError(CustomError, ImportError):
    """Raised when there's a general dependency error."""

    def __init__(
        self, func: FuncExceptT, deps: str | list[str] | ImportError,
        message: SupportsString = "Missing dependencies: '{deps}'!",
        **kwargs: Any
    ) -> None:
        """
        :param func:        Function this error was raised from.
        :param deps:        Either the raised error or the names of the missing package.
        :param message:     Custom error message.
        """

        super().__init__(message, func, deps=deps, **kwargs)


class MissingPluginsError(CustomDependencyError):
    """Raised when there's missing plugins."""

    def __init__(
        self, func: FuncExceptT, plugins: str | list[str] | ImportError,
        message: SupportsString = "Missing plugins '{deps}'!",
        **kwargs: Any
    ) -> None:
        if isinstance(plugins, list) and len(plugins) == 1:
            if isinstance(message, str):
                message = message.replace("plugins", "plugin")

            plugins = plugins[0]

        super().__init__(func, plugins, message, **kwargs)


class MissingPluginFunctionsError(CustomDependencyError):
    """Raised when a plugin is missing functions."""

    def __init__(
        self, func: FuncExceptT, plugin: str, functions: str | list[str],
        message: SupportsString = "'{plugin}' plugin is missing functions '{deps}'!",
        **kwargs: Any
    ) -> None:
        if isinstance(functions, list) and len(functions) == 1:
            if isinstance(message, str):
                message = message.replace("functions", "function")

            functions = functions[0]

        super().__init__(func, functions, message, plugin=plugin, **kwargs)


class MissingPackagesError(CustomDependencyError):
    """Raised when there's missing packages."""

    def __init__(
        self, func: FuncExceptT, packages: str | list[str] | ImportError,
        message: SupportsString = "Missing packages '{deps}'!",
        **kwargs: Any
    ) -> None:
        if isinstance(packages, list) and len(packages) == 1:
            if isinstance(message, str):
                message = message.replace("packages", "package")

            packages = packages[0]

        super().__init__(func, packages, message, **kwargs)
