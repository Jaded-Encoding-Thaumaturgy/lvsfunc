# lvsfunc

<p align="center">
    <!-- <a href="https://lvsfunc.encode.moe"><img alt="Read the Docs" src="https://img.shields.io/readthedocs/lvsfunc"></a> -->
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/lvsfunc">
    <a href="https://pypi.org/project/lvsfunc/"><img alt="PyPI" src="https://img.shields.io/pypi/v/lvsfunc"></a>
    <a href="https://github.com/Irrational-Encoding-Wizardry/lvsfunc/commits/master"><img alt="GitHub commits since tagged version" src="https://img.shields.io/github/commits-since/Irrational-Encoding-Wizardry/lvsfunc/latest"></a>
    <a href="https://github.com/Irrational-Encoding-Wizardry/lvsfunc/blob/master/LICENSE"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/lvsfunc"></a>
    <a href="https://discord.gg/XTpc6Fa9eB"><img alt="Discord" src="https://img.shields.io/discord/856381934052704266?label=discord"></a>
    <img alt="downloads" src="https://static.pepy.tech/personalized-badge/lvsfunc?period=total&units=international_system&left_color=grey&right_color=blue&left_text=downloads">
</p>

> [!CAUTION]
>Anything **MAY** change at any time.
>The public API **SHOULD NOT** be considered stable.
>
>Many functions in this package are considered **EXPERIMENTAL** and **UNOPTIMAL** for regular filterchains,
>are likely to require either extensive testing,
>or may be moved to a different [_Jaded Encoding Thaumaturgy_](https://github.com/Jaded-Encoding-Thaumaturgy) package at any point.
>
>If you use `lvsfunc` in any of your projects,
>please consider hardcoding a version requirement!

If you're testing new functionality
that may be ported over
to a JET package
in the future,
please make sure to install
the latest version on git.

----

A collection of VapourSynth functions and wrappers
written and/or modified by LightArrowsEXE.
Full information on how every function/wrapper works,
as well as a list of dependencies and links,
can be found in the docstrings of each function/wrapper.
For further support,
drop by `#dev` in the [JET Discord server](https://discord.gg/XTpc6Fa9eB).

## How to install

`lvsfunc` is distributed via PyPi. You can install it with the following command:

```shell
pip install lvsfunc
```

You can install the git latest version with the following command:

```shell
pip install git+https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc.git
```

## Usage

After installation, functions can be loaded and used as follows:

```py
import lvsfunc as lvf

aa = lvf.deblock.autodb_dpir(...)
comp = lvf.comparison.compare(...)
...
```
