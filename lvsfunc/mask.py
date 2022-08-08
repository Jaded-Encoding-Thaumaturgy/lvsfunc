from __future__ import annotations

import math
from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable, Sequence

import vapoursynth as vs
from vsexprtools.util import normalise_planes
from vsrgtools import removegrain
from vsutil import Range as CRange
from vsutil import depth, get_depth, get_y, iterate, join, split

from .types import Position, Range, Shapes, Size
from .util import check_variable, check_variable_resolution, quick_resample, replace_ranges, scale_peak, scale_thresh

core = vs.core


__all__ = [
    'BoundingBox',
    'DeferredMask',
    'detail_mask_neo',
    'detail_mask',
    'fine_dehalo_mask',
    'halo_mask',
    'mt_xxpand_multi', 'minm', 'maxm',
    'range_mask',
]


def detail_mask(clip: vs.VideoNode, sigma: float | None = None,
                rad: int = 3, brz_a: float = 0.025, brz_b: float = 0.045) -> vs.VideoNode:
    """
    Create a detail mask to be used during denoising and/or debanding.

    The detail mask is created using debandshit's range mask,
    and is then merged with Prewitt to catch lines it may have missed.

    Dependencies:

    * `VapourSynth-Bilateral <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Bilateral>`_ (optional: sigma)
    * `RGSF <https://github.com/IFeelBloated/RGSF>`_ (optional: 32 bit clip)

    :param clip:        Clip to process.
    :param sigma:       Sigma for Bilateral for pre-blurring (Default: False).
    :param rad:         The luma equivalent of gradfun3's "mask" parameter.
    :param brz_a:       Binarizing thresh for the detail mask.
                        Scaled to clip's depth if between 0 and 1 (inclusive),
                        else assumed to be in native range. (Default: 0.025)
    :param brz_b:       Binarizing thresh for the edge mask.
                        Scaled to clip's depth if between 0 and 1 (inclusive),
                        else assumed to be in native range. (Default: 0.045)

    :return:            Detail mask.
    """
    check_variable_resolution(clip, "detail_mask")

    brz_a = scale_thresh(brz_a, clip)
    brz_b = scale_thresh(brz_b, clip)

    blur = (quick_resample(clip, partial(core.bilateral.Gaussian, sigma=sigma))
            if sigma else clip)

    mask_a = range_mask(get_y(blur), rad=rad)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = core.std.Prewitt(get_y(blur))
    mask_b = core.std.Binarize(mask_b, brz_b)

    mask = core.akarin.Expr([mask_a, mask_b], 'x y max')
    mask = removegrain(mask, 22)
    return removegrain(mask, 11).std.Limiter()


