"""
Dehardsubbing helpers.
"""
import vapoursynth as vs
import kagefunc as kgf

import vsutil

from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, Union

from .mask import BoundingBox
from .misc import replace_ranges
from .types import Range

core = vs.core


class Mask(ABC):
    """
    Deferred masking interface.

    Provides an interface to use different masking functions for detecting hardsubs.

    :param range:    A single range or list of ranges to replace,
                     compatible with :py:class:`lvsfunc.misc.replace_ranges`
    :param bound:    A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted.
                     (Default: ``None``, no bounding)
    :param blur:     Blur the bounding mask (Default: True)
    :param refframe: A single frame number to use to generate the mask
                     or a list of frame numbers with the same length as ``range``

    """
    ranges: List[Range]
    bound: Optional[BoundingBox]
    refframes: List[int]
    blur: bool

    def __init__(self, ranges: Union[Range, List[Range]],
                 bound: Union[BoundingBox, Tuple[Tuple[int, int], Tuple[int, int]], None] = None,
                 *,
                 blur: bool = False, refframes: Union[int, List[int], None] = None):
        self.ranges = ranges if isinstance(ranges, list) else [ranges]
        self.blur = blur

        if bound is None:
            self.bound = None
        elif isinstance(bound, BoundingBox):
            self.bound = bound
        else:
            self.bound = BoundingBox(bound[0], bound[1])

        if refframes is None:
            self.refframes = []
        elif isinstance(refframes, int):
            self.refframes = [refframes] * len(self.ranges)
        else:
            self.refframes = refframes

        if len(self.refframes) > 0 and len(self.refframes) != len(self.ranges):
            raise ValueError("Mask: 'Received reference frame and range list size mismatch!'")

    def get_mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get the bounded mask for the hardsub.

        :param hrdsb: Hardsubbed source
        :param ref:   Reference clip

        :return:      Bounded mask for the hardsub
        """
        if ref.format is None or hrdsb.format is None:
            raise ValueError("get_all_masks: 'Variable-format clips not supported'")

        if self.bound:
            bm = self.bound.get_mask(ref)
            bm = bm if not self.blur else bm.std.BoxBlur(hradius=10, vradius=10, hpasses=5, vpasses=5)

        if len(self.refframes) == 0:
            hm = vsutil.depth(self._mask(hrdsb, ref), hrdsb.format.bits_per_sample,
                              range=vsutil.Range.FULL, range_in=vsutil.Range.FULL)
        else:
            hm = core.std.BlankClip(ref, format=ref.format.replace(color_family=vs.GRAY,
                                                                   subsampling_h=0, subsampling_w=0).id)
            for range, rf in zip(self.ranges, self.refframes):
                mask = vsutil.depth(self._mask(hrdsb[rf], ref[rf]), hrdsb.format.bits_per_sample,
                                    range=vsutil.Range.FULL, range_in=vsutil.Range.FULL)
                hm = replace_ranges(hm, mask*len(hm), range)

        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)

    def apply_mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Apply the mask to the clip.

        :param hrdsb: Hardsubbed source
        :param ref:   Reference clip

        :return:      Dehardsubbed clip
        """
        return replace_ranges(hrdsb,
                              core.std.MaskedMerge(hrdsb, ref, self.get_mask(hrdsb, ref)),
                              self.ranges)

    @abstractmethod
    def _mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        pass


class HardsubSign(Mask):
    """
    Hardsub scenefiltering helper using kgf.hardsubmask_fades.

    :param highpass: Highpass filter for hardsub detection (16-bit, Default: 5000)
    :param expand:   ``kgf.hardsubmask_fades`` expand parameter (Default: 8)
    """
    highpass: int
    expand: int

    def __init__(self, *args: Any, highpass: int = 5000, expand: int = 8,
                 blur: bool = True, **kwargs: Any) -> None:
        self.highpass = highpass
        self.expand = expand
        super().__init__(*args, blur=blur, **kwargs)

    def _mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return kgf.hardsubmask_fades(hrdsb, ref, highpass=self.highpass, expand_n=self.expand)


class HardsubLine(Mask):
    """
    Hardsub scenefiltering helper using kgf.hardsubmask.

    :param expand: ``kgf.hardsubmask`` expand parameter (Default: clip.width // 200)

    """
    expand: Optional[int]

    def __init__(self, *args: Any, expand: Optional[int] = None, **kwargs: Any) -> None:
        self.expand = expand
        super().__init__(*args, **kwargs)

    def _mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return kgf.hardsubmask(hrdsb, ref, expand_n=self.expand)


class HardsubLineFade(HardsubLine):
    """
    Hardsub scenefiltering helper using kgf.hardsubmask.
    Similar to :py:class:`lvsfunc.dehardsub.HardsubLine` but
    automatically sets the reference frame to the range's midpoint.

    :param expand: ``kgf.hardsubmask`` expand parameter (Default: clip.width // 200)

    """
    def __init__(self, ranges: Union[Range, List[Range]], *args: Any,
                 expand: Optional[int] = None, **kwargs: Any) -> None:
        ranges = ranges if isinstance(ranges, list) else [ranges]
        refframes = [r[0]+(r[1]-r[0])//2 if isinstance(r, tuple) else r for r in ranges]
        super().__init__(ranges, *args, refframes=refframes, **kwargs)


def get_all_masks(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[Mask]) -> vs.VideoNode:
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


def bounded_dehardsub(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[Mask]) -> vs.VideoNode:
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
        hrdsb = sign.apply_mask(hrdsb, ref)

    return hrdsb
