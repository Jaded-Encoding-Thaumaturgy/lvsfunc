from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from math import ceil
from typing import Any

from stgpytools import (MISSING, CustomIndexError, CustomNotImplementedError,
                        CustomTypeError, CustomValueError,
                        DependencyNotFoundError, FileNotExistsError, SPath,
                        SPathLike)
from vsdeinterlace import fix_telecined_fades
from vsexprtools import ExprOp
from vsmasktools import Morpho
from vsrgtools import gauss_blur
from vstools import (FieldBased, FieldBasedT, FunctionUtil, Keyframes,
                     Timecodes, UnsupportedFieldBasedError, core, plane,
                     replace_ranges, vs)
from vsdenoise import prefilter_to_full_range

from .exceptions import InvalidCycleError, InvalidMatchError
from .info import (FreezeFrame, InterlacedFade, OrphanField, Section,
                   VDecParams, VfmParams, WobblyMeta, WobblyVideo)
from .types import Match, OrphanMatch


@dataclass
class WobblyParsed:
    """Dataclass representing the contents of a parsed Wobbly file."""

    work_clip: WobblyVideo
    """Information about how to handle the work clip used in Wobbly itself."""

    meta: WobblyMeta
    """Meta information about Wobbly."""

    field_order: FieldBasedT
    """The field order represented as a FieldBased object."""

    matches: list[str]
    """
    The field matches. See this webpage for more information:
    <http://underpop.online.fr/f/ffmpeg/help/p_002fc_002fn_002fu_002fb-meaning.htm.gz>
    """

    combed_frames: set[int]
    """A set of combed frames. Frames with interlaced fades will be excluded."""

    orphan_frames: list[OrphanField]
    """A set of OrphanField objects representing an orphan."""

    decimations: set[int]
    """A set of frames to decimate."""

    sections: list[Section]
    """A set of Section objects representing the scenes of a video."""

    interlaced_fades: list[InterlacedFade]
    """A set of InterlacedFade objects representing frames marked as interlaced fades."""

    freeze_frames: list[FreezeFrame]
    """A list of FreezeFrame objects representing ranges to freeze, and which frames to replace them with."""

    vfm_params: VfmParams
    """An object containing all the vivtc.VFM parameters passed through wibbly."""

    vdecimate_params: VDecParams
    """An object containing all the vivtc.VDecimate parameters passed through wibbly."""

    def __init__(self, wobbly_path: SPathLike) -> None:
        """
        Parse the wobbly file.

        :param wobbly_path:     Path to the .wob file Wobbly outputs. If the path does not end
                                with a .wob extension, it will be implicitly added.
        """
        self._func = self.__class__.__name__

        if not (wob_file := SPath(wobbly_path)).suffix == ".wob":
            wob_file = wob_file.parent / (wob_file.name + ".wob")

        if not wob_file.exists():
            raise FileNotExistsError(f"Could not find the file, \"{wob_file}\"!", self._func)

        with open(wob_file, "r") as f:
            self._wob_data = dict(json.load(f))

        # Obtaining the values.
        self.work_clip = WobblyVideo(  # type:ignore[call-arg]
            self._get_val("input file"),
            self._get_val("source filter"),
            self._get_val("trim", []),
            Fraction(*self._get_val("input frame rate", [30000, 1001]))
        )

        self.meta = WobblyMeta(
            self._get_val("wobbly version", -1),
            self._get_val("project format version", -1),
            self._get_val("generated with", None)
        )

        self.vfm_params = VfmParams(**dict(self._get_val("vfm parameters", {})))
        self.vdecimate_params = VDecParams(**dict(self._get_val("vdecimate parameters", {})))

        if self.vdecimate_params.cycle != 5:
            raise InvalidCycleError("Wobbly currently only supports a cycle of 5!", self._func)

        self.field_order = FieldBased.from_param(self.vfm_params.order + 1, self._func)

        if not self.field_order.is_inter:
            raise UnsupportedFieldBasedError("Your source may not be Progressive!", self._func)

        self.matches = self._get_val("matches", [])
        self.combed_frames = self._get_val("combed frames", set())
        self.decimated_frames = self._get_val("decimated frames", set())

        if not bool(len(illegal_chars := set(self.matches) - {*Match.__args__})):  # type:ignore[attr-defined]
            raise InvalidMatchError(f"Illegal characters found in matches: {tuple(illegal_chars)}", self._func)

        self._get_sections()
        self._get_interlaced_fades()
        self._get_freeze_frames()
        self._get_orphan_frames()

        # Further sanitizing where necessary.
        self._remove_ifades_from_combed()

    def apply(
        self,
        clip: vs.VideoNode | None = None,
        tff: FieldBasedT = None,
        orphan_handling: bool | OrphanMatch | list[OrphanMatch] = False,
        mask_orphans: bool = False,
        **qtgmc_kwargs: Any
    ) -> vs.VideoNode:
        """
        Apply all the Wobbly processing to a given clip.

        :param clip:                Clip to process. If None, index the `input_file` file as defined
                                    in the original Wobbly file, using the same indexer Wobbly used.
                                    Default: None.
        :param tff:                 Top-Field-First. If None, obtain this from the parsed wobbly file.
                                    If it can't obtain it from that, it will try to obtain it from the VideoNode.
                                    Default: None.
        :param orphan_handling:     Deinterlace orphan fields. This may restore motion that is otherwise lost,
                                    at the heavy cost of speed and potential deinterlacing artifacting.
                                    If an OrphanMatch or a list of OrphanMatch is passed instead, it will only
                                    handle orphan fields that were matched to the selected matches.
                                    Default: False.
        :param mask_orphans:        Mask orphan fields get get deinterlaced. This may miss some combing,
                                    so make sure to check! Setting this to `True` will also make the
                                    `_orphan_mask` attribute available.
                                    Default: False.
        :param qtgmc_kwargs:        Keyword arguments to pass on to QTGMC.

        :return:                    Clip with wobbly processing applied, and optionally orphan fields deinterlaced.
        """
        if clip is None:
            clip = self.work_clip.source()

        func = FunctionUtil(clip, self.apply, None, vs.YUV)

        wclip = FieldBased.from_param(tff or self.field_order, self.apply).apply(func.work_clip)

        if orphan_handling:
            OrphanMatches = OrphanMatch.__args__  # type:ignore[attr-defined]

            if isinstance(orphan_handling, bool):
                orphan_handling = OrphanMatches
            # ! TODO: Find a better way to do this.
            elif all(m in ("b", "n", "p", "u") for m in list(orphan_handling)):
                orphan_handling = list(orphan_handling)  # type:ignore[list-item]
            else:
                raise CustomTypeError(
                    f"Expected type: (bool, ['b', 'n', 'p', 'u']), "
                    f"not {type(orphan_handling)}!", self.apply
                )

            orphans_to_process = list[OrphanField]()

            # TODO: this could almost definitely be handled cleaner.
            if orphan_handling == OrphanMatches:
                orphans_to_process = list(self.orphan_frames)
            else:
                for orphan in self.orphan_frames:
                    if orphan.match in orphan_handling:
                        orphans_to_process += [orphan]

        # Setting matches to 'c' matches if orphan handling enabled.
        matches_to_process = self.matches

        if orphan_handling:
            for orphan in self.orphan_frames:
                if orphan.match in orphan_handling:
                    matches_to_process[orphan.framenum] = "c"

        if matches_to_process:
            wclip = self._apply_fieldmatches(wclip, matches_to_process)

        if self.freeze_frames:
            wclip = self._apply_freezeframes(wclip)

        if self.decimated_frames:
            wclip = self._mark_framerates(wclip)

        if self.interlaced_fades:
            wclip = self._apply_interlaced_fades(wclip)

        if orphan_handling:
            wclip = self._deinterlace_orphans(wclip, orphans_to_process, mask_orphans, **qtgmc_kwargs)

        if self.combed_frames:
            wclip = self._apply_combed_markers(wclip)

        if self.decimated_frames:
            wclip = wclip.std.DeleteFrames(self.decimated_frames)

        wclip = FieldBased.PROGRESSIVE.apply(wclip)

        return func.return_clip(wclip)

    def _get_val(self, key: str, fallback: Any = MISSING) -> Any:
        if (val := self._wob_data.get(key, fallback)) is MISSING:
            raise CustomValueError(f"Could not get the value from \"{key}\" in the wobbly file!", self._func)

        return val

    def _get_sections(self) -> None:
        self.sections = list(
            Section(section.get("start", 0), section.get("presets", []))
            for section in self._get_val("sections", [{}])
        )

    def _get_interlaced_fades(self) -> None:
        self.interlaced_fades = list(
            InterlacedFade(ifade.get("frame"), ifade.get("field_difference"))
            for ifade in self._get_val("interlaced fades", [{}])
        )

    def _get_freeze_frames(self) -> None:
        self.freeze_frames = [FreezeFrame(*tuple(freezes[0])) for freezes in zip(self._get_val("frozen frames", ()))]

    def _get_orphan_frames(self) -> None:
        self.orphan_frames = list[OrphanField]()

        try:
            for i in self._get_val("orphan frames", []):
                self.orphan_frames += [OrphanField(i, self.matches[i])]
        except IndexError as e:
            raise CustomIndexError(" ".join([str(e), f"(frame: {i})"]), self._func)

    def _remove_ifades_from_combed(self) -> None:
        if self.interlaced_fades:
            self.combed_frames = self.combed_frames - set(i.framenum for i in self.interlaced_fades)

    def _apply_fieldmatches(self, clip: vs.VideoNode, matches: list[str]) -> vs.VideoNode:
        clip = clip.fh.FieldHint(None, self.field_order, "".join(matches))

        match_clips = dict[str, vs.VideoNode]()

        for match in set(matches):
            match_clips |= {match: clip.std.SetFrameProps(wobbly_match=match)}

        return clip.std.FrameEval(lambda n: match_clips.get(matches[n]))


    def _mark_framerates(self, clip: vs.VideoNode) -> vs.VideoNode:
        """Mark the framerates per cycle."""
        framerates = [
            self.work_clip.frame_rate.numerator / self.vdecimate_params.cycle * i
            for i in range(self.vdecimate_params.cycle, 0, -1)
        ]

        fps_clips = [
            clip.std.AssumeFPS(None, int(fps), self.work_clip.frame_rate.denominator)
            .std.SetFrameProps(
                wobbly_cycle_fps=int(fps // 1000),
                _DurationNum=int(fps),
                _DurationDen=self.work_clip.frame_rate.denominator
            ) for fps in framerates
        ]

        split_decimations = [
            [
                j for j in range(i * self.vdecimate_params.cycle, (i + 1) * self.vdecimate_params.cycle)
                if j in self.decimations
            ]
            for i in range(0, ceil((max(self.decimated_frames) + 1) / self.vdecimate_params.cycle))
        ]

        n_split_decimations = len(split_decimations)

        indices = [
            0 if (sd_idx := ceil(n / self.vdecimate_params.cycle)) >= n_split_decimations
            else len(split_decimations[sd_idx]) for n in range(clip.num_frames)
        ]

        return clip.std.FrameEval(lambda n: fps_clips[indices[n]])

    def _apply_freezeframes(self, clip: vs.VideoNode) -> vs.VideoNode:
        # I realise this is slower, but props!
        for freeze in self.freeze_frames:
            fclip = clip.std.FreezeFrames(freeze.start, freeze.end, freeze.replacement)

            fclip = fclip.std.SetFrameProps(
                wobbly_freeze_start=freeze.start,
                wobbly_freeze_end=freeze.end,
                wobbly_freeze_replacement=freeze.replacement
            )

            clip = replace_ranges(clip, fclip, [(freeze.start, freeze.end)])

        return clip

        # ! TODO: Test this faster method (but without props)!
        # wclip = wclip.std.FreezeFrames(*zip(*self.freeze_frames))

    def _apply_interlaced_fades(self, clip: vs.VideoNode) -> vs.VideoNode:
        # TODO: Figure out how to get the right `color` param per frame with an eval.
        # TODO: Check if other ftf works better and implement that

        clip = clip.std.SetFrameProps(wobbly_ftf=False)
        ftf = fix_telecined_fades(clip, colors=0, planes=0).std.SetFrameProps(wobbly_ftf=True)

        return replace_ranges(clip, ftf, [f.framenum for f in self.interlaced_fades])

    def _deinterlace_orphans(
        self, clip: vs.VideoNode,
        orphans: list[OrphanField],
        mask_orphans: bool = False,
        **kwargs: Any
    ) -> vs.VideoNode:
        try:
            from havsfunc import QTGMC  # type:ignore[import]
        except ModuleNotFoundError:
            raise DependencyNotFoundError(self.apply, "havsfunc")

        n_frames = [o.framenum for o in orphans if o.match == "n"]
        b_frames = [o.framenum for o in orphans if o.match == "b"]

        # ! TODO: Figure out how to better deinterlace orphans, hopefully remove QTGMC dep one day.
        # This is almost entirely copied from old code. I need to run tests at some point.
        field_order = FieldBased.from_video(clip)

        kwargs.pop("TFF", None)

        qtgmc_kwargs: dict[str, Any] = dict(
            TR0=2, TR1=2, TR2=2, Sharpness=0, Lossless=1, InputType=0,
            Rep0=3, Rep1=3, Rep2=2, SourceMatch=3, EdiMode='EEDI3+NNEDI3', EdiQual=2,
            Sbb=3, SubPel=4, SubPelInterp=2, opencl=False, RefineMotion=True,
            Preset='Placebo', MatchPreset='Placebo', MatchPreset2='Placebo'
        ) | kwargs | dict(FPSDivisor=1)

        deint_n = QTGMC(clip, TFF=field_order.is_tff, **qtgmc_kwargs)[not field_order.field::2]
        deint_b = QTGMC(clip, TFF=field_order.is_tff, **qtgmc_kwargs)[field_order.field::2]

        # ! TODO: improve this. It seems to work surprisingly well, but it's not perfect.
        if mask_orphans and all(hasattr(core, plugin) for plugin in ("motionmask", "comb")):
            base_clip = plane(clip, 0)
            base_clip = prefilter_to_full_range(base_clip, 4.5)

            comb_mask = base_clip.comb.CombMask(6, 4)

            n_motion_clip = replace_ranges(base_clip, base_clip[1:] + base_clip[-1], [n - 1 for n in n_frames])
            b_motion_clip = replace_ranges(base_clip, base_clip[0] + base_clip[:-1], [n - 1 for n in n_frames])

            motionmask_args = (None, 1, 1, 255)
            deint_mask_n = n_motion_clip.motionmask.MotionMask(*motionmask_args)
            deint_mask_n_off = base_clip.motionmask.MotionMask(*motionmask_args)
            deint_mask_b = base_clip.motionmask.MotionMask(*motionmask_args)
            deint_mask_b_off = b_motion_clip.motionmask.MotionMask(*motionmask_args)

            deint_mask_n = ExprOp.MAX(comb_mask, deint_mask_n, deint_mask_n_off)
            deint_mask_b = ExprOp.MAX(comb_mask, deint_mask_b, deint_mask_b_off)

            deint_mask = deint_mask_n.std.BlankClip(keep=True)
            deint_mask = replace_ranges(deint_mask, deint_mask_n, n_frames)
            deint_mask =  replace_ranges(deint_mask, deint_mask_b, b_frames)

            deint_mask = Morpho.closing(deint_mask, 3)
            deint_mask = Morpho.inpand(deint_mask, 1)
            deint_mask = Morpho.expand(deint_mask, 14)
            deint_mask = Morpho.closing(deint_mask, 4)
            deint_mask = deint_mask.std.Binarize().std.Limiter()
            deint_mask = gauss_blur(deint_mask, 1.5)

            self._orphan_mask = deint_mask

            deint_n = clip.std.MaskedMerge(deint_n, deint_mask)
            deint_b = clip.std.MaskedMerge(deint_b, deint_mask)

        deint_n = deint_n.std.SetFrameProps(wobbly_orphan_deinterlace="n")
        deint_b = deint_b.std.SetFrameProps(wobbly_orphan_deinterlace="b")

        # ! TODO: Compare the previous frame and 3 frames previous (because animated on twos) to check for similarity.
        # If we can be smart about copying over frames, we can avoid an unnecessary deinterlacing step.
        out = replace_ranges(clip, deint_n, n_frames)
        out = replace_ranges(out, deint_b, b_frames)

        return out

    def _apply_combed_markers(self, clip: vs.VideoNode) -> vs.VideoNode:
        clip = clip.std.SetFrameProps(wobbly_combed=0)
        combed = clip.std.SetFrameProps(wobbly_combed=1)

        return replace_ranges(clip, combed, list(self.combed_frames))

    @property
    def keyframes(self) -> Keyframes:
        """Return a Keyframes object created using sections."""
        return Keyframes([i.framenum for i in self.sections])

    #! TODO: Calculate the timecodes from the information provided, not a clip.
    @property
    def timecodes(self) -> Timecodes:
        """The timecodes represented as a Timecode object."""
        raise CustomNotImplementedError("Timecodes have not yet been implemented!", self._func)