def detail_mask_neo(clip: vs.VideoNode, sigma: float = 1.0,
                    detail_brz: float = 0.05, lines_brz: float = 0.08,
                    blur_func: Callable[[vs.VideoNode, vs.VideoNode, float],
                                        vs.VideoNode] | None = None,
                    edgemask_func: Callable[[vs.VideoNode], vs.VideoNode] = core.std.Prewitt,
                    rg_mode: int | Sequence[int] = 17) -> vs.VideoNode:
    """
    Detail mask aimed at preserving as much detail as possible.

    This mask will catch a whole lot of stuff, including noise and grain.

    :param clip:            Clip to process.
    :param sigma:           Sigma for the detail mask.
                            Higher means more detail and noise will be caught.
    :param detail_brz:      Binarizing for the detail mask.
                            Default values assume a 16bit clip, so you may need to adjust it yourself.
                            Will not binarize if set to 0.
    :param lines_brz:       Binarizing for the prewitt mask.
                            Default values assume a 16bit clip, so you may need to adjust it yourself.
                            Will not binarize if set to 0.
    :param blur_func:       Blurring function used for the detail detection.
                            Must accept the following parameters: ``clip``, ``ref_clip``, ``sigma``.
                            Uses `bilateral.Bilateral` by default.
    :param edgemask_func:   Edgemasking function used for the edge detection.
    :param rg_mode:         Removegrain mode performed on the final output.

    :return:                Detail mask.
    """
    assert check_variable(clip, "detail_mask_neo")

    if not blur_func:
        blur_func = core.bilateral.Bilateral

    detail_brz = scale_thresh(detail_brz, clip)
    lines_brz = scale_thresh(lines_brz, clip)

    clip_y = get_y(clip)
    blur_pf = core.bilateral.Gaussian(clip_y, sigma=sigma / 4 * 3)

    blur_pref = blur_func(clip_y, blur_pf, sigma)
    blur_pref_diff = core.akarin.Expr([blur_pref, clip_y], "x y -").std.Deflate()
    blur_pref = iterate(blur_pref_diff, core.std.Inflate, 4)

    prew_mask = edgemask_func(clip_y).std.Deflate().std.Inflate()

    if detail_brz > 0:
        blur_pref = blur_pref.std.Binarize(detail_brz)
    if lines_brz > 0:
        prew_mask = prew_mask.std.Binarize(lines_brz)

    merged = core.akarin.Expr([blur_pref, prew_mask], "x y +")
    rm_grain = removegrain(merged, rg_mode)

    return depth(rm_grain, clip.format.bits_per_sample).std.Limiter()


def halo_mask(clip: vs.VideoNode, rad: int = 2,
              brz: float = 0.35,
              thmi: float = 0.315, thma: float = 0.5,
              thlimi: float = 0.195, thlima: float = 0.392,
              edgemask: vs.VideoNode | None = None) -> vs.VideoNode:
    """
    Halo mask to catch basic haloing.

    Inspired by the mask from FineDehalo.

    Most of it was copied from there, but some key adjustments have been made
    to center it specifically around masking.

    rx and ry are now combined into rad and expects an integer.
    Float made sense for FineDehalo since it uses DeHalo_alpha for dehaloing,
    but the masks themselves use rounded rx/ry values, so there's no reason to bother with floats here.

    All thresholds are float and will be scaled to ``clip``'s format.
    If thresholds are greater than 1, they will be asummed to be in 8-bit and scaled accordingly.

    :param clip:            Clip to process.
    :param rad:             Radius for the mask.
    :param brz:             Binarizing for shrinking mask (Default: 0.35).
    :param thmi:            Minimum threshold for sharp edges; keep only the sharpest edges.
    :param thma:            Maximum threshold for sharp edges; keep only the sharpest edges.
    :param thlimi:          Minimum limiting threshold; includes more edges than previously, but ignores simple details.
    :param thlima:          Maximum limiting threshold; includes more edges than previously, but ignores simple details.
    :param edgemask:        Edgemask to use. If None, uses :py:func:`vapoursynth.core.std.Prewitt` (Default: None).

    :return:                Halo mask.
    """
    assert check_variable(clip, "halo_mask")

    smax = scale_thresh(1.0, clip)

    thmi, thma, thlimi, thlima = (scale_thresh(t, clip, assume=8) for t in [thmi, thma, thlimi, thlima])

    matrix = [1, 2, 1, 2, 4, 2, 1, 2, 1]

    edgemask = edgemask or get_y(clip).std.Prewitt()

    # Preserve just the strongest edges
    strong = core.akarin.Expr(edgemask, expr=f"x {thmi} - {thlima-thlimi} / {smax} *")
    # Expand to pick up additional halos
    expand = iterate(strong, core.std.Maximum, rad)

    # Having too many intersecting lines will oversmooth the mask. We get rid of those here.
    light = core.akarin.Expr(edgemask, expr=f"x {thlimi} - {thma-thmi} / {smax} *")
    shrink = iterate(light, core.std.Maximum, rad)
    shrink = core.std.Binarize(shrink, scale_thresh(brz, clip))
    shrink = iterate(shrink, core.std.Minimum, rad)
    shrink = iterate(shrink, partial(core.std.Convolution, matrix=matrix), 2)

    # Making sure the lines are actually excluded
    excl = core.akarin.Expr([strong, shrink], expr="x y max")
    # Subtract and boosting to make sure we get the max pixel values for dehaloing
    mask = core.akarin.Expr([expand, excl], expr="x y - 2 *")
    # Additional blurring to amplify the mask
    mask = core.std.Convolution(mask, matrix)
    return core.akarin.Expr(mask, expr="x 2 *").std.Limiter()


