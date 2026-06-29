from __future__ import annotations

import pytest
from vsscale.onnx import Backend
from vstools import core, vs

from lvsfunc.models.base import _LvsfuncRgbModel
from lvsfunc.models.delowpass import LHzDelowpass
from lvsfunc.models.dempeg2 import LDempeg2

CPU_BACKEND = Backend.ORT_CPU

CONCRETE_MODELS: tuple[type[_LvsfuncRgbModel], ...] = (
    LDempeg2,
    LHzDelowpass.DoubleTaps_4_4_15_15,
    LHzDelowpass.DoubleTaps_4_4_15_15_mpeg2,
    LHzDelowpass.DoubleTaps_4_4_125_1375_mpeg2,
)


def has_mlrt_inference() -> bool:
    return hasattr(core, "ort") or hasattr(core, "ncnn")


requires_inference = pytest.mark.skipif(
    not has_mlrt_inference(),
    reason="vs-mlrt inference plugins (ort/ncnn) are not installed",
)


@pytest.fixture
def small_yuv_clip() -> vs.VideoNode:
    return core.std.BlankClip(format=vs.YUV420P16, width=64, height=64, length=1)


@pytest.fixture(params=CONCRETE_MODELS)
def concrete_model_cls(request: pytest.FixtureRequest) -> type[_LvsfuncRgbModel]:
    return request.param
