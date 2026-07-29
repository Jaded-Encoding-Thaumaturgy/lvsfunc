from __future__ import annotations

from vstools import PackageStorage

from lvsfunc._package import _LvsfuncSubStorage, get_lvsfunc_storage
from lvsfunc.models.base import _get_onnx_model
from lvsfunc.models.dempeg2 import LDempeg2


def test_get_lvsfunc_storage_default_is_package_storage() -> None:
    storage = get_lvsfunc_storage()

    assert isinstance(storage, PackageStorage)
    assert not isinstance(storage, _LvsfuncSubStorage)
    assert storage.folder.name == "lvsfunc"


def test_get_lvsfunc_storage_subpkg_uses_vsjet_base_folder() -> None:
    storage = get_lvsfunc_storage("keyframes")

    assert isinstance(storage, _LvsfuncSubStorage)
    assert storage.folder.name == "keyframes"
    assert storage.folder.parent.name == "lvsfunc"
    assert ".vsjet" in storage.folder.parts


def test_get_lvsfunc_storage_is_cached() -> None:
    assert get_lvsfunc_storage() is get_lvsfunc_storage()
    assert get_lvsfunc_storage("models") is get_lvsfunc_storage("models")
    assert get_lvsfunc_storage() is not get_lvsfunc_storage("models")


def test_get_onnx_model_resolves_under_lvsfunc_package() -> None:
    model = object.__new__(LDempeg2)
    path = _get_onnx_model(model)

    assert path.is_file()
    assert path.suffix == ".onnx"
    assert path.parts[-4:] == ("models", "shaders", "ldempeg2", path.name)
    assert "lvsfunc" in path.parts
