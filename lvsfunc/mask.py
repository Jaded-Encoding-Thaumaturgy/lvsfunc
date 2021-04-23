"""
    Wrappers and masks for denoising.
"""
import math
from abc import ABC, abstractmethod
from functools import partial
from typing import Callable, List, Optional, Tuple, Union

import vapoursynth as vs
from vsutil import depth, get_depth, get_y, iterate, scale_value
from vsutil import Range as CRange

from . import util
from .misc import replace_ranges, scale_thresh
from .types import Position, Range, Size

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


@functoolz.curry
def adaptive_mask(clip: vs.VideoNode, luma_scaling: float = 8.0) -> vs.VideoNode:
    """
    A wrapper to create a luma mask for denoising and/or debanding.

    Function is curried to allow parameter tuning when passing to denoisers
    that allow you to pass your own mask.

    Dependencies: adaptivegrain

    :param clip:         Input clip
    :param luma_scaling: Luma scaling factor (Default: 8.0)

    :return:             Luma mask
    """
    return core.adg.Mask(clip.std.PlaneStats(), luma_scaling)


@functoolz.curry
def detail_mask(clip: vs.VideoNode, sigma: Optional[float] = None,
                rad: int = 3, radc: int = 2,
                brz_a: float = 0.005, brz_b: float = 0.005) -> vs.VideoNode:
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
    :param brz_a:       Binarizing for the detail mask (Default: 0.05)
    :param brz_b:       Binarizing for the edge mask (Default: 0.05)

    :return:            Detail mask
    """
    if clip.format is None:
        raise ValueError("detail_mask: 'Variable-format clips not supported'")

    brz_a = scale_thresh(brz_a, clip)
    brz_b = scale_thresh(brz_b, clip)

    blur = (util.quick_resample(clip, partial(core.bilateral.Gaussian, sigma=sigma))
            if sigma else clip)

    mask_a = range_mask(get_y(blur), rad=rad, radc=radc)
    mask_a = depth(mask_a, clip.format.bits_per_sample, range=CRange.FULL, range_in=CRange.FULL)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = core.std.Prewitt(get_y(blur))
    mask_b = core.std.Binarize(mask_b, brz_b)

    mask = core.std.Expr([mask_a, mask_b], 'x y max')
    mask = util.pick_removegrain(mask)(mask, 22)
    return util.pick_removegrain(mask)(mask, 11)


@functoolz.curry
def halo_mask(clip: vs.VideoNode, rad: int = 2, sigma: float = 1.0,
              thmi: int = 80, thma: int = 128,
              thlimi: int = 50, thlima: int = 100,
              edgemasking: Callable[[vs.VideoNode, float], vs.VideoNode]
              = lambda clip, sigma: core.std.Prewitt(clip, scale=sigma)) -> vs.VideoNode:
    """
    A halo mask to catch basic haloing, inspired by the mask from FineDehalo.
    Most was copied from there, but some key adjustments were made to center it specifically around masking.

    rx and ry are now combined into rad and expects an integer.
    Float made sense for FineDehalo since it uses DeHalo_alpha for dehaloing,
    but the masks themselves use rounded rx/ry values, so there's no reason to bother with floats here.

    :param clip:            Input clip
    :param rad:             Radius for the mask
    :param scale:           Multiply all pixels by scale before outputting. Sigma if `edgemask` with a sigma is passed
    :param thmi:            Minimum threshold for sharp edges; keep only the sharpest edges
    :param thma:            Maximum threshold for sharp edges; keep only the sharpest edges
    :param thlimi:          Minimum limiting threshold; includes more edges than previously, but ignores simple details
    :param thlima:          Maximum limiting threshold; includes more edges than previously, but ignores simple details
    :param edgemasking:     Callable function with signature edgemask(clip, scale/sigma)

    :return:                Halo mask
    """
    peak = (1 << get_depth(clip)) - 1
    smax = _scale(255, peak)

    thmi = _scale(thmi, peak)
    thma = _scale(thma, peak)
    thlimi = _scale(thlimi, peak)
    thlima = _scale(thlima, peak)

    matrix = [1, 2, 1, 2, 4, 2, 1, 2, 1]

    edgemask = edgemasking(get_y(clip), sigma)

    # Preserve just the strongest edges
    strong = core.std.Expr(edgemask, expr=f"x {thmi} - {thma-thmi} / {smax} *")
    # Expand to pick up additional halos
    expand = iterate(strong, core.std.Maximum, rad)

    # Having too many intersecting lines will oversmooth the mask. We get rid of those here.
    light = core.std.Expr(edgemask, expr=f"x {thlimi} - {thma-thmi} / {smax} *")
    shrink = iterate(light, core.std.Maximum, rad)
    shrink = core.std.Binarize(shrink, scale_value(.25, 32, get_depth(clip)))
    shrink = iterate(shrink, core.std.Minimum, rad)
    shrink = iterate(shrink, partial(core.std.Convolution, matrix=matrix), 2)

    # Making sure the lines are actually excluded
    excl = core.std.Expr([strong, shrink], expr="x y max")
    # Subtract and boosting to make sure we get the max pixel values for dehaloing
    mask = core.std.Expr([expand, excl], expr="x y - 2 *")
    # Additional blurring to amplify the mask
    mask = core.std.Convolution(mask, matrix)
    return core.std.Expr(mask, expr="x 2 *")


@functoolz.curry
def range_mask(clip: vs.VideoNode, rad: int = 2, radc: Optional[int] = None) -> vs.VideoNode:
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
    :param radc:    Chroma equivalent to `rad`

    :return:        Range mask
    """
    radc = rad if radc is None else radc
    if radc == 0:
        clip = get_y(clip)
    ma = _minmax(clip, rad, radc, maximum=True)
    mi = _minmax(clip, rad, radc, maximum=False)

    return core.std.Expr([ma, mi], expr='x y -')


# Helper functions
def _scale(value: int, peak: int) -> int:
    x = value * peak / 255
    return math.floor(x + 0.5) if x > 0 else math.ceil(x - 0.5)


def _minmax(clip: vs.VideoNode, sy: int = 2, sc: int = 2, maximum: bool = False) -> vs.VideoNode:
    yp = sy >= sc
    yiter = 1 if yp else 0
    cp = sc >= sy
    citer = 1 if cp else 0
    planes = [0] if yp and not cp else [1, 2] if cp and not yp else [0, 1, 2]

    if max(sy, sc) % 3 != 1:
        coor = [0, 1, 0, 1, 1, 0, 1, 0]
    else:
        coor = [1] * 8

    if sy > 0 or sc > 0:
        func = clip.std.Maximum if maximum else clip.std.Minimum
        return _minmax(func(planes=planes, coordinates=coor), sy=sy-yiter, sc=sc-citer)
    else:
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
                hm = replace_ranges(hm, mask*len(hm), range)

        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)

    @abstractmethod
    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        pass