def fine_dehalo_mask(clip: vs.VideoNode,
                     rx: float = 2.0, ry: float = 2.0,
                     thmi: float = 80, thma: float = 128,
                     thlimi: float = 50, thlima: float = 100,
                     show_mask: bool | int = False) -> vs.VideoNode:
    """
    Create the mask for fine_dehalo.

    This allows you to use the mask without having to jump through all the other code in fine_dehalo.

    You can return the mask at different stages during the process with `show_mask`.

    * 1 = Full mask (for backwards and fine_dehalo compatibility)

    :param clip:            Clip to process.
    :param rx:              Horizontal radius for halo removal. Must be greater than 1. Will be rounded up.
    :param ry:              Vertical radius for halo removal. Must be greater than 1.  Will be rounded up.
    :param thmi:            Minimum threshold for sharp edges. Keep only the sharpest edges (line edges).
                            To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thma:            Maximum threshold for sharp edges. Keep only the sharpest edges (line edges).
                            To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thlimi:          Minimum limiting threshold. Includes more edges than previously, but ignores simple details.
    :param thlima:          Maximum limiting threshold. Includes more edges than previously, but ignores simple details.
    :param show_mask:       Return mask clip at various stages in the operation. Valid options are 1–7.

    :return:                Halo mask clip.

    :raises ValueError:     ``rx`` or ``ry`` are smaller than 1.0.
    :raises ValueError:     Invalid value for ``show_mask`` is passed.
    """
    assert check_variable(clip, "halo_mask")

    clip_y = get_y(clip)

    if not all(x >= 1 for x in (rx, ry)):
        raise ValueError("halo_mask: '`rx` and `ry` must both be bigger than 1.0!'")

    if show_mask is not False and not (0 < int(show_mask) <= 7):
        raise ValueError("halo_mask: 'Valid values for `show_mask` are 1–7!'")

    bits = get_depth(clip)
    peak = (1 << bits) - 1
    smax = scale_peak(255, peak)
    thmi, thma, thlimi, thlima = map(partial(scale_peak, peak=peak), [thmi, thma, thlimi, thlima])
    rx_i, ry_i = int(math.ceil(rx)), int(math.ceil(rx))

    # Basic edge detection, thresholding will be applied later.
    edges = clip_y.std.Prewitt()

    # Keeps only the sharpest edges (line edges)
    strong = core.akarin.Expr(edges, f"x {thmi} - {thma-thmi} / {smax} *")

    # Extends them to include the potential halos
    large: vs.VideoNode = maxm(strong, rx_i, ry_i)[-1]

    # Includes more edges than previously, but ignores simple details
    light = core.akarin.Expr(edges, f"x {thlimi} - {thlima-thlimi} / {smax} *")

    # Growing the mask
    shrink = maxm(light, sw=rx_i, sh=ry_i, mode=Shapes.ELLIPSE)[-1]
    shrink = core.akarin.Expr(shrink, "x 2 *")
    shrink = minm(shrink, sw=rx_i, sh=rx_i, mode=Shapes.ELLIPSE)[-1]
    shrink = shrink.std.Convolution(matrix=[1] * 9).std.Convolution(matrix=[1] * 9)

    shr_med = core.akarin.Expr([strong, shrink], expr="x y max")

    mask = core.akarin.Expr([large, shr_med], expr="x y - 2 *")
    mask = core.std.Convolution(mask, matrix=[1] * 9)
    mask = core.akarin.Expr([mask], expr="x 2 *").std.Limiter()

    match show_mask:
        case 1: return mask
        case 2: return shrink
        case 3: return edges
        case 4: return strong
        case 5: return light
        case 6: return large
        case 7: return shr_med
        case _: return mask


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

    :param clip:        Clip to process.
    :param rad:         Depth in pixels of the detail/edge masking.
    :param radc:        Chroma equivalent to ``rad``.

    :return:            Range mask.
    """
    assert check_variable(clip, "range_mask")

    if radc == 0:
        clip = get_y(clip)

    if clip.format.color_family == vs.GRAY:  # type:ignore[union-attr]
        ma = _minmax(clip, rad, True)
        mi = _minmax(clip, rad, False)
        mask = core.akarin.Expr([ma, mi], 'x y -')
    else:
        planes = split(clip)
        for i, rad_ in enumerate([rad, radc, radc]):
            ma = _minmax(planes[i], rad_, True)
            mi = _minmax(planes[i], rad_, False)
            planes[i] = core.akarin.Expr([ma, mi], 'x y -')
        mask = join(planes)

    return mask.std.Limiter()


# Helper functions
def _minmax(clip: vs.VideoNode, iterations: int, maximum: bool) -> vs.VideoNode:
    assert check_variable(clip, "_minmax")

    func = core.std.Maximum if maximum else core.std.Minimum

    for i in range(1, iterations + 1):
        coord = [0, 1, 0, 1, 1, 0, 1, 0] if (i % 3) != 1 else [1] * 8
        clip = func(clip, coordinates=coord)

    return clip


class BoundingBox():
    """
    Positional bounding box.

    Basically kagefunc.squaremask, but can be configured and then deferred.

    Uses Position + Size, like provided by GIMP's rectangle selection tool.

    :param pos:     Offset of top-left corner of the bounding box from the top-left corner of the frame.
                    Supports either a :py:attr:`lvsfunc.types.Position` or a tuple that will be converted.
    :param size:    Offset of the bottom-right corner of the bounding box from the top-left corner of the bounding box.
                    Supports either a :py:attr:`lvsfunc.types.Size` or a tuple that will be converted.
    """

    pos: Position
    size: Size

    def __init__(self, pos: Position | tuple[int, int], size: Size | tuple[int, int]):
        self.pos = pos if isinstance(pos, Position) else Position(pos[0], pos[1])
        self.size = size if isinstance(size, Size) else Size(size[0], size[1])

    def get_mask(self, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get a mask representing the bounding box.

        :param ref:             Reference clip for format, resolution, and length.

        :return:                Square mask representing the bounding box.

        :raises ValueError:     Bound exceeds clip size.
        """
        assert check_variable(ref, "get_mask")

        if self.pos.x + self.size.x > ref.width or self.pos.y + self.size.y > ref.height:
            raise ValueError("BoundingBox: Bounds exceed clip size!")

        mask_fmt: vs.VideoFormat = ref.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0)
        white: float = 1 if mask_fmt.sample_type == vs.FLOAT else (1 << ref.format.bits_per_sample) - 1
        mask: vs.VideoNode = ref.std.BlankClip(color=white, format=mask_fmt.id, keep=True)
        mask = mask.std.Crop(self.pos.x, ref.width - (self.pos.x + self.size.x),
                             self.pos.y, ref.height - (self.pos.y + self.size.y))
        mask = mask.std.AddBorders(self.pos.x, ref.width - (self.pos.x + self.size.x),
                                   self.pos.y, ref.height - (self.pos.y + self.size.y))

        return mask.std.Limiter()


