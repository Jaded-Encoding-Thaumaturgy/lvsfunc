"""
    Wrappers and masks for denoising.
"""
from abc import ABC, abstractmethod
from functools import partial
from typing import List, Optional, Tuple, Union

import vapoursynth as vs
from vsutil import depth, get_y, iterate, join, split
from vsutil import Range as CRange

from . import util
from .misc import replace_ranges, scale_thresh
from .types import Position, Range, Size

core = vs.core


def detail_mask(clip: vs.VideoNode, sigma: Optional[float] = None,
                rad: int = 3, radc: int = 2,
                brz_a: float = 0.025, brz_b: float = 0.045) -> vs.VideoNode:
    """
    A wrapper for creating a detail mask to be used during denoising and/or debanding.
    The detail mask is created using debandshit's range mask,
    and is then merged with Prewitt to catch lines it may have missed.

    Function is curried to allow parameter tuning when passing to denoisers
    that allow you to pass your own mask.

    Dependencies: VapourSynth-Bilateral (optional: sigma), debandshit

    :param clip:        Input clip
    :param sigma:       Sigma for Bilateral for pre-blurring (Default: False)
    :param rad:         The luma equivalent of gradfun3's "mask" parameter
    :param radc:        The chroma equivalent of gradfun3's "mask" parameter
    :param brz_a:       Binarizing thresh for the detail mask.
                        Scaled to clip's depth if between 0 and 1 (inclusive),
                        else assumed to be in native range. (Default: 0.025)
    :param brz_b:       Binarizing thresh for the edge mask.
                        Scaled to clip's depth if between 0 and 1 (inclusive),
                        else assumed to be in native range. (Default: 0.045)

    :return:            Detail mask
    """
    if clip.format is None:
        raise ValueError("detail_mask: 'Variable-format clips not supported'")

    brz_a = scale_thresh(brz_a, clip)
    brz_b = scale_thresh(brz_b, clip)

    blur = (util.quick_resample(clip, partial(core.bilateral.Gaussian, sigma=sigma))
            if sigma else clip)

    mask_a = range_mask(get_y(blur), rad=rad, radc=radc)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = core.std.Prewitt(get_y(blur))
    mask_b = core.std.Binarize(mask_b, brz_b)

    mask = core.std.Expr([mask_a, mask_b], 'x y max')
    mask = util.pick_removegrain(mask)(mask, 22)
    return util.pick_removegrain(mask)(mask, 11)


def halo_mask(clip: vs.VideoNode, rad: int = 2,
              brz: float = 0.35,
              thmi: float = 0.315, thma: float = 0.5,
              thlimi: float = 0.195, thlima: float = 0.392,
              edgemask: Optional[vs.VideoNode] = None) -> vs.VideoNode:
    """
    A halo mask to catch basic haloing, inspired by the mask from FineDehalo.
    Most was copied from there, but some key adjustments were made to center it specifically around masking.

    rx and ry are now combined into rad and expects an integer.
    Float made sense for FineDehalo since it uses DeHalo_alpha for dehaloing,
    but the masks themselves use rounded rx/ry values, so there's no reason to bother with floats here.

    All thresholds are float and will be scaled to ``clip``\\'s format.
    If thresholds are greater than 1, they will be asummed to be in 8-bit and scaled accordingly.

    :param clip:            Input clip
    :param rad:             Radius for the mask
    :param brz:             Binarizing for shrinking mask (Default: 0.35)
    :param thmi:            Minimum threshold for sharp edges; keep only the sharpest edges
    :param thma:            Maximum threshold for sharp edges; keep only the sharpest edges
    :param thlimi:          Minimum limiting threshold; includes more edges than previously, but ignores simple details
    :param thlima:          Maximum limiting threshold; includes more edges than previously, but ignores simple details
    :param edgemask:        Edgemask to use. If None, uses ``clip.std.Prewitt()`` (Default: None).

    :return:                Halo mask
    """
    smax = scale_thresh(1.0, clip)

    thmi, thma, thlimi, thlima = (scale_thresh(t, clip, assume=8) for t in [thmi, thma, thlimi, thlima])

    matrix = [1, 2, 1, 2, 4, 2, 1, 2, 1]

    edgemask = edgemask or get_y(clip).std.Prewitt()

    # Preserve just the strongest edges
    strong = core.std.Expr(edgemask, expr=f"x {thmi} - {thlima-thlimi} / {smax} *")
    # Expand to pick up additional halos
    expand = iterate(strong, core.std.Maximum, rad)

    # Having too many intersecting lines will oversmooth the mask. We get rid of those here.
    light = core.std.Expr(edgemask, expr=f"x {thlimi} - {thma-thmi} / {smax} *")
    shrink = iterate(light, core.std.Maximum, rad)
    shrink = core.std.Binarize(shrink, scale_thresh(brz, clip))
    shrink = iterate(shrink, core.std.Minimum, rad)
    shrink = iterate(shrink, partial(core.std.Convolution, matrix=matrix), 2)

    # Making sure the lines are actually excluded
    excl = core.std.Expr([strong, shrink], expr="x y max")
    # Subtract and boosting to make sure we get the max pixel values for dehaloing
    mask = core.std.Expr([expand, excl], expr="x y - 2 *")
    # Additional blurring to amplify the mask
    mask = core.std.Convolution(mask, matrix)
    return core.std.Expr(mask, expr="x 2 *")


