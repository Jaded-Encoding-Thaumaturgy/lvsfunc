from abc import ABC, abstractmethod

from vstools import (CustomValueError, FuncExceptT, PlanesT, core, get_prop, merge_clip_props,
                     normalize_planes, vs)

from .enum import VMAFFeature
from .types import CallbacksT

__all__: list[str] = [
    'PlaneAvgDiff',
    'VMAFDiff',
]


class DiffStrategy(ABC):
    """Base abstract class for diff strategies."""

    def __init__(
        self,
        threshold: float,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
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
    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """
        Process the difference between two clips.

        :param src:             The source clip to compare.
        :param ref:             The reference clip to compare.

        :return:                A tuple containing the processed clip and callbacks.
        """

        ...


class PlaneAvgDiff(DiffStrategy):
    """Strategy for comparing clips using PlaneAvg."""

    def __init__(
        self,
        threshold: float = 0.005,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the PlaneAvg strategy.

        Dependencies:

            - vapoursynth-zip (https://github.com/dnjulek/vapoursynth-zip)

        :param threshold:       The threshold to use for the comparison.
                                Higher will catch more differences.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self._check_vszip_version()

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using PlaneAvg."""

        self.threshold = max(0, min(1, self.threshold))

        ps_comp = src.vszip.PlaneAverage(
            [0], ref, planes=normalize_planes(src, self.planes), prop='fd_ps'
        )

        def _check_diff(f: vs.VideoFrame) -> bool:
            diff = get_prop(f, 'fd_psDiff', (list, float), default=0)

            if isinstance(diff, float):
                return diff >= self.threshold

            return any(float(x) >= self.threshold for x in diff)

        callbacks = CallbacksT([_check_diff])

        return ps_comp.std.SetFrameProps(fd_thr=self.threshold), callbacks

    def _check_vszip_version(self) -> None:
        if hasattr(core, 'vszip'):
            return

        raise CustomValueError(
            'vszip is not available! Please install it at "https://github.com/dnjulek/vapoursynth-zip"!',
            self._func_except
        )


class VMAFDiff(DiffStrategy):
    """Strategy for comparing clips using VMAF."""

    def __init__(
        self,
        threshold: float = 0.999,
        feature: VMAFFeature | list[VMAFFeature] = VMAFFeature.SSIM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
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

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using VMAF."""

        self.threshold = max(0, min(1, self.threshold))

        features = [
            f for feature in self.feature
            for f in ([f for f in VMAFFeature if f.value >= 0]
                      if feature == VMAFFeature.ALL else [feature])
        ]

        if not features:
            raise CustomValueError("You must specify at least one VMAF feature!", self.process, self.feature)

        vmaf_clips = [core.vmaf.Metric(src, ref, feature=feature) for feature in features]
        vmaf_clip = merge_clip_props(*vmaf_clips)

        callbacks = CallbacksT(
            [lambda f: get_prop(f, feature.prop, (float, int), default=100)
             <= self.threshold for feature in features]
        )

        return vmaf_clip.std.SetFrameProps(fd_thr=self.threshold), callbacks
