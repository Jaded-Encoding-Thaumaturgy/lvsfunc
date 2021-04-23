"""
Dehardsubbing helpers.
"""
import vapoursynth as vs

import vsutil

from abc import ABC
from typing import Any, List, Optional, Tuple, Union

from .mask import DeferredMask
from .misc import replace_ranges, scale_thresh
from .types import Range

core = vs.core


class HardsubMask(DeferredMask, ABC):
    """
    Dehardsub masking interface.

    Provides extra functions potentially useful for dehardsubbing.

    :param range:    A single range or list of ranges to replace,
                     compatible with :py:class:`lvsfunc.misc.replace_ranges`
    :param bound:    A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted.
                     (Default: ``None``, no bounding)
    :param blur:     Blur the bounding mask (Default: True)
    :param refframe: A single frame number to use to generate the mask
                     or a list of frame numbers with the same length as ``range``

    """
    def get_progressive_dehardsub(self, hrdsb: vs.VideoNode, ref: vs.VideoNode,
                                  partials: List[vs.VideoNode]) -> Tuple[List[vs.VideoNode], List[vs.VideoNode]]:
        """
        Dehardsub using multiple superior hardsubbed sources and one inferior non-subbed source.

        :param hrdsb:    Hardsub master source (eg Wakanim RU dub)
        :param ref:      Non-subbed reference source (eg CR, Funi, Amazon)
        :param partials: Sources to use for partial dehardsubbing (eg Waka DE, FR, SC)

        :return:         Dehardsub stages and masks used for progressive dehardsub
        """
        masks = [self.get_mask(hrdsb, ref)]
        pdhs = [hrdsb]
        dmasks = []
        partials = partials + [ref]
        assert masks[-1].format is not None
        thresh = scale_thresh(0.75, masks[-1])
        for p in partials:
            masks.append(core.std.Expr([masks[-1], self.get_mask(p, ref)], expr="x y -"))
            dmasks.append(vsutil.iterate(core.std.Expr([masks[-1]], f"x {thresh} < 0 x ?"),
                                         core.std.Maximum,
                                         4).std.Inflate())
            pdhs.append(core.std.MaskedMerge(pdhs[-1], p, dmasks[-1]))
            masks[-1] = core.std.MaskedMerge(masks[-1], masks[-1].std.Invert(), masks[-2])
        return pdhs, dmasks

    def apply_dehardsub(self, hrdsb: vs.VideoNode, ref: vs.VideoNode,
                        partials: Optional[List[vs.VideoNode]]) -> vs.VideoNode:
        """
        Apply dehardsubbing to a clip.

        :param hrdsb:    Hardsubbed source
        :param ref:      Non-hardsubbed source
        :param partials: Other hardsubbed sources

        :return:         Dehardsubbed clip
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
    Hardsub scenefiltering helper using kgf.hardsubmask_fades.

    :param highpass: Highpass filter for hardsub detection (16-bit, Default: 5000)
    :param expand:   ``kgf.hardsubmask_fades`` expand parameter (Default: 8)
    """
    highpass: int
    expand: int

    def __init__(self, *args: Any, highpass: int = 5000, expand: int = 8, **kwargs: Any) -> None:
        try:
            from kagefunc import hardsubmask_fades
        except ModuleNotFoundError:
            raise ModuleNotFoundError("HardsubSignKgf: missing dependency 'kagefunc'")
        self.hardsubmask_fades = hardsubmask_fades
        self.highpass = highpass
        self.expand = expand
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return self.hardsubmask_fades(clip, ref, highpass=self.highpass, expand_n=self.expand)


