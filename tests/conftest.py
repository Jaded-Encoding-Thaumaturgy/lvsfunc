from __future__ import annotations

import pytest
from jetpytools import SPath


@pytest.fixture
def tmp_path(
    request: pytest.FixtureRequest,
    tmp_path_factory: pytest.TempPathFactory,
) -> SPath:
    return SPath(tmp_path_factory.mktemp(request.node.name, numbered=True))