class DeferredMask(ABC):
    """
    Deferred masking interface.

    Provides an interface to use different preconfigured masking functions.
    Provides support for ranges, reference frames, and bounding.

    :param range:       A single range or list of ranges to replace,
                        compatible with :py:func:`lvsfunc.misc.replace_ranges`
    :param bound:       A :py:class:`lvsfunc.mask.BoundingBox` or a tuple that will be converted
                        (Default: ``None``, no bounding).
    :param blur:        Blur the bounding mask (Default: False).
    :param refframe:    A single frame number to use to generate the mask
                        or a list of frame numbers with the same length as :py:func:`lvsfunc.types.Range`.

    :raises ValueError: Reference frame and ranges mismatch.
    """

    ranges: list[Range]
    bound: BoundingBox | None
    refframes: list[int | None]
    blur: bool

    def __init__(self, ranges: Range | list[Range] | None = None,
                 bound: BoundingBox | tuple[tuple[int, int], tuple[int, int]] | None = None,
                 *,
                 blur: bool = False, refframes: int | list[int] | None = None):
        self.ranges = ranges if isinstance(ranges, list) else [(0, None)] if ranges is None else [ranges]
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
            self.refframes = list(refframes)

        if len(self.refframes) > 0 and len(self.refframes) != len(self.ranges):
            raise ValueError("DeferredMask: 'Received reference frame and range list size mismatch!'")

    def get_mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        """
        Get the bounded mask.

        :param clip:  Source.
        :param ref:   Reference clip.

        :return:      Bounded mask.
        """
        assert check_variable(clip, "get_mask")
        assert check_variable(ref, "get_mask")

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
                if rf is None:
                    rf = ref.num_frames - 1
                elif rf < 0:
                    rf = ref.num_frames - 1 + rf
                mask = depth(self._mask(clip[rf], ref[rf]), clip.format.bits_per_sample,
                             range=CRange.FULL, range_in=CRange.FULL)
                hm = replace_ranges(hm, core.akarin.Expr([hm, mask*len(hm)], expr="x y max"), range)

        hm = hm.std.Limiter()

        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)

    @abstractmethod
    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        pass


