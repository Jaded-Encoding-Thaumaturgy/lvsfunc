# lvsfunc

<p align="center">
    <img alt="Read the Docs" src="https://img.shields.io/readthedocs/lvsfunc">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/lvsfunc">
    <img alt="GitHub commits since tagged version" src="https://img.shields.io/github/commits-since/Irrational-Encoding-Wizardry/lvsfunc/latest">
    <img alt="PyPI - License" src="https://img.shields.io/pypi/l/lvsfunc">
    <img alt="Discord" src="https://img.shields.io/discord/856381934052704266?label=discord">
</p>

A collection of VapourSynth functions and wrappers
written and/or modified by LightArrowsEXE.
Full information on how every function/wrapper works,
as well as a list of dependencies and links,
can be found in the [documentation](https://lvsfunc.encode.moe/en/latest/).
For further support,
drop by `#lvsfunc` in the [IEW Discord server](https://discord.gg/qxTxVJGtst).

## How to install

If you have the old `lvsfunc.py` module,
remove that from your system first.

Install `lvsfunc` with the following command:

```sh
$ pip3 install lvsfunc --no-cache-dir --upgrade
```

Or if you want the latest git version, install it with this command:

```sh
$ python3 -m pip install --no-cache-dir --upgrade git+https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git -U
```

### Arch Linux

Install the [AUR package](https://aur.archlinux.org/packages/vapoursynth-plugin-lvsfunc-git/) `vapoursynth-plugin-lvsfunc-git` with your favorite AUR helper:

```sh
$ yay -S vapoursynth-plugin-lvsfunc-git
```

Note that this may be outdated.
It's recommended you grab the git version instead.

## Usage

After installation, functions can be loaded and used as follows:

```py
import lvsfunc as lvf

src = lvf.misc.source(...)
aa = lvf.aa.clamp_aa(...)
comp = lvf.comparison.compare(...)
...
```

## Disclaimer

Anything **MAY** change at any time.
The public API **SHOULD NOT** be considered stable.
If you use lvsfunc in any of your projects,
consider hardcoding a version requirement.
