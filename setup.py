#!/usr/bin/env python3

import setuptools

from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

with open("README.md", "r") as fh:
    long_description = fh.read()

name = "lvsfunc"
version = "0.0.1"
release = "0.0.1"

setuptools.setup(
    name=name,
    version=release,
    author="LightArrowsEXE",
    author_email="Lightarrowsreboot@gmail.com",
    description="Light's Vapoursynth Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Irrational-Encoding-Wizardry/lvsfunc",
    install_requires=[
        "vapoursynth",
        "vsutil"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    command_options={
        "build_sphinx": {
            "project": ("setup.py", name),
            "version": ("setup.py", version),
            "release": ("setup.py", release),
            "source_dir": ("setup.py", "docs")
        }
    }
)
