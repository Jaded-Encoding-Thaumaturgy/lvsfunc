lvsfunc, a collection of VapourSynth functions and wrappers written and/or "borrowed" by LightArrowsEXE.
Full information on how every function/wrapper works can be found in the docstrings.

## How to install

Create a directory in your Python installation's `site-packages` called `lvsfunc` and dump all the Python files in there.
You can then import lvsfunc and use its function as you would any other *func.

```py
import lvsfunc as lvf

src = lvf.source()
aa = lvf.nneedi3_clamp()
comp = lvf.compare()
...
```

## Requirements:

- Vapoursynth R28 or newer
- Python 3.6 or newer

## Dependencies:

- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)
- [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [kagefunc](https://github.com/Irrational-Encoding-Wizardry/kagefunc)
- [mvsfunc](https://github.com/HomeOfVapourSynthEvolution/mvsfunc)
- [nnedi3_rpow2](https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py)
- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [vsutil](https://github.com/Irrational-Encoding-Wizardry/vsutil)
- [combmask](https://mega.nz/#!whtkTShS!JsDhi-_QGs-kZkzWqgcXHX2MQII4Bl9Y4Ft0zHnXDvk)
- [descale](https://github.com/Irrational-Encoding-Wizardry/vapoursynth-descale) (Specifically the library)

### Optional dependencies:
- waifu2x-caffe
- L-SMASH Source
- d2vsource
- FFMS2

These can all be found at <http://www.vapoursynth.com/doc/pluginlist.html>
<br>
<br>
**For more information on how to use every funtion, please refer to the docstrings.<br>
If you run into any issues, feel free to leave a PR or otherwise contact me on Discord (LightArrowsEXE#0476)**
