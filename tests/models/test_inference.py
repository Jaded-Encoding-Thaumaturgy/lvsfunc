from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from vstools import depth, vs

from .conftest import CONCRETE_MODELS, CPU_BACKEND, requires_inference

if TYPE_CHECKING:
    from lvsfunc.models.base import _LvsfuncRgbModel


@requires_inference
@pytest.mark.parametrize("model_cls", CONCRETE_MODELS)
def test_model_scale_preserves_geometry(
    model_cls: type[_LvsfuncRgbModel],
    small_yuv_clip: vs.VideoNode,
) -> None:
    model = model_cls(backend=CPU_BACKEND)
    out = model.scale(depth(small_yuv_clip, 32))

    assert out.width == small_yuv_clip.width
    assert out.height == small_yuv_clip.height
    assert out.num_frames == small_yuv_clip.num_frames
