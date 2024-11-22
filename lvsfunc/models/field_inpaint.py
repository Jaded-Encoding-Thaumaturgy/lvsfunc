from dataclasses import dataclass
from typing import Any

from vstools import (
    UnsupportedFieldBasedError,FieldBased, FieldBasedT, PlanesT, core, depth,
                     get_lowest_values, get_peak_value, get_y, inject_self,
                     normalize_seq, vs, padder)
from vsaa import Antialiaser, Nnedi3
from vskernels import Lanczos, Hermite, Point

from .base import Base1xModel

__all__: list[str] = [
    "LFieldInpaint",
]


@dataclass
class LFieldInpaint(Base1xModel):
    """
    Light's Field Inpainting model.

    This model is used to inpaint fields in interlaced content.
    This can be 60i content, or hard-interlaced frames in telecined content.

    DO NOT, UNDER ANY CIRCUMSTANCES, use this model to replace the IVTC process!
    This is strictly intended for dealing with interlaced content,
    and more specifically, interlaced frames such as orphaned fields.
    """

    _model_filename = '1x_field_inpaint_fp32.onnx'

    def __str__(self):
        return 'LFieldInpaint'

    @inject_self
    def apply(
        self,
        clip: vs.VideoNode,
        field_based: FieldBasedT | None = None,
        double_rate: bool = True,
        planes: PlanesT = None,
        **kwargs: Any
    ) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:            The clip to process.
        :param field_based:     The field order. Default: get from clip.
        :param double_rate:     Whether to double the frame rate. This is useful for deinterlacing 60i content.
                                Note that there's no motion compensation in this method.
                                If False, use the field from `field_based`.
                                Default: True.
        :param planes:          The planes to apply the model to. Default: all planes.
        :param kwargs:          Additional keyword arguments.

        :return:                The processed clip.
        """

        self.tff = FieldBased.from_param_or_video(field_based, clip, True, self.apply)
        self.double_rate = double_rate

        if not self.tff.is_inter:
            raise UnsupportedFieldBasedError(
                f'`field_based` must be either TFF or BFF, not {self.tff}!',
                self.apply
            )

        pref = Lanczos.resample(clip, vs.YUV444PS)
        pref = self.tff.apply(pref)
        pref = self._pad_crop(pref)
        pref = self._greenweave(pref)
        pref = FieldBased.PROGRESSIVE.apply(pref)

        proc = super().apply(pref, planes=planes, **kwargs)
        proc = Point.shift(proc, -1.0 * self.tff.is_tff, 0.0)

        woven = self._weave_original_field(pref, proc)
        woven = self._pad_crop(woven, crop=True)

        return Hermite.resample(woven, clip)

    def _pad_crop(self, clip: vs.VideoNode, crop: bool = False, px: int = 16) -> vs.VideoNode:
        """Pad or crop the clip."""

        if crop:
            return clip.std.Crop(top=px, bottom=px)

        return padder.MIRROR(clip, top=px, bottom=px)

    def _greenweave(self, clip: vs.VideoNode) -> vs.VideoNode:
        """Create a clip with green fields interwoven."""

        colors = normalize_seq(
            [get_peak_value(clip), *get_lowest_values(clip)[1:]],
            clip.format.num_planes
        )

        clip = clip.std.SeparateFields(self.tff.is_tff)
        blank = clip.std.BlankClip(color=colors, keep=True)

        if self.tff.is_tff:
            clips = [clip, blank]
        else:
            clips = [blank, clip]

        woven = core.std.Interleave(clips)
        woven = woven.std.DoubleWeave(not self.tff.is_tff)

        woven = woven[self.tff.is_tff::2]

        if not self.double_rate:
            woven = woven[::2]

        return woven

    def _weave_original_field(self, clip: vs.VideoNode, proc_clip: vs.VideoNode) -> vs.VideoNode:
        """Weave the original field back in."""

        sep_clip = clip.std.SeparateFields(self.tff.is_tff)
        sep_proc = proc_clip.std.SeparateFields(not self.tff.is_tff)

        if self.tff.is_tff:
            clips = [sep_clip, sep_proc]
        else:
            clips = [sep_proc, sep_clip]

        woven = core.std.Interleave(clips)
        woven = woven.std.DoubleWeave(not self.tff.is_tff)

        return woven[self.tff.is_tff::4]
