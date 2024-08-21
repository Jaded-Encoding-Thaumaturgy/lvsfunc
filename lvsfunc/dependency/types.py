from typing import Any, Callable, TypeVar

__all__ = [
    'DEP_URL',
    'F',
]


DEP_URL = str
"""A string representing a URL to download a dependency from."""

F = TypeVar('F', bound=Callable[..., Any])
"""Generic type variable for the function"""
