from __future__ import annotations

from abc import ABC
from typing import Any

import vapoursynth as vs
from vsutil import iterate, split

from .mask import DeferredMask
from .types import Range
from .util import check_variable, normalize_ranges, replace_ranges, scale_thresh

core = vs.core

__all__ = [
    'bounded_dehardsub',
    'get_all_masks',
    'hardsub_mask',
    'HardsubASS',
    'HardsubLine', 'HardsubLineFade',
    'HardsubMask',
    'HardsubSign', 'HardsubSignFade',
    'HardsubSignKgf',
]


class HardsubMask(DeferredMask, ABC):
    """
    Dehardsub masking interface.

    Provides extra functions potentially useful for dehardsubbing.

    :param range:    A single range or list of ranges to replace,
                     compatible with :py:class:`lvsfunc.misc.replace_ranges`
    :param bound:    A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted.
                     (Default: ``None``, no bounding)
    :param blur:     Blur the bounding mask (Default: True).
    :param refframe: A single frame number to use to generate the mask.
                     or a list of frame numbers with the same length as :py:func:`lvsfunc.types.Range`
    """

    def get_progressive_dehardsub(self, hrdsb: vs.VideoNode, ref: vs.VideoNode,
                                  partials: list[vs.VideoNode]) -> tuple[list[vs.VideoNode], list[vs.VideoNode]]:
        """
        Dehardsub using multiple superior hardsubbed sources and one inferior non-subbed source.

        :param hrdsb:    Hardsub master source (eg Wakanim RU dub).
        :param ref:      Non-subbed reference source (eg CR, Funi, Amazon).
        :param partials: Sources to use for partial dehardsubbing (eg Waka DE, FR, SC).

        :return:         Dehardsub stages and masks used for progressive dehardsub.
        """
        masks = [self.get_mask(hrdsb, ref)]
        pdhs = [hrdsb]
        dmasks = []
        partials = partials + [ref]
        assert masks[-1].format is not None
        thresh = scale_thresh(0.75, masks[-1])
        for p in partials:
            masks.append(core.akarin.Expr([masks[-1], self.get_mask(p, ref)], expr="x y -"))
            dmasks.append(iterate(core.akarin.Expr([masks[-1]], f"x {thresh} < 0 x ?"),
                                  core.std.Maximum,
                                  4).std.Inflate())
            pdhs.append(core.std.MaskedMerge(pdhs[-1], p, dmasks[-1]))
            masks[-1] = core.std.MaskedMerge(masks[-1], masks[-1].std.Invert(), masks[-2])
        return pdhs, dmasks

    def apply_dehardsub(self, hrdsb: vs.VideoNode, ref: vs.VideoNode,
                        partials: list[vs.VideoNode] | None) -> vs.VideoNode:
        """
        Apply dehardsubbing to a clip.

        :param hrdsb:    Hardsubbed source.
        :param ref:      Non-hardsubbed source.
        :param partials: Other hardsubbed sources.

        :return:         Dehardsubbed clip.
        """
        if partials:
            return replace_ranges(hrdsb,
                                  self.get_progressive_dehardsub(hrdsb, ref, partials)[0][-1],
                                  self.ranges)
        else:
            return replace_ranges(hrdsb,
                                  core.std.MaskedMerge(hrdsb, ref, self.get_mask(hrdsb, ref)),
                                  self.ranges)


class HardsubSignKgf(HardsubMask):
    """
    Hardsub scenefiltering helper using :py:func:`kgf.hardsubmask_fades`.

    Dependencies:

    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_

    :param highpass:                Highpass filter for hardsub detection (16-bit, Default: 5000).
    :param expand:                  :py:func:`kgf.hardsubmask_fades` expand parameter (Default: 8).

    :raises ModuleNotFoundError:    Dependencies are missing.
    """

    highpass: int
    expand: int

    def __init__(self, *args: Any, highpass: int = 5000, expand: int = 8, **kwargs: Any) -> None:
        try:
            from kagefunc import hardsubmask_fades
        except ModuleNotFoundError:
            raise ModuleNotFoundError("HardsubSignKgf: missing dependency `kagefunc`!")

        self.hardsubmask_fades = hardsubmask_fades
        self.highpass = highpass
        self.expand = expand
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return self.hardsubmask_fades(clip, ref, highpass=self.highpass, expand_n=self.expand)


