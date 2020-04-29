lvsfunc, a collection of VapourSynth functions and wrappers written and/or
"borrowed" by LightArrowsEXE. Full information on how every function/wrapper
works and specific dependencies can be found in the documentation.

## How to install

Install with `python3 setup.py install`


```py
import lvsfunc as lvf

src = lvf.misc.source()
aa = lvf.aa.nneedi3_clamp()
comp = lvf.comparison.compare()
...
```

## Requirements:

- Vapoursynth R48 or newer
- Python 3.6 or newer
