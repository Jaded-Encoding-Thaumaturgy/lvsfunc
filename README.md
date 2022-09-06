# lvsfunc

<p align="center">
    <a href="https://lvsfunc.encode.moe"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/lvsfunc"></a>
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/lvsfunc">
    <a href="https://pypi.org/project/lvsfunc/"><img alt="PyPI" src="https://img.shields.io/pypi/v/lvsfunc"></a>
    <a href="https://github.com/Irrational-Encoding-Wizardry/lvsfunc/commits/master"><img alt="GitHub commits since tagged version" src="https://img.shields.io/github/commits-since/Irrational-Encoding-Wizardry/lvsfunc/latest"></a>
    <a href="https://github.com/Irrational-Encoding-Wizardry/lvsfunc/blob/master/LICENSE"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/lvsfunc"></a>
    <a href="https://discord.gg/qxTxVJGtst"><img alt="Discord" src="https://img.shields.io/discord/856381934052704266?label=discord"></a>
    <img alt="downloads" src="https://static.pepy.tech/personalized-badge/lvsfunc?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads">
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
$ pip3 install lvsfunc --no-cache-dir -U
```

Or if you want the latest git version, install it with this command:

```sh
$ pip3 install git+https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git --no-cache-dir -U
```

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