class HardsubSign(HardsubMask):
    """
    Hardsub scenefiltering helper using `Zastin <https://github.com/kgrabs>`_'s hardsub mask.

    :param thresh:  Binarization threshold, [0, 1] (Default: 0.06).
    :param expand:  std.Maximum iterations (Default: 8).
    :param inflate: std.Inflate iterations (Default: 7).
    """

    thresh: float
    minimum: int
    expand: int
    inflate: int

    def __init__(self, *args: Any, thresh: float = 0.06, minimum: int = 1,
                 expand: int = 8, inflate: int = 7, **kwargs: Any) -> None:
        self.thresh = thresh
        self.minimum = minimum
        self.expand = expand
        self.inflate = inflate
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return hardsub_mask(clip, ref, thresh=self.thresh, minimum=self.minimum,
                            expand=self.expand, inflate=self.inflate)


class HardsubLine(HardsubMask):
    """
    Hardsub scenefiltering helper using :py:func:`kgf.hardsubmask`.

    Dependencies:

    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_

    :param expand:                  :py:func:`kgf.hardsubmask` expand parameter (Default: clip.width // 200).

    :raises ModuleNotFoundError:    Dependencies are missing.
    """

    expand: int | None

    def __init__(self, *args: Any, expand: int | None = None, **kwargs: Any) -> None:
        self.expand = expand
        try:
            from kagefunc import hardsubmask
        except ModuleNotFoundError:
            raise ModuleNotFoundError("HardsubLine: missing dependency `kagefunc`!")

        self.hardsubmask = hardsubmask
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return self.hardsubmask(clip, ref, expand_n=self.expand)


class HardsubLineFade(HardsubLine):
    """
    Hardsub scenefiltering helper using :py:func:`kgf.hardsubmask`.

    Similar to :py:class:`lvsfunc.dehardsub.HardsubLine` but
    automatically sets the reference frame to the range's midpoint.

    :param refframe:        Desired reference point as a percent of the frame range.
                            0 = first frame, 1 = last frame, 0.5 = midpoint (Default)

    :raises ValueError:     `refframe` is not between 0–1.
    """

    ref_float: float

    def __init__(self, ranges: Range | list[Range], *args: Any,
                 refframe: float = 0.5, **kwargs: Any) -> None:
        if refframe < 0 or refframe > 1:
            raise ValueError("HardsubLineFade: '`refframe` must be between 0 and 1!'")
        ranges = ranges if isinstance(ranges, list) else [ranges]
        self.ref_float = refframe
        super().__init__(ranges, *args, refframes=None, **kwargs)

    def get_mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """Get the mask."""
        self.refframes = [r[0]+round((r[1]-r[0])*self.ref_float) for r in normalize_ranges(ref, self.ranges)]
        return super().get_mask(clip, ref)


# TODO: find a more idiomatic way to do this
class HardsubSignFade(HardsubSign):
    """
    Hardsub scenefiltering helper using `Zastin <https://github.com/kgrabs>`_'s sign mask.

    Similar to :py:class:`lvsfunc.dehardsub.HardsubSign` but
    automatically sets the reference frame to the range's midpoint.

    :param refframe:        Desired reference point as a percent of the frame range.
                            0 = first frame, 1 = last frame, 0.5 = midpoint (Default)

    :raises ValueError:     `refframe` is not between 0–1.
    """

    ref_float: float

    def __init__(self, ranges: Range | list[Range], *args: Any,
                 refframe: float = 0.5, **kwargs: Any) -> None:
        if refframe < 0 or refframe > 1:
            raise ValueError("HardsubSignFade: 'refframe must be between 0 and 1!'")
        ranges = ranges if isinstance(ranges, list) else [ranges]
        self.ref_float = refframe
        super().__init__(ranges, *args, refframes=None, **kwargs)

    def get_mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """Get the mask."""
        self.refframes = [r[0]+round((r[1]-r[0])*self.ref_float) for r in normalize_ranges(ref, self.ranges)]
        return super().get_mask(clip, ref)


