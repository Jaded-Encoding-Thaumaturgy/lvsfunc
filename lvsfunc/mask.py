from pathlib import Path

from vstools import FormatsRefClipMismatchError, FrameRangesN, LengthMismatchError, core, replace_ranges, vs

from .util import match_clip

__all__ = [
    'custom_mask_clip',
]


def custom_mask_clip(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
                     imgs: list[str | Path] = [], ranges: FrameRangesN = [],
                     show_mask: bool = True) -> vs.VideoNode:
    """
    Splice in custom masks onto a blank clip to use as a mask clip.

    This is optimised from other implementations I've seen by splicing the masks into a blank clip,
    as opposed to opening up the image, masking, and then moving on to the next image.

    By default, this function returns just the mask.

    :param clip:                        Clip to process.
    :param ref:                         The ref clip. A blank clip will be created based on this.
                                        If `show_mask=False`, this clip will be masked ontop of `clip`.
                                        If `None`, replaced with `clip`.
    :param imgs:                        A list of filepaths to the images.
    :param ranges:                      A list of ranges to "insert" clips into the mask clip.
                                        This must be equal to the amount of `imgs`.
    :param show_mask:                   Whether to return the mask. If False, returns a MaskedMerged clip.

    :return:                            A masked clip using custom masks, or a mask clip.

    :raises FormatsRefClipMismatchError:    `ref` is passed and `clip` and `ref`'s formats do not match.
    :raises ValueError:                     `imgs` and `ranges` length doesn't match.
    """
    if ref:
        FormatsRefClipMismatchError.check(custom_mask_clip, clip, ref)

    LengthMismatchError.check(custom_mask_clip, len(imgs), len(ranges),
                              message="`imgs` and `ranges` must be of the same length!")

    ref = ref or clip
    blank = ref.std.BlankClip(keep=True)

    masks = [match_clip(core.imwri.Read(str(x)), ref, length=True) for x in imgs]

    for mask, frange in zip(masks, ranges):
        blank = replace_ranges(blank, mask, frange)

    if show_mask:
        return blank

    return core.std.MaskedMerge(clip, ref, blank)