class HardsubSign(HardsubMask):
    """
    Hardsub scenefiltering helper using Zastin's hardsub mask.

    :param thresh:  Binarization threshold, [0, 1] (Default: 0.06)
    :param expand:  std.Maximum iterations (Default: 8)
    :param inflate: std.Inflate iterations (Default: 7)
    """
    thresh: float
    expand: int
    inflate: int

    def __init__(self, *args: Any, thresh: float = 0.06, expand: int = 8, inflate: int = 7, **kwargs: Any) -> None:
        self.thresh = thresh
        self.expand = expand
        self.inflate = inflate
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        assert clip.format is not None
        hsmf = core.std.Expr(vsutil.split(core.std.Expr([clip, ref], 'x y - abs')
                                          .resize.Point(format=clip.format.replace(subsampling_w=0,
                                                                                   subsampling_h=0).id)),
                             "x y z max max")
        hsmf = vsutil.iterate(vsutil.iterate(hsmf.std.Binarize(scale_thresh(self.thresh, clip))
                                             .std.Minimum(),
                                             core.std.Maximum, self.expand),
                              core.std.Inflate, self.inflate)
        return hsmf


class HardsubLine(HardsubMask):
    """
    Hardsub scenefiltering helper using kgf.hardsubmask.

    :param expand: ``kgf.hardsubmask`` expand parameter (Default: clip.width // 200)
    """
    expand: Optional[int]

    def __init__(self, *args: Any, expand: Optional[int] = None, **kwargs: Any) -> None:
        self.expand = expand
        try:
            from kagefunc import hardsubmask
        except ModuleNotFoundError:
            raise ModuleNotFoundError("HardsubLine: missing dependency 'kagefunc'")
        self.hardsubmask = hardsubmask
        super().__init__(*args, **kwargs)

    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return self.hardsubmask(clip, ref, expand_n=self.expand)


class HardsubLineFade(HardsubLine):
    """
    Hardsub scenefiltering helper using kgf.hardsubmask.
    Similar to :py:class:`lvsfunc.dehardsub.HardsubLine` but
    automatically sets the reference frame to the range's midpoint.

    :param refframe: Desired reference point as a percent of the frame range.
                     0 = first frame, 1 = last frame, 0.5 = midpoint (Default)
    """
    def __init__(self, ranges: Union[Range, List[Range]], *args: Any,
                 refframe: float = 0.5, **kwargs: Any) -> None:
        if refframe < 0 or refframe > 1:
            raise ValueError("HardsubLineFade: 'refframe must be between 0 and 1!'")
        ranges = ranges if isinstance(ranges, list) else [ranges]
        refframes = [r[0]+round((r[1]-r[0])*refframe) if isinstance(r, tuple) else r for r in ranges]
        super().__init__(ranges, *args, refframes=refframes, **kwargs)


def get_all_masks(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[HardsubMask]) -> vs.VideoNode:
    """
    Get a clip of :py:class:`lvsfunc.dehardsub.HardsubSign` masks.

    :param hrdsb: Hardsubbed source
    :param ref:   Reference clip
    :param signs: List of :py:class:`lvsfunc.dehardsub.HardsubSign` to generate masks for

    :return:      Clip of all hardsub masks
    """
    if ref.format is None:
        raise ValueError("get_all_masks: 'Variable-format clips not supported'")

    mask = core.std.BlankClip(ref, format=ref.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id)
    for sign in signs:
        mask = replace_ranges(mask, core.std.Expr([mask, sign.get_mask(hrdsb, ref)], 'x y +'), sign.ranges)
    return mask


def bounded_dehardsub(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[HardsubMask],
                      partials: Optional[List[vs.VideoNode]] = None) -> vs.VideoNode:
    """
    Apply a list of :py:class:`lvsfunc.dehardsub.HardsubSign`

    :param hrdsb: Hardsubbed source
    :param ref:   Reference clip
    :param signs: List of :py:class:`lvsfunc.dehardsub.HardsubSign` to apply

    :return:      Dehardsubbed clip
    """
    if ref.format is None:
        raise ValueError("get_all_masks: 'Variable-format clips not supported'")

    for sign in signs:
        hrdsb = sign.apply_dehardsub(hrdsb, ref, partials)

    return hrdsb
