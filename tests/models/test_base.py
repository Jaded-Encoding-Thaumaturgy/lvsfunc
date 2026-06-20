from __future__ import annotations

import pytest
from jetpytools import CustomNotImplementedError

from lvsfunc.models.base import _get_onnx_model, _LvsfuncRgbModel, _model_variants
from lvsfunc.models.delowpass import LHzDelowpass
from lvsfunc.models.dempeg2 import LDempeg2

from .conftest import CONCRETE_MODELS


def test_lhzdelowpass_is_namespace() -> None:
    with pytest.raises(CustomNotImplementedError, match="is a namespace") as exc:
        LHzDelowpass()

    message = str(exc.value)
    assert "DoubleTaps_4_4_15_15" in message
    assert "Available variants:" in message


def test_model_variants_lists_nested_classes() -> None:
    assert "DoubleTaps_4_4_125_1375_mpeg2" in _model_variants(LHzDelowpass)


@pytest.mark.parametrize("model_cls", CONCRETE_MODELS)
def test_onnx_shader_exists(model_cls: type[_LvsfuncRgbModel]) -> None:
    model = object.__new__(model_cls)

    path = _get_onnx_model(model)

    assert path.is_file()


@pytest.mark.parametrize(
    ("model_cls", "expected_dir"),
    [
        (LDempeg2, "ldempeg2"),
        (LHzDelowpass.DoubleTaps_4_4_15_15, "lhzdelowpass"),
    ],
)
def test_model_dir(model_cls: type, expected_dir: str) -> None:
    assert model_cls(backend=None)._model_dir == expected_dir
