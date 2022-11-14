from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Sequence

from vsrgtools import gauss_blur, removegrain
from vstools import (
    ColorRange, FrameRangeN, FrameRangesN, check_variable, check_variable_resolution, core, depth, get_y, iterate, join,
    replace_ranges, scale_thresh, split, vs
)

from .types import Position, Size

__all__ = [
    'BoundingBox',
    'DeferredMask',
    'detail_mask_neo',
    'detail_mask',
    'range_mask'
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

    y = get_y(clip)

    blur = gauss_blur(y, sigma) if sigma else y

    mask_a = range_mask(blur, rad=rad)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = blur.std.Prewitt()
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

    :return:            FrameRangesN mask.
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


class BoundingBox:
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
                        or a list of frame numbers with the same length as :py:func:`lvsfunc.types.FrameRangesN`.

    :raises ValueError: Reference frame and ranges mismatch.
    """

    ranges: FrameRangesN
    bound: BoundingBox | None
    refframes: list[int | None]
    blur: bool

    def __init__(self, ranges: FrameRangeN | FrameRangesN | None = None,
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
                       range_out=ColorRange.FULL, range_in=ColorRange.FULL)
        else:
            hm = core.std.BlankClip(ref, format=ref.format.replace(color_family=vs.GRAY,
                                                                   subsampling_h=0, subsampling_w=0).id)
            for range, rf in zip(self.ranges, self.refframes):
                if rf is None:
                    rf = ref.num_frames - 1
                elif rf < 0:
                    rf = ref.num_frames - 1 + rf
                mask = depth(self._mask(clip[rf], ref[rf]), clip.format.bits_per_sample,
                             range_out=ColorRange.FULL, range_in=ColorRange.FULL)
                hm = replace_ranges(hm, core.akarin.Expr([hm, mask*len(hm)], expr="x y max"), range)

        hm = hm.std.Limiter()

        return hm if self.bound is None else core.std.MaskedMerge(core.std.BlankClip(hm), hm, bm)

    @abstractmethod
    def _mask(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        pass