def mt_xxpand_multi(clip: vs.VideoNode,
                    sw: float = 1, sh: float | None = None,
                    mode: Shapes | int = Shapes.ELLIPSE,
                    start: int = 0,
                    m__imum: Callable[..., vs.VideoNode] = core.std.Maximum,
                    planes: list[int] = [0, 1, 2],
                    **m_params: Any) -> list[vs.VideoNode]:
    """
    Mask expanding/inpanding function written by `Zastin <https://github.com/kgrabs>`_.

    Performs multiple Minimums/Maximums.
    """
    assert check_variable(clip, "mt_xxpand_multi")

    planes = normalise_planes(clip, planes)

    params: dict[str, Any] = dict(planes=planes)
    params |= m_params

    sh = sh or sw

    match mode:
        case Shapes.ELLIPSE: coordinates = [[1] * 8, [0, 1, 0, 1, 1, 0, 1, 0],
                                            [0, 1, 0, 1, 1, 0, 1, 0]]
        case Shapes.LOSANGE: coordinates = [[0, 1, 0, 1, 1, 0, 1, 0]] * 3
        case _: coordinates = [[1] * 8] * 3

    clips: list[vs.VideoNode] = [clip]
    end = int(min(sw, sh)) + start

    for x in range(start, end):
        clips += [m__imum(clips[-1], coordinates=coordinates[x % 3], **params)]
    for x in range(end, int(end + sw - sh)):
        clips += [m__imum(clips[-1], coordinates=[0, 0, 0, 1, 1, 0, 0, 0], **params)]
    for x in range(end, int(end + sh - sw)):
        clips += [m__imum(clips[-1], coordinates=[0, 1, 0, 0, 0, 0, 1, 0], **params)
                  .std.Limiter()]

    return clips


maxm = partial(mt_xxpand_multi, m__imum=core.std.Maximum)
minm = partial(mt_xxpand_multi, m__imum=core.std.Minimum)
