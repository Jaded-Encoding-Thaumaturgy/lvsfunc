from __future__ import annotations

from functools import cache

from jetpytools import SPath
from vstools import PackageStorage

__all__ = ["get_lvsfunc_storage"]


class _LvsfuncSubStorage(PackageStorage):
    BASE_FOLDER = SPath(".vsjet/lvsfunc")


@cache
def get_lvsfunc_storage(
    subpkg: str | None = None,
) -> PackageStorage:
    if subpkg is None:
        return PackageStorage(package_name="lvsfunc")

    return _LvsfuncSubStorage(package_name=subpkg)