class HardsubASS(HardsubMask):
    """
    Generate a mask using an ass script, such as for dehardubbing AoD with CR DE.

    :param filename: Path to ASS script.
    :param fontdir:  Extra fonts path.
    :param shift:    Offset to apply to the script, in frames.
                     May misbehave due to timestamp rounding.
    """

    filename: str
    fontdir: str | None
    shift: int | None

    def __init__(self, filename: str, *args: Any, fontdir: str | None = None,
                 shift: int | None = None, **kwargs: Any) -> None:
        self.filename = filename
        self.fontdir = fontdir
        self.shift = shift
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        ref = ref[0] * self.shift + ref if self.shift else ref
        mask = ref.sub.TextFile(self.filename, fontdir=self.fontdir, blend=False)[1]  # horrific abuse of typechecker
        mask = mask[self.shift:] if self.shift else mask
        mask = mask.std.Binarize(1)
        mask = iterate(mask, core.std.Maximum, 3)
        mask = iterate(mask, core.std.Inflate, 3)
        return mask.std.Limiter()


def get_all_masks(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: list[HardsubMask]) -> vs.VideoNode:
    """
    Get a clip of :py:class:`lvsfunc.dehardsub.HardsubSign` masks.

    :param hrdsb: Hardsubbed source.
    :param ref:   Reference clip.
    :param signs: List of :py:class:`lvsfunc.dehardsub.HardsubSign` to generate masks for.

    :return:      Clip of all hardsub masks.
    """
    assert check_variable(hrdsb, "get_all_masks")
    assert check_variable(ref, "get_all_masks")

    mask = core.std.BlankClip(ref, format=ref.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id)
    for sign in signs:
        mask = replace_ranges(mask, core.akarin.Expr([mask, sign.get_mask(hrdsb, ref)], 'x y +'), sign.ranges)
    return mask.std.Limiter()


def bounded_dehardsub(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: list[HardsubMask],
                      partials: list[vs.VideoNode] | None = None) -> vs.VideoNode:
    """
    Apply a list of :py:class:`lvsfunc.dehardsub.HardsubSign`.

    :param hrdsb: Hardsubbed source.
    :param ref:   Reference clip.
    :param signs: List of :py:class:`lvsfunc.dehardsub.HardsubSign` to apply.

    :return:      Dehardsubbed clip.
    """
    for sign in signs:
        hrdsb = sign.apply_dehardsub(hrdsb, ref, partials)

    return hrdsb


def hardsub_mask(hrdsb: vs.VideoNode, ref: vs.VideoNode, thresh: float = 0.06,
                 minimum: int = 1, expand: int = 8, inflate: int = 7) -> vs.VideoNode:
    """
    `Zastin <https://github.com/kgrabs>`_'s spatially-aware hardsub mask.

    :param hrdsb:   Hardsubbed source.
    :param ref:     Reference clip.
    :param thresh:  Binarization threshold, [0, 1] (Default: 0.06).
    :param minimum: Times to minimize the max (Default: 1).
    :param expand:  Times to maximize the mask (Default: 8).
    :param inflate: Times to inflate the mask (Default: 7).

    :return:        Hardsub mask.
    """
    assert check_variable(hrdsb, "hardsub_mask")
    assert check_variable(ref, "hardsub_mask")

    hsmf = core.akarin.Expr([hrdsb, ref], 'x y - abs') \
        .resize.Point(format=hrdsb.format.replace(subsampling_w=0, subsampling_h=0).id)
    hsmf = core.akarin.Expr(split(hsmf), "x y z max max")
    hsmf = hsmf.std.Binarize(scale_thresh(thresh, hsmf))
    hsmf = iterate(hsmf, core.std.Minimum, minimum)
    hsmf = iterate(hsmf, core.std.Maximum, expand)
    hsmf = iterate(hsmf, core.std.Inflate, inflate)

    return hsmf.std.Limiter()
