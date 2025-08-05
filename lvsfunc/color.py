from typing import Literal, Self

from jetpytools import CustomEnum, NotFoundEnumValue
from vskernels import Point
from vstools import ColorRange, Matrix, core, scale_value, vs

__all__: list[str] = [
    'RGBColor'
]


class RGBColor(tuple[float, float, float], CustomEnum):
    """An enum representing RGB colours."""

    RED = (1.0, 0.0, 0.0)
    GREEN = (0.0, 1.0, 0.0)
    BLUE = (0.0, 0.0, 1.0)
    WHITE = (1.0, 1.0, 1.0)
    BLACK = (0.0, 0.0, 0.0)
    YELLOW = (1.0, 1.0, 0.0)
    MAGENTA = (1.0, 0.0, 1.0)
    CYAN = (0.0, 1.0, 1.0)
    GRAY = (0.5, 0.5, 0.5)
    SILVER = (0.75, 0.75, 0.75)
    GOLD = (1.0, 0.84, 0.0)
    ORANGE = (1.0, 0.65, 0.0)
    PURPLE = (0.5, 0.0, 0.5)
    BROWN = (0.65, 0.16, 0.16)
    PINK = (1.0, 0.75, 0.8)
    LIME = (0.0, 1.0, 0.0)
    TEAL = (0.0, 0.5, 0.5)
    NAVY = (0.0, 0.0, 0.5)
    MAROON = (0.5, 0.0, 0.0)
    OLIVE = (0.5, 0.5, 0.0)
    INDIGO = (0.29, 0.0, 0.51)
    VIOLET = (0.93, 0.51, 0.93)
    TURQUOISE = (0.25, 0.88, 0.82)
    CORAL = (1.0, 0.5, 0.31)
    CRIMSON = (0.86, 0.08, 0.24)
    KHAKI = (0.94, 0.9, 0.55)
    PLUM = (0.87, 0.63, 0.87)
    SALMON = (0.98, 0.5, 0.45)
    AQUA = (0.0, 1.0, 1.0)
    LAVENDER = (0.9, 0.9, 0.98)
    BEIGE = (0.96, 0.96, 0.86)
    MINT = (0.24, 0.71, 0.54)
    PERIWINKLE = (0.8, 0.8, 1.0)
    CHARTREUSE = (0.5, 1.0, 0.0)
    BURGUNDY = (0.5, 0.0, 0.13)
    MAUVE = (0.88, 0.69, 1.0)
    FOREST_GREEN = (0.13, 0.55, 0.13)
    RUST = (0.72, 0.25, 0.05)
    ROYAL_BLUE = (0.25, 0.41, 0.88)
    SLATE = (0.44, 0.5, 0.56)

    @classmethod
    def from_name(cls, name: str) -> Self:
        """Get the RGBColor from a name."""

        if name.upper() not in cls.__members__:
            raise NotFoundEnumValue(f'{name} is not a valid RGBColor name.', cls.from_name)

        return cls(name)

    def to_clip(self, ref: vs.VideoNode | None = None) -> vs.VideoNode:
        """Create a blank clip with the color."""

        blank_clip = core.std.BlankClip(ref, format=vs.RGBS, color=self)

        if not ref:
            return blank_clip

        assert ref.format

        return Point.resample(blank_clip, ref.format.id, matrix=Matrix.from_video(ref))

    def scale_value(
        self, bitdepth: Literal[
            8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31
        ]
    ) -> list[int]:
        """Scale the value of the color."""

        # TODO: idk what to do with the colour range
        return [
            int(scale_value(value, bitdepth, 32, range_in=ColorRange.FULL)) for value in self.value
        ]
