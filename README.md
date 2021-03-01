# lvsfunc

A collection of VapourSynth functions and wrappers
written and/or "borrowed" by LightArrowsEXE.
Full information on how every function/wrapper works,
as well as specific dependencies
can be found in the [documentation](https://lvsfunc.readthedocs.io/).

## How to install

If you have the old `lvsfunc.py` module,
remove that from your system first.

Install `lvsfunc` with the following command:
```sh
$ pip install lvsfunc
```

### Arch Linux

Install the [AUR package](https://aur.archlinux.org/packages/vapoursynth-plugin-lvsfunc-git/) `vapoursynth-plugin-lvsfunc-git` with your favorite AUR helper:

```sh
$ yay -S vapoursynth-plugin-lvsfunc-git
```

## Usage

After installation, functions can be loaded and used as follows:

```py
import lvsfunc as lvf

src = lvf.misc.source(...)
aa = lvf.aa.nneedi3_clamp(...)
comp = lvf.comparison.compare(...)
...
```

## Requirements

- Python 3.8 or newer
- Vapoursynth R49 or newer
