from .itertoolz import *
from .functoolz import *
from .dicttoolz import *
from .recipes import *
from . import curried as curried
from ._version import __toolz_version__ as __toolz_version__
from .compatibility import filter as filter, map as map
from functools import partial as partial, reduce as reduce
from typing import Any

sorted = sorted
comp = compose
flip: Any
memoize: Any
