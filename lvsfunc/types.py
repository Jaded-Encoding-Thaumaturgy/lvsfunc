from typing import Tuple, Union

Range = Union[int, Tuple[int, int]]


class Coordinate():
    """
    A positive set of (x, y) coodinates.
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise ValueError(f"{self.__class__.__name__}: 'Can't be negative!'")
        self.x = x
        self.y = y


class Position(Coordinate):
    pass


class Size(Coordinate):
    pass
