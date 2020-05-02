lvsfunc, a collection of VapourSynth functions and wrappers
written and/or "borrowed" by LightArrowsEXE.<br>
Full information on how every function/wrapper works,
as well as specific dependencies
can be found in the [documentation](https://lvsfunc.readthedocs.io/).

## How to install

If you have the old `lvsfunc.py` module,
remove that from your system first.<br>
You can then install `lvsfunc`
with `python3 setup.py install`.

Functions can be loaded and used as follows:
```py
import lvsfunc as lvf

src = lvf.misc.source()
aa = lvf.aa.nneedi3_clamp()
comp = lvf.comparison.compare()
...
```

## Requirements:

- Python 3.8 or newer
- Vapoursynth R49 or newer
