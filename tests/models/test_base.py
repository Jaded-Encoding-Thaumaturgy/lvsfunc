from __future__ import annotations

from typing import Any

import pytest
from jetpytools import CustomNotImplementedError, FileWasNotFoundError
from vstools import core, vs

from lvsfunc.models.base import _get_onnx_model, _LvsfuncRgbModel, _model_variants
from lvsfunc.models.delowpass import LHzDelowpass
from lvsfunc.models.dempeg2 import LDempeg2

from .conftest import CONCRETE_MODELS


class _ModelWithoutShader(_LvsfuncRgbModel):
    _model = "definitely_missing_shader"


class _EmptyModelNamespace(_LvsfuncRgbModel):
    pass


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


def test_model_path_argument_is_ignored() -> None:
    with pytest.warns(UserWarning, match="bundled ONNX weights"):
        LDempeg2(model="/tmp/custom.onnx", backend=None)


def test_get_onnx_model_requires_model_filename() -> None:
    model = object.__new__(_EmptyModelNamespace)

    with pytest.raises(FileWasNotFoundError, match="does not define a _model filename"):
        _get_onnx_model(model)


def test_get_onnx_model_requires_shader_file_on_disk() -> None:
    with pytest.raises(FileWasNotFoundError, match="was not found"):
        _ModelWithoutShader(backend=None)


def test_rgb_model_without_variants_reports_generic_message() -> None:
    with pytest.raises(CustomNotImplementedError, match="no model variants defined"):
        _EmptyModelNamespace()


def test_apply_is_deprecated_and_wraps_scale(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model = LDempeg2(backend=None)
    clip = core.std.BlankClip(width=64, height=64, format=vs.YUV420P16, length=1)
    scaled = core.std.BlankClip(width=64, height=64, format=vs.YUV420P16, length=1)
    called: list[vs.VideoNode] = []

    def fake_scale(node: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        called.append(node)
        return scaled

    monkeypatch.setattr(model, "scale", fake_scale)

    with pytest.deprecated_call():
        result = model.apply(clip)

    assert called
    assert (result.width, result.height) == (clip.width, clip.height)
    assert result.format.id == clip.format.id
