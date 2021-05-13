#!/usr/bin/env python3

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    install_requires = fh.read()

name = "lvsfunc"
version = "0.3.1"
release = "0.3.1"

setuptools.setup(
    name=name,
    version=release,
    author="LightArrowsEXE",
    author_email="Lightarrowsreboot@gmail.com",
    description="Light's Vapoursynth Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["lvsfunc"],
    url="https://github.com/Irrational-Encoding-Wizardry/lvsfunc",
    package_data={
        'lvsfunc': ['py.typed'],
    },
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    command_options={
        "build_sphinx": {
            "project": ("setup.py", name),
            "version": ("setup.py", version),
            "release": ("setup.py", release),
            "source_dir": ("setup.py", "docs")
        }
    }
)
