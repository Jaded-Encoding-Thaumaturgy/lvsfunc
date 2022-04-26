"""
    Tests to make sure lvsfunc functions return the expected values.
    A lot of methods were taken from vsutil.
"""
import contextlib
import os
import shutil
import unittest
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

import lvsfunc as lvf
import vapoursynth as vs
import vsutil

core = vs.core

__all__: List[str] = []


class LvsfuncTests(unittest.TestCase):
    # Common arguments
    DEPS: str = "dependencies"

    DEF_LENGTH: int = 100

    DEF_WIDTH: int = 160
    DEF_HEIGHT: int = 120

    COLOR_BLACK: List[int] = [0, 128, 128]
    COLOR_WHITE: List[int] = [255, 128, 128]

    COLOR_BLUE: List[int] = [0, 255, 0]
    COLOR_GREEN: List[int] = [128, 0, 0]
    COLOR_RED: List[int] = [0, 0, 255]
    COLOR_YELLOW: List[int] = [255, 0, 255]

    # 16/9 256x144 clip
    SMALL_WIDTH: int = 256
    SMALL_HEIGHT: int = 144

    # 16/9 1024x576 clip
    MEDIUM_WIDTH: int = 1024
    MEDIUM_HEIGHT: int = 576

    # 16/9 1920x1080 clip
    BIG_WIDTH: int = 1920
    BIG_HEIGHT: int = 1080

    # A bunch of blank clips with different (relatively) common formats
    DEF_VALUES: Dict[str, Any] = {
        'width': DEF_WIDTH, 'height': DEF_HEIGHT,
        'color': COLOR_BLACK, 'length': DEF_LENGTH,
        'fpsnum': 24000, 'fpsden': 1001
    }

    YUV420P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, **DEF_VALUES)
    YUV420P10_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P10, **DEF_VALUES)
    YUV420P16_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P16, **DEF_VALUES)
    YUV420PS_CLIP: vs.VideoNode = vsutil.depth(YUV420P8_CLIP, 32, dither_type=vsutil.Dither.NONE)

    YUV444P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P8, **DEF_VALUES)
    YUV444P10_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P10, **DEF_VALUES)
    YUV444P16_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P16, **DEF_VALUES)
    YUV444PS_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444PS, **DEF_VALUES)

    RGB24_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGB24)
    RGBS_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGBS)

    YUV422P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV422P8, **DEF_VALUES)
    YUV410P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV410P8, **DEF_VALUES)
    YUV411P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV411P8, **DEF_VALUES)
    YUV440P8_CLIP = core.std.BlankClip(format=vs.YUV440P8, **DEF_VALUES)

    del DEF_VALUES['color']

    GRAY8_CLIP = core.std.BlankClip(format=vs.GRAY8, **DEF_VALUES)
    GRAY16_CLIP = core.std.BlankClip(format=vs.GRAY16, **DEF_VALUES)
    GRAYS_CLIP = core.std.BlankClip(format=vs.GRAYS, **DEF_VALUES)

    # Other kinds of blank clips
    SMALLER_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=SMALL_WIDTH, height=SMALL_HEIGHT)
    MEDIUM_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH, height=MEDIUM_HEIGHT)
    BIGGER_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=BIG_WIDTH, height=BIG_HEIGHT)

    BLACK_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_BLACK, **DEF_VALUES)
    WHITE_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_WHITE, **DEF_VALUES)

    VARIABLE_FORMAT_CLIP: vs.VideoNode = core.std.Interleave([YUV420P8_CLIP, YUV444P8_CLIP], mismatch=True)

    # 30p clips for deinterlacing functions
    BLACK_SAMPLE_CLIP_30p: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH,
                                                             height=MEDIUM_HEIGHT, color=COLOR_BLACK,
                                                             length=DEF_LENGTH, fpsnum=30000, fpsden=1001)
    BLACK_SAMPLE_CLIP_30p = core.std.SetFieldBased(BLACK_SAMPLE_CLIP_30p, value=2)
    WHITE_SAMPLE_CLIP_30p: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH,
                                                             height=MEDIUM_HEIGHT, color=COLOR_WHITE,
                                                             length=DEF_LENGTH, fpsnum=30000, fpsden=1001)
    BLACK_SAMPLE_CLIP_30p = core.std.SetFieldBased(WHITE_SAMPLE_CLIP_30p, value=2)

    # Coloured clips
    BLUE_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_BLUE,
                                                        width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    GREEN_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_GREEN,
                                                         width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    RED_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_RED,
                                                       width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    YELLOW_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_YELLOW,
                                                          width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)

    # Additional dependencies
    SHADER_FILE: str = f"{DEPS}/FSRCNNX_x2_16-0-4-1.glsl"

    # Basic assertions
    def assert_same_dimensions(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same width and height.
        """
        self.assertEqual(a.height, b.height, f"Same height expected, was {a.height} and {b.height}.")
        self.assertEqual(a.width, b.width, f"Same width expected, was {a.width} and {b.width}.")

    def assert_same_format(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same format (but not necessarily size).
        """
        self.assertEqual(a.format.id, b.format.id, f"Same format expected, was {a.format.id} and {b.format.id}.")

    def assert_same_bitdepth(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same number of bits per sample.
        """
        assert a.format
        assert b.format

        self.assertEqual(a.format.bits_per_sample, b.format.bits_per_sample,
                         f"Same depth expected, was {a.format.bits_per_sample} "
                         f"and {b.format.bits_per_sample}.")

    def assert_same_length(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same length
        """
        self.assertEqual(len(a), len(b),
                         f"Same number of frames expected, was {len(a)} and {len(b)}.")

    def assert_same_metadata(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same height, width, format, depth, and length.
        """
        self.assert_same_format(a, b)
        self.assert_same_dimensions(a, b)
        self.assert_same_length(a, b)

    def assert_returns_callable(self, func: Any) -> None:
        """
        Assert that the function returns a callable.
        """
        try:
            assert callable(func)
        except AssertionError:
            raise ValueError(f"Expected function to return a callable, was {func}.")

    def assert_same_frame(self, a: vs.VideoNode, b: vs.VideoNode, frameno: int = 0) -> None:
        """
        Assert that two frames are identical. Only the first frame of the arguments is used.
        """
        diff = core.std.PlaneStats(a, b)
        frame = diff.get_frame(frameno)
        self.assertEqual(frame.props.PlaneStatsDiff, 0,
                         f"Same frame expected, was {frame.props.PlaneStatsDiff}.")

    def assert_same_framerate(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same framenum and frameden.
        """
        self.assertEqual(a.fps, b.fps, f"Same framerate expected, was {a.fps} and {b.fps}.")

    def assert_not_same_frame(self, a: vs.VideoNode, b: vs.VideoNode, frameno: int = 0) -> None:
        """
        Assert that two frames are NOT identical. Only the first frame of the arguments is used.
        """
        diff = core.std.PlaneStats(a, b)
        frame = diff.get_frame(frameno)
        self.assertNotEqual(frame.props.PlaneStatsDiff, 0,
                            f"Different frame expected, was {frame.props.PlaneStatsDiff}.")

    def assert_length(self, clip: vs.VideoNode, length: int) -> None:
        """
        Assert that a clip is a certain length.
        """
        try:
            assert len(clip) == length
        except AssertionError:
            raise ValueError(f"Expected clip to have a length of {length}, was {len(clip)}")

    def assert_framerate(self, clip: vs.VideoNode, fps: Fraction) -> None:
        """
        Assert that a clip has a certain framerate.
        """
        try:
            assert clip.fps == fps
        except AssertionError:
            raise ValueError(f"Expected clip to have a framerate of {fps}, was {clip.fps}.")

    def assert_variable_format(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip is of a variable format.
        """
        try:
            assert clip.format is None
        except AssertionError:
            raise ValueError(f"Expected clip to have a variable format, was {clip.format.id}.")

    def assert_variable_dimensions(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip is with variable dimensions.
        """
        try:
            assert 0 in (clip.width, clip.height)
        except AssertionError:
            raise ValueError(f"Expected clip to have variable dimensions, was {clip.width} and {clip.height}.")

    def assert_dimensions(self, clip: vs.VideoNode, width: int, height: int) -> None:
        """
        Assert that a clip has a specific width and height.
        """
        self.assertEqual(clip.width, width)
        self.assertEqual(clip.height, height)

    def assert_runs(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip returns a frame.
        """
        try:
            assert clip.get_frame(0)
        except AssertionError:
            raise ValueError("Expected for clip to return a frame.")

    def assert_prop(self, clip: vs.VideoNode, prop: str, ptype: Any) -> None:
        """
        Assert that a clip returns a frame.
        """
        try:
            assert lvf.util.get_prop(clip.get_frame(0), prop, ptype)
        except AssertionError:
            raise ValueError(f"Expected clip to have {prop} property.")


# lvsfunc.aa
class LvsfuncTestAa(LvsfuncTests):
    def test_clamp_aa(self) -> None:
        clip = lvf.aa.clamp_aa(src=self.YUV420P8_CLIP, weak=self.YUV420P8_CLIP, strong=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_taa(self) -> None:
        clip = lvf.aa.taa(clip=self.YUV420P8_CLIP, aafun=lvf.aa.nnedi3())
        self.assert_runs(clip)

    def test_nnedi3(self) -> None:
        func = lvf.aa.nnedi3()
        self.assert_returns_callable(func)

    def test_eedi3(self) -> None:
        func = lvf.aa.eedi3()
        self.assert_returns_callable(func)

    def test_nneedi3_clamp(self) -> None:
        clip = lvf.aa.nneedi3_clamp(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_transpose_aa(self) -> None:
        clip = lvf.aa.transpose_aa(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_upscaled_sraa(self) -> None:
        clip = lvf.aa.upscaled_sraa(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

        clip_down = lvf.aa.upscaled_sraa(clip=self.YUV420P8_CLIP, width=self.SMALL_WIDTH, height=self.SMALL_HEIGHT)
        self.assert_dimensions(clip_down, width=self.SMALL_WIDTH, height=self.SMALL_HEIGHT)

    def test_based_aa(self) -> None:
        clip = lvf.aa.based_aa(self.YUV420P8_CLIP, shader_file=self.SHADER_FILE)
        self.assert_runs(clip)


# lvsfunc.comparison
class LvsfuncTestComparison(LvsfuncTests):
    def test_compare(self) -> None:
        clip = lvf.comparison.compare(clip_a=self.BLACK_SAMPLE_CLIP, clip_b=self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_same_format(clip, self.RGB24_CLIP)

        clip_no_resample = lvf.comparison.compare(clip_a=self.YUV420P8_CLIP, clip_b=self.YUV420P8_CLIP,
                                                  force_resample=False, print_frame=False)
        self.assert_same_format(clip_no_resample, self.YUV420P8_CLIP)
        self.assert_same_frame(clip_no_resample, self.BLACK_SAMPLE_CLIP, 0)

        clip_mismatch = lvf.comparison.compare(clip_a=self.YUV420P8_CLIP, clip_b=self.YUV420P10_CLIP,
                                               force_resample=False, mismatch=True)
        self.assert_variable_format(clip_mismatch)

    def test_stack_compare(self) -> None:
        clip = lvf.comparison.stack_compare(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 1024, 864)

    def test_stack_planes(self) -> None:
        clip = lvf.comparison.stack_planes(self.YUV420P8_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, int(self.DEF_WIDTH / 2 + self.DEF_WIDTH), self.DEF_HEIGHT)
        self.assert_same_format(clip, self.GRAY8_CLIP)

        clip_vert = lvf.comparison.stack_planes(self.YUV420P8_CLIP, stack_vertical=True)
        self.assert_dimensions(clip_vert, self.DEF_WIDTH, int(self.DEF_HEIGHT / 2 + self.DEF_HEIGHT))

        clip_444 = lvf.comparison.stack_planes(self.YUV444P8_CLIP)
        self.assert_dimensions(clip_444, self.DEF_WIDTH * 3, self.DEF_HEIGHT)

        clip_444_vert = lvf.comparison.stack_planes(self.YUV444P8_CLIP, stack_vertical=True)
        self.assert_dimensions(clip_444_vert, self.DEF_WIDTH, self.DEF_HEIGHT * 3)

    def test_diff_hardsub_mask(self) -> None:
        clip = lvf.comparison.diff_hardsub_mask(self.YUV420P8_CLIP, self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_diff(self) -> None:
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                clip = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
                clip_interleave = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
                                                      interleave=True)
                clip_exclude = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
                                                   exclusion_ranges=[(1, self.BLACK_SAMPLE_CLIP.num_frames)])

        self.assert_runs(clip)  # type:ignore[arg-type]
        self.assert_dimensions(clip, 1024, 864)  # type:ignore[arg-type]

        clip_text = self.BLACK_SAMPLE_CLIP.text.FrameNum(9).text.Text("Clip A")
        self.assert_same_frame(clip_interleave, clip_text, 0)  # type:ignore[arg-type]

        self.assert_length(clip_exclude, 1)  # type:ignore[arg-type]

    def test_interleave(self) -> None:
        clip = lvf.comparison.interleave(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_same_frame(clip, self.BLACK_SAMPLE_CLIP, 0)

    def test_split(self) -> None:
        clip = lvf.comparison.split(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_tile(self) -> None:
        clip = lvf.comparison.tile(
            self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP,
            self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
            self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP,
        )
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH * 3, self.DEF_HEIGHT * 3)

    def test_stack_vertical(self) -> None:
        clip = lvf.comparison.stack_vertical(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH, self.DEF_HEIGHT * 2)

    def test_stack_horizontal(self) -> None:
        clip = lvf.comparison.stack_horizontal(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH * 2, self.DEF_HEIGHT)


# lvsfunc.deblock
class LvsfuncTestDeblock(LvsfuncTests):
    MOD8_WIDTH = 128
    MOD8_HEIGHT = 72

    MOD8_YUV_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MOD8_WIDTH, height=MOD8_HEIGHT)
    MOD8_RGB_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGB24, width=MOD8_WIDTH, height=MOD8_HEIGHT)

    def test_vsdpir(self) -> None:
        clip = lvf.deblock.vsdpir(self.MOD8_YUV_CLIP, matrix=lvf.types.Matrix.BT709)
        self.assert_runs(clip)

        clip_rgb = lvf.deblock.vsdpir(self.MOD8_RGB_CLIP)
        self.assert_same_format(clip_rgb, self.RGB24_CLIP)

        clip_444 = lvf.deblock.vsdpir(self.YUV420P16_CLIP, i444=True, matrix=lvf.types.Matrix.BT709)
        self.assert_same_format(clip_444, self.YUV444P16_CLIP)

    def test_autodb_dpir(self) -> None:
        input_clip = core.std.SetFrameProps(self.MOD8_YUV_CLIP, _PictType=b'I')

        clip = lvf.deblock.autodb_dpir(input_clip, matrix=lvf.types.Matrix.BT709)
        self.assert_runs(clip)

        # clip_props = lvf.deblock.autodb_dpir(input_clip, write_props=True, matrix=lvf.types.Matrix.BT709)
        # self.assert_prop(clip_props, 'Adb_EdgeValRefDiff', float)  # This errors and idk why


# lvsfunc.dehalo
class LvsfuncTestDehalo(LvsfuncTests):
    def test_bidehalo(self) -> None:
        clip = lvf.dehalo.bidehalo(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_masked_dha(self) -> None:
        clip = lvf.dehalo.masked_dha(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_fine_dehalo(self) -> None:
        clip = lvf.dehalo.fine_dehalo(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)


# lvsfunc.dehardsub
class LvsfuncTestDehardsub(LvsfuncTests):
    ...


# lvsfunc.deinterlace
class LvsfuncTestDeinterlace(LvsfuncTests):
    def create_pulldown_clip(self) -> vs.VideoNode:
        """
        .. warning::
            This function has not been properly implemented yet!

        Create a test 3:2 pulldown clip.
        """
        clip = lvf.comparison.interleave(blue=self.BLUE_SAMPLE_CLIP,
                                         green=self.GREEN_SAMPLE_CLIP,
                                         red=self.RED_SAMPLE_CLIP,
                                         yellow=self.YELLOW_SAMPLE_CLIP)
        clip = core.std.AssumeFPS(clip, self.BLACK_SAMPLE_CLIP)[2::]
        clip = core.std.SeparateFields(clip, tff=True)
        clip = core.std.SelectEvery(clip, cycle=8, offsets=[0, 1, 2, 3, 2, 5, 4, 7, 6, 7])
        clip = core.std.DoubleWeave(clip, tff=True)[4::1]

        return clip

    def test_sivtc(self) -> None:
        clip = lvf.deinterlace.sivtc(self.BLACK_SAMPLE_CLIP_30p)
        print(clip.num_frames)
        self.assert_runs(clip)
        self.assert_length(clip, 80)
        self.assert_framerate(clip, Fraction(24000, 1001))

        clip_no_dec = lvf.deinterlace.sivtc(self.BLACK_SAMPLE_CLIP_30p, decimate=False)
        self.assert_length(clip_no_dec, 200)
        self.assert_framerate(clip_no_dec, Fraction(60000, 1001))

    def test_seek_cycle(self) -> None:
        clip = lvf.deinterlace.seek_cycle(self.MEDIUM_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 1344, 776)

    # def test_tivtc_vfr(self) -> None:
    #     iclip = core.std.SetFieldBased(self.BLACK_SAMPLE_CLIP, 2)
    #     return ...

    #     with open(os.devnull, 'w') as devnull:
    #         with contextlib.redirect_stdout(devnull):
    #             clip = lvf.deinterlace.tivtc_vfr(iclip)

    #     self.assert_runs(clip)

    #     shutil.rmtree(Path('.ivtc'))

    def test_ivtc_credits(self) -> None:
        clip = lvf.deinterlace.ivtc_credits(self.BLACK_SAMPLE_CLIP_30p, frame_ref=0)
        self.assert_runs(clip)
        self.assert_length(clip, 80)
        self.assert_framerate(clip, Fraction(24000, 1001))


_not_implemented: List[str] = [
    'lvsfunc.dehardsub.hardsub_mask', 'lvf.deblock.autodb_dpir (write_props=True)', 'lvsfunc.deinterlace.tivtc_vfr',
    'lvsfunc.dehardsub.HardsubASS', 'lvsfunc.dehardsub.get_all_masks', 'lvsfunc.dehardsub.bounded_dehardsub',
    'lvsfunc.dehardsub.HardsubLine', 'lvsfunc.dehardsub.HardsubLineFade', 'lvsfunc.dehardsub.HardsubSignFade',
    'lvsfunc.dehardsub.HardsubMask', 'lvsfunc.dehardsub.HardsubSignKgf', 'lvsfunc.dehardsub.HardsubSign',
    'lvsfunc.denoise', 'lvsfunc.fun', 'lvsfunc.kernels', 'lvsfunc.mask', 'lvsfunc.misc', 'lvsfunc.progress',
    'lvsfunc.recon', 'lvsfunc.render', 'lvsfunc.scale', 'lvsfunc.types', 'lvsfunc.util'
]


if __name__ == '__main__':
    print("\nRunning lvsfunc unit tests..."
          "\n----------------------------------------------------------------------\n",
          "\nThe following functions have not been implemented yet:")

    for f in _not_implemented:
        print("    * ", f)

    print("\n")

    unittest.main(verbosity=2)
