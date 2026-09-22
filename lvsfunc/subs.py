from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta
from fnmatch import fnmatchcase
from fractions import Fraction
from math import ceil

import ass
from jetpytools import FileNotExistsError, FuncExceptT, SPath, SPathLike, to_arr
from vstools import FrameRangesN, UnsupportedFramerateError, vs

from .exceptions import InvalidAssFileError

__all__ = [
    "ass_to_ranges",
]


def ass_to_ranges(
    file: SPathLike,
    ref: vs.VideoNode | Fraction = Fraction(24000, 1001),
    styles: Iterable[str] | str | None = None,
    effects: Iterable[str] | str | None = None,
    *,
    func_except: FuncExceptT | None = None,
) -> FrameRangesN:
    """
    Convert events in an ASS file to frame ranges.

    Args:
        file: Path to the ASS file. Must be a valid ASS file.
        ref: Reference frame rate. Variable frame rate is currently not supported.
            Default: 24000/1001.
        styles: A filter for which events to get ranges from using the event's style field.
            Allows for wildcards, so you can match all `TS-*` styles for example.
            Default: None (all events).
        effects: A filter for which events to get ranges from using the event's effect field.
            Allows for wildcards, so you can match all `TS-*` effects for example.
            Default: None (all events).

    Returns:
        FrameRangesN: A list of frame ranges.
    """

    func = func_except or ass_to_ranges

    if isinstance(ref, vs.VideoNode) and ref.fps.numerator == 0:
        # TODO: Figure out a better Exception class to raise
        raise UnsupportedFramerateError(
            func, ref, Fraction(24000, 1001), "Variable frame rate is currently not supported."
        )

    fps = ref.fps if isinstance(ref, vs.VideoNode) else ref

    if not (spath := SPath(file)).exists():
        raise FileNotExistsError(f'Could not find the file, "{spath}".', func, spath)

    InvalidAssFileError.check(spath, func)

    with spath.open("r", encoding="utf-8-sig") as f:
        script = ass.parse(f)

    style_patterns = None if styles is None else tuple(to_arr(styles))
    effect_patterns = None if effects is None else tuple(to_arr(effects))

    ranges: list[tuple[int, int]] = []

    for event in script.events:
        if isinstance(event, ass.Comment):
            continue

        if not event.text.strip():
            continue

        if style_patterns is not None and not _matches(event.style, style_patterns):
            continue

        if effect_patterns is not None and not _matches(event.effect, effect_patterns):
            continue

        if event.end <= event.start:
            continue

        start = ceil(_timedelta_to_fraction(event.start) * fps)
        end = ceil(_timedelta_to_fraction(event.end) * fps) - 1

        if start <= end:
            ranges.append((start, end))

    return _merge_ranges(ranges)


def _timedelta_to_fraction(value: timedelta) -> Fraction:
    return Fraction(
        value.days * 86400000000 + value.seconds * 1000000 + value.microseconds,
        1000000,
    )


def _matches(value: str, patterns: tuple[str, ...]) -> bool:
    return any(fnmatchcase(value, pattern) for pattern in patterns)


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not ranges:
        return []

    merged: list[tuple[int, int]] = []

    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    return merged
