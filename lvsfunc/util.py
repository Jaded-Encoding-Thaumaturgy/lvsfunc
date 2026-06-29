from __future__ import annotations

import colorsys
import random
from typing import TYPE_CHECKING, Any

from jetpytools import CustomIndexError, CustomValueError
from psutil import cpu_count, virtual_memory
from vsdenoise import DFTTest
from vstools import core, vs

if TYPE_CHECKING:
    from matplotlib.figure import Figure

__all__ = [
    "colored_clips",
    "set_vs_affinity",
    "sloc_curve_to_graph",
]


def set_vs_affinity(*, threads: int = -1, cache_limit_mb: int = -1) -> None:
    """
    Configure VapourSynth worker threads and framebuffer cache.

    If the CPU enables SMT, pins the process to every second logical CPU (0, 2, 4, ...)
    so each worker gets its own physical core. Otherwise, pins to every logical CPU.

    Args:
        threads: Number of VS worker threads.
            Default: ``-1`` uses all physical cores if SMT is enabled, otherwise all logical cores, capped at 8.
        cache_limit_mb: Upper framebuffer cache limit in MB.
            VS may use less; cached frames are freed once this limit is exceeded.
            Default: ``-1`` uses three quarters of installed RAM,
            but reserves at least 2 GB for the OS and encoder.
    """

    logical = cpu_count(logical=True) or 16
    physical = cpu_count(logical=False) or logical // 2

    smt = logical > physical

    if threads <= 0:
        threads = min(physical if smt else logical, 8)

    threads = max(threads, 1)

    if cache_limit_mb <= 0:
        total_mb = virtual_memory().total // 1024**2
        cache_limit_mb = min(total_mb * 3 // 4, max(total_mb - 2048, 1024))

    if smt:
        core.set_affinity(range(0, min(threads * 2, logical), 2), cache_limit_mb)
    else:
        core.set_affinity(range(0, min(threads, logical)), cache_limit_mb)


def colored_clips(
    amount: int,
    max_hue: int = 300,
    rand: bool = True,
    seed: Any | None = None,
    **kwargs: Any,
) -> list[vs.VideoNode]:
    """
    Return a list of BlankClips with unique colors in sequential or random order.

    The colors will be evenly spaced by hue in the HSL colorspace.

    Useful for comparison functions or just for getting multiple uniquely colored BlankClips for testing purposes.
    Will always return a pure red clip in the list as this is the RGB equivalent of the lowest HSL hue possible (0).

    Written by `Dave <https://github.com/OrangeChannel>`_.

    Args:
        amount: Number of VideoNodes to return.
        max_hue: Maximum hue (``0 < hue <= 360``) in degrees to generate colors from (uses the HSL color model).
            Values above 315 may loop back toward red and are not recommended for visually distinct colors.
            If ``amount`` exceeds ``max_hue``, duplicate hues may appear.
            Default: 300.
        rand: Randomizes order of the returned list. Default: ``True``.
        seed: Seed for the random number generator.
            Allows for consistent randomized order of the resulting clips if specified.
            Default: ``None``.
        kwargs: Additional keyword arguments passed to :py:func:`vapoursynth.core.std.BlankClip`.

    Returns:
        List of uniquely colored clips in sequential or random order.

    Raises:
        CustomIndexError: ``amount`` is less than 2.
        CustomValueError: ``max_hue`` is not in ``(0, 360]``.
    """

    if amount < 2:
        raise CustomIndexError("`amount` must be at least 2!", colored_clips)
    if not (0 < max_hue <= 360):
        raise CustomValueError("`max_hue` must be greater than 0 and less than 360 degrees!", colored_clips)

    blank_clip_args: dict[str, Any] = dict(keep=1) | kwargs

    hues = [i * max_hue / (amount - 1) for i in range(amount - 1)] + [max_hue]

    hls_color_list = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


def sloc_curve_to_graph(
    slocation: DFTTest.SLocation,
    *,
    res: int = 100,
    digits: int = 3,
    figsize: tuple[float, float] = (8.0, 4.0),
    title: str | None = None,
) -> Figure:
    """
    Plot a DFTTest ``SLocation`` curve.

    Plots the ``frequencies`` and ``sigmas`` stored on ``slocation``.
    Locations passed with an ``interpolate`` mode
    to :py:meth:`~vsdenoise.DFTTest.SLocation.__init__` are already expanded.
    Otherwise :py:meth:`~vsdenoise.DFTTest.SLocation.interpolate` upsamples for display.
    Unexpanded locations are also drawn as markers.

    Args:
        slocation: The ``SLocation`` to plot.
        res: Resolution passed to :py:meth:`~vsdenoise.DFTTest.SLocation.interpolate`.
        digits: Precision of frequency values passed to :py:meth:`~vsdenoise.DFTTest.SLocation.interpolate`.
        figsize: Figure size in inches, ``(width, height)``.
        title: Optional plot title.

    Returns:
        A matplotlib figure.
    """

    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("Agg")

    interpolated = slocation.interpolate(res=res, digits=digits) if len(slocation) < res else slocation

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(list(interpolated.frequencies), list(interpolated.sigmas), label="slocation")

    if len(slocation) <= 8:
        ax.scatter(list(slocation.frequencies), list(slocation.sigmas), zorder=5, label="locations")

    ax.set(xlabel="frequency", ylabel="sigma", xlim=(0.0, 1.0))
    ax.set_ylim(bottom=0.0)
    ax.grid(True, alpha=0.3)

    ax.legend()

    if title is not None:
        ax.set_title(title)

    fig.tight_layout()

    return fig