def range_mask(clip: vs.VideoNode, rad: int = 2, radc: int = 0) -> vs.VideoNode:
    """
    Min/max mask with separate luma/chroma radii.

    rad/radc are the luma/chroma equivalent of gradfun3's "mask" parameter.
    The way gradfun3's mask works is on an 8 bit scale, with rounded dithering of high depth input.
    As such, when following this filter with a Binarize, use the following conversion steps based on input:

    -  8 bit = Binarize(2) or Binarize(thr_det)
    - 16 bit = Binarize(384) or Binarize((thr_det - 0.5) * 256)
    - floats = Binarize(0.005859375) or Binarize((thr_det - 0.5) / 256)

    When radii are equal to 1, this filter becomes identical to mt_edge("min/max", 0, 255, 0, 255).

    :param clip:    Input clip
    :param rad:     Depth in pixels of the detail/edge masking
    :param radc:    Chroma equivalent to ``rad``

    :return:        Range mask
    """
    if radc == 0:
        clip = get_y(clip)

    if clip.format is None:
        raise ValueError("range_mask: 'Variable-format clips not supported'")

    if clip.format.color_family == vs.GRAY:
        ma = _minmax(clip, rad, True)
        mi = _minmax(clip, rad, False)
        mask = core.std.Expr([ma, mi], 'x y -')
    else:
        planes = split(clip)
        for i, rad_ in enumerate([rad, radc, radc]):
            ma = _minmax(planes[i], rad_, True)
            mi = _minmax(planes[i], rad_, False)
            planes[i] = core.std.Expr([ma, mi], 'x y -')
        mask = join(planes)

    return mask


# Helper functions
def _minmax(clip: vs.VideoNode, iterations: int, maximum: bool) -> vs.VideoNode:
    func = core.std.Maximum if maximum else core.std.Minimum
    for i in range(1, iterations + 1):
        coord = [0, 1, 0, 1, 1, 0, 1, 0] if (i % 3) != 1 else [1] * 8
        clip = func(clip, coordinates=coord)
    return clip


class BoundingBox():
    """
    A positional bounding box.
    Basically kagefunc.squaremask but can be configured then deferred.

    Uses Position + Size, like provided by GIMP's rectangle selection tool.

    :param pos:  Offset of top-left corner of the bounding box from the top-left corner of the frame.
                 Supports either a :py:class:`lvsfunc.types.Position` or a tuple that will be converted.
    :param size: Offset of the bottom-right corner of the bounding box from the top-left corner of the bounding box.
                 Supports either a :py:class:`lvsfunc.types.Size` or a tuple that will be converted.
    """
    pos: Position
    size: Size

    def __init__(self, pos: Union[Position, Tuple[int, int]], size: Union[Size, Tuple[int, int]]):
        self.pos = pos if isinstance(pos, Position) else Position(pos[0], pos[1])
        self.size = size if isinstance(size, Size) else Size(size[0], size[1])

    def get_mask(self, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get a mask representing the bounding box

        :param ref: Reference clip for format, resolution, and length.

        :return:    Square mask representing the bounding box.
        """
        if ref.format is None:
            raise ValueError("get_all_masks: 'Variable-format clips not supported'")

        if self.pos.x + self.size.x > ref.width or self.pos.y + self.size.y > ref.height:
            raise ValueError("BoundingBox: Bounds exceed clip size!")

        mask_fmt: vs.Format = ref.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0)
        white: float = 1 if mask_fmt.sample_type == vs.FLOAT else (1 << ref.format.bits_per_sample) - 1
        mask: vs.VideoNode = core.std.BlankClip(ref, color=white, length=1, format=mask_fmt.id)
        mask = mask.std.Crop(self.pos.x, ref.width - (self.pos.x + self.size.x),
                             self.pos.y, ref.height - (self.pos.y + self.size.y))
        mask = mask.std.AddBorders(self.pos.x, ref.width - (self.pos.x + self.size.x),
                                   self.pos.y, ref.height - (self.pos.y + self.size.y))

        return mask


class DeferredMask(ABC):
    """
    Deferred masking interface.

    Provides an interface to use different preconfigured masking functions.
    Provides support for ranges, reference frames, and bounding.

    :param range:    A single range or list of ranges to replace,
                     compatible with :py:class:`lvsfunc.misc.replace_ranges`
    :param bound:    A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted.
                     (Default: ``None``, no bounding)
    :param blur:     Blur the bounding mask (Default: False)
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

    def get_mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get the bounded mask.

        :param clip:  Source
        :param ref:   Reference clip

        :return:      Bounded mask
        """
        if ref.format is None or clip.format is None:
            raise ValueError("get_all_masks: 'Variable-format clips not supported'")

        if self.bound:
            bm = self.bound.get_mask(ref)
            bm = bm if not self.blur else bm.std.BoxBlur(hradius=5, vradius=5, hpasses=5, vpasses=5)

        if len(self.refframes) == 0:
            hm = depth(self._mask(clip, ref), clip.format.bits_per_sample,
                       range=CRange.FULL, range_in=CRange.FULL)
        else:
            hm = core.std.BlankClip(ref, format=ref.format.replace(color_family=vs.GRAY,
                                                                   subsampling_h=0, subsampling_w=0).id)
            for range, rf in zip(self.ranges, self.refframes):
                mask = depth(self._mask(clip[rf], ref[rf]), clip.format.bits_per_sample,
                             range=CRange.FULL, range_in=CRange.FULL)
                hm = replace_ranges(hm, core.std.Expr([hm, mask*len(hm)], expr="x y max"), range)

        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)

    @abstractmethod
    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        pass
