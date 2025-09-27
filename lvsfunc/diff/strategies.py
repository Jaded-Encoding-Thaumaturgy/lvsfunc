from abc import ABC, abstractmethod
from typing import Iterable

from vskernels import Catrom
from vstools import (
    CustomValueError,
    DependencyNotFoundError,
    FuncExceptT,
    LengthRefClipMismatchError,
    Matrix,
    PlanesT,
    VSFunction,
    core,
    depth,
    get_prop,
    merge_clip_props,
    normalize_planes,
    vs,
)

from .enum import ButteraugliNorm, VMAFFeature
from .exceptions import NoGpuError, VMAFError
from .types import CallbacksT

__all__: list[str] = [
    "PlaneStatsDiff",
    "PlaneAvgFloatDiff",
    "VMAFDiff",
    "ButteraugliDiff",
]


class DiffStrategy(ABC):
    """Base abstract class for diff strategies."""

    def __init__(
        self,
        threshold: float,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Initialize the diff strategy.

        :param threshold:       The threshold to use for the comparison.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        self.threshold = threshold
        self.planes = planes
        self._func_except = func_except or self.__class__.__name__

    @abstractmethod
    def process(
        self, src: vs.VideoNode, ref: vs.VideoNode
    ) -> tuple[vs.VideoNode, CallbacksT]:
        """
        Process the difference between two clips.

        :param src:             The source clip to compare.
        :param ref:             The reference clip to compare.

        :return:                A tuple containing the processed clip and callbacks.
        """

        ...


class _vszipStrategy:
    """Base class for vszip strategies."""

    def __post_init__(self) -> None:
        if hasattr(core, "vszip"):
            return

        if not hasattr(self, "_func_except"):
            self._func_except = self.__class__.__name__

        raise DependencyNotFoundError(
            self._func_except,
            "vszip <https://github.com/dnjulek/vapoursynth-zip>",
        )


class PlaneStatsDiff(DiffStrategy, _vszipStrategy):
    """Strategy for comparing clips using PlaneStats."""

    def __init__(
        self,
        threshold: int = 96,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Initialize the PlaneStats strategy.

        Dependencies:

            - vapoursynth-zip (https://github.com/dnjulek/vapoursynth-zip)

        :param threshold:       The threshold to use for the comparison.
                                Must be between -128 and 128.
                                Higher values will catch more differences.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        if not -128 <= threshold <= 128:
            raise CustomValueError(
                "Threshold must be between -128 and 128!",
                self.__init__,
                threshold,
            )

        super().__init__(threshold, planes, func_except)

    def process(
        self, src: vs.VideoNode, ref: vs.VideoNode
    ) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using the old find_diff logic."""

        src = depth(src, 8)
        ref = depth(ref, 8)

        diff_clip = (
            src.std.MakeDiff(ref, planes=self.planes)
            .vszip.PlaneMinMax(prop="fs_ps")
            .std.PlaneStats(prop="fs_ps")
        )

        def _check_diff(f: vs.VideoFrame) -> bool:
            diff_min = get_prop(f, "fs_psMin", (float, int), default=0.0)
            diff_max = get_prop(f, "fs_psMax", (float, int), default=0.0)

            return diff_min <= self.threshold or diff_max >= (255 - self.threshold)

        callbacks = [_check_diff]

        return diff_clip, CallbacksT(callbacks)


class PlaneAvgFloatDiff(DiffStrategy, _vszipStrategy):
    """Strategy for comparing clips using PlaneAvg."""

    def __init__(
        self,
        threshold: float = 0.003,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Initialize the PlaneAvg (float) strategy.

        Dependencies:

            - vapoursynth-zip (https://github.com/dnjulek/vapoursynth-zip)

        :param threshold:       The threshold to use for the comparison.
                                Must be between 0 and 1.
                                Lower values will catch more differences.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        if not 0 <= threshold <= 1:
            raise CustomValueError(
                "Threshold must be between 0 and 1!",
                self.__init__,
                threshold,
            )

        super().__init__(threshold, planes, func_except)

    def process(
        self, src: vs.VideoNode, ref: vs.VideoNode
    ) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using PlaneAvg."""

        self.threshold = max(0, min(1, self.threshold))

        src = depth(src, 32)
        ref = depth(ref, 32)

        try:
            ps_comp = src.vszip.PlaneAverage(
                [0], ref, planes=normalize_planes(src, self.planes), prop="fd_psf"
            )
        except vs.Error as e:
            if "less frames than" in str(e):
                raise LengthRefClipMismatchError(self.process, src, ref)

            raise

        def _check_diff(f: vs.VideoFrame) -> bool:
            diff = get_prop(f, "fd_psfDiff", (list, float), default=0.0)

            if isinstance(diff, Iterable):
                return any(float(x) >= self.threshold for x in diff)

            return diff >= self.threshold

        callbacks = CallbacksT([_check_diff])

        return ps_comp.std.SetFrameProps(fd_thr=self.threshold), callbacks


class VMAFDiff(DiffStrategy):
    """Strategy for comparing clips using VMAF."""

    def __post_init__(self) -> None:
        """
        Check if VMAF is installed.

        :raise DependencyNotFoundError: If VMAF is not installed.
        """

        if hasattr(core, "vmaf"):
            return

        raise DependencyNotFoundError(
            self._func_except,
            "vmaf <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF>",
        )

    def __init__(
        self,
        threshold: float = 0.999,
        feature: VMAFFeature | list[VMAFFeature] = VMAFFeature.SSIM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Initialize the VMAF strategy.

        Dependencies:

            - VapourSynth-VMAF (https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF)

        :param threshold:       The threshold to use for the comparison.
                                Lower will catch more differences.
        :param feature:         The VMAF feature(s) to use for comparison.
                                See :py:class:`lvsfunc.diff.enum.VMAFFeature` for more information.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self.feature = [feature] if isinstance(feature, VMAFFeature) else feature

    def process(
        self, src: vs.VideoNode, ref: vs.VideoNode
    ) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using VMAF."""

        self.threshold = max(0, min(1, self.threshold))

        features = [
            f
            for feature in self.feature
            for f in (
                [f for f in VMAFFeature if f.value >= 0]
                if feature == VMAFFeature.ALL
                else [feature]
            )
        ]

        if not features:
            raise VMAFError(
                "You must specify at least one VMAF feature!",
                self._func_except,
                self.feature,
            )

        vmaf_clips = [
            core.vmaf.Metric(src, ref, feature=feature) for feature in features
        ]
        vmaf_clip = merge_clip_props(*vmaf_clips)

        callbacks = CallbacksT(
            [
                lambda f: get_prop(f, feature.prop, (float, int), default=100)
                <= self.threshold
                for feature in features
            ]
        )

        return vmaf_clip.std.SetFrameProps(fd_thr=self.threshold), callbacks


class ButteraugliDiff(DiffStrategy):
    """Strategy for comparing clips using Butteraugli."""

    def __init__(
        self,
        threshold: float = 2.0,
        intensity_multiplier: float = 80.0,
        norm_mode: ButteraugliNorm | list[ButteraugliNorm] = ButteraugliNorm.TWO_NORM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Initialize the Butteraugli strategy.

        Dependencies:
            - vship (https://github.com/Line-fr/Vship) (GPU)
            - vapoursynth-julek-plugin (https://github.com/dnjulek/vapoursynth-julek-plugin) (CPU)

        :param threshold:               The threshold to use for the comparison.
                                        Lower will catch more differences.
        :param intensity_multiplier:    Controls sensitivity of the Butteraugli metric.
                                        Higher values make it more sensitive to differences.
        :param norm_mode:               Which norm to use for the comparison.
                                        See :py:class:`lvsfunc.diff.enum.ButteraugliNorm` for more information.
        :param planes:                  The planes to compare.
        :param func_except:             The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self.intensity_multiplier = intensity_multiplier
        self.norm_mode = norm_mode

        if not isinstance(self.norm_mode, list):
            self.norm_mode = [self.norm_mode]

    def process(
        self, src: vs.VideoNode, ref: vs.VideoNode
    ) -> tuple[vs.VideoNode, CallbacksT]:
        """
        Process the difference between two clips using Butteraugli.

        :raise NoGpuError:              If no GPU is detected.
        :raise VMAFError:               If there's an issue with VMAF.
        """

        plugin, intensity_param = self._get_plugin()

        src_matrix = Matrix.from_video(src)

        # We have to resample to RGB ourselves because the plugin doesn't do it
        if intensity_param == "intensity_target":
            src, ref = self._to_rgb(src), self._to_rgb(ref)
            self.norm_mode = [ButteraugliNorm.JULEK]
        else:
            self.norm_mode = [x for x in self.norm_mode if x != ButteraugliNorm.JULEK]  # type: ignore

            if not self.norm_mode:
                self.norm_mode = [ButteraugliNorm.TWO_NORM]

        ba_clip = plugin(src, ref, **{intensity_param: self.intensity_multiplier})  # type: ignore
        props = [norm.prop for norm in self.norm_mode]

        callbacks = CallbacksT(
            [
                lambda f: any(
                    get_prop(f, prop, (float, int), default=0) >= self.threshold
                    for prop in props
                )
            ]
        )

        # Get the matrix from source back to prevent it from being set to RGB in the return clip
        return src_matrix.apply(ba_clip).std.SetFrameProps(
            fd_thr=self.threshold
        ), callbacks

    def _get_plugin(self) -> tuple[VSFunction, str]:
        if hasattr(core, "vship"):
            try:
                core.vship.GpuInfo()
                return core.vship.BUTTERAUGLI, "intensity_multiplier"  # type: ignore
            except vs.Error as e:
                if "Device" in str(e):
                    if hasattr(core, "julek"):
                        return core.julek.Butteraugli, "intensity_target"  # type: ignore

                    raise NoGpuError("No GPU detected!", self._get_plugin)

        if hasattr(core, "julek"):
            return core.julek.Butteraugli, "intensity_target"  # type: ignore

        raise DependencyNotFoundError(
            self._func_except,
            "vship <https://github.com/Line-fr/Vship> (GPU) or "
            "vapoursynth-julek-plugin <https://github.com/dnjulek/vapoursynth-julek-plugin> (CPU)",
        )

    def _to_rgb(self, clip: vs.VideoNode) -> vs.VideoNode:
        return Catrom().resample(
            clip, vs.RGBS, matrix_in=Matrix.from_param_or_video(1, clip)
        )
