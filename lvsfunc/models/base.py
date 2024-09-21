from warnings import warn
import importlib.resources as pkg_resources

from stgpytools import FileWasNotFoundError, SPath

__all__: list[str] = []


def _get_pkg_path() -> SPath:
    """Get the path of the package."""

    import lvsfunc

    return SPath(pkg_resources.files(lvsfunc)) / 'models' / 'shaders'


def _get_model_path(sub_dir: str, model_name: str, fp16: bool = True) -> SPath:
    """Get the path of the model."""

    if model_name not in _model_paths:
        raise FileWasNotFoundError(f"Model {model_name} not found!", _get_model_path)

    model_path = _get_pkg_path() / str(sub_dir) / _model_paths[model_name]

    if not fp16:
        return model_path

    new_path = model_path.with_name(model_path.stem.split('_fp32')[0] + '_fp16.onnx')

    if new_path.exists():
        return new_path

    warn(f'{model_name}: Could not find fp16 model! Returning fp32 model instead.')

    return model_path


# Paths to every model. Should always end with _fp32.onnx, we swap it out later if necessary.
_model_paths: dict[str, SPath] = {
    # Delowpassing models
    'LHzDelowpass.DoubleTaps_4_4_15_15': '1x_lanczos_hz_delowpass_4_4_15_15_fp32.onnx',
}
