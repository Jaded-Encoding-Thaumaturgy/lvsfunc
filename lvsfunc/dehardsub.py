"""
Dehardsubbing helpers.
"""
import vapoursynth as vs
import kagefunc as kgf
import lvsfunc as lvf

import vsutil

from typing import List, Optional, Tuple, Union

from .mask import BoundingBox
from .types import Range

core = vs.core


class HardsubSign():
    """
    Hardsub scenefiltering helper.

    Supply range(s) for the sign and optionally a bounding box.

    :param range:    A single range or list of ranges to replace,
                     compatible with :py:class:`lvsfunc.misc.replace_ranges`
    :param bound:    A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted.
    :param blur:     Blur the bounding mask (Default: True)
    :param refframe: Force specific frame to be used for mask generation
    :param highpass: Highpass filter for hardsub detection (16-bit, Default: 5000)
    :param expand:   ``kgf.hardsubmask_fades`` expand parameter (Default: 8)
    """
    ranges: Union[Range, List[Range]]
    bound: Optional[BoundingBox]
    refframe: Optional[int]
    highpass: int
    expand: int
    blur: bool

    def __init__(self,
                 ranges: Union[Range, List[Range]],
                 bound: Union[BoundingBox, Tuple[Tuple[int, int], Tuple[int, int]], None],
                 blur: bool = True, refframe: Optional[int] = None, highpass: int = 5000, expand: int = 8):
        self.ranges = ranges
        self.refframe = refframe
        self.highpass = highpass
        self.expand = expand
        self.blur = blur
        if bound is None:
            self.bound = None
        elif isinstance(bound, BoundingBox):
            self.bound = bound
        else:
            self.bound = BoundingBox(bound[0], bound[1])

    def _hardsub_mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:

        if self.refframe is not None:
            hrdsb = hrdsb[self.refframe]
            ref = ref[self.refframe]

        if ref.format is None or hrdsb.format is None:
            raise ValueError("get_all_masks: 'Variable-format clips not supported'")

        mask = kgf.hardsubmask_fades(hrdsb, ref, highpass=self.highpass, expand_n=self.expand)
        assert isinstance(mask, vs.VideoNode)
        return vsutil.depth(mask, hrdsb.format.bits_per_sample)

    def get_mask(self, hrdsb: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get the bounded mask for the hardsub.

        :param hrdsb: Hardsubbed source
        :param ref:   Reference clip

        :return:      Bounded mask for the hardsub
        """
        hm = self._hardsub_mask(hrdsb, ref)
        if self.bound:
            bm = self.bound.get_mask(ref)
            bm = bm if not self.blur else bm.std.BoxBlur(hradius=10, vradius=10, hpasses=5, vpasses=5)
        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)


def get_all_masks(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[HardsubSign]) -> vs.VideoNode:
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
        mask = lvf.misc.replace_ranges(mask, core.std.Expr([mask, sign.get_mask(hrdsb, ref)], 'x y +'), sign.ranges)
    return mask


def bounded_dehardsub(hrdsb: vs.VideoNode, ref: vs.VideoNode, signs: List[HardsubSign]) -> vs.VideoNode:
    """
    Apply a list of :py:class:`lvsfunc.dehardsub.HardsubSign`

    :param hrdsb: Hardsubbed source
    :param ref:   Reference clip
    :param signs: List of :py:class:`lvsfunc.dehardsub.HardsubSign` to apply

    :return:      Dehardsubbed clip
    """
    if ref.format is None:
        raise ValueError("get_all_masks: 'Variable-format clips not supported'")

    bound = hrdsb
    for sign in signs:
        bound = lvf.misc.replace_ranges(bound,
                                        core.std.MaskedMerge(bound, ref, sign.get_mask(hrdsb, ref)),
                                        sign.ranges)

    return bound
