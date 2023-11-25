from stgpytools import CustomError

__all__: list[str] = [
    "WobblyError",
    "InvalidMatchError",
    "MatchMismatchError",
    "InvalidCycleError",
]


class WobblyError(CustomError):
    """Thrown when an error related to Wobbly is thrown."""


class InvalidMatchError(WobblyError, TypeError):
    """Thrown when an invalid fieldmatch value is given."""


class MatchMismatchError(WobblyError, ValueError):
    """Thrown when a fieldmatch value is given that is not allowed."""


class InvalidCycleError(WobblyError):
    """Raised when a wrong cycle is given."""
