#!/usr/bin/env python3

import setuptools

with open("README.md") as fh:
    long_description = fh.read()

with open("requirements.txt") as fh:
    install_requires = fh.read()

name = "lvsfunc"
version = "0.4.2"
release = "0.4.2"

setuptools.setup(
    name=name,
    version=release,
    author="LightArrowsEXE",
    author_email="lightarrowsreboot@gmail.com",
    description="Light's Vapoursynth Functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["lvsfunc"],
    package_data={
        'lvsfunc': ['py.typed'],
    },
    install_requires=install_requires,
    project_urls={
        "Source Code": 'https://github.com/Irrational-Encoding-Wizardry/lvsfunc',
        "Documentation": 'https://lvsfunc.encode.moe/en/latest/',
        "Contact": 'https://discord.gg/qxTxVJGtst',
    },
    classifiers=[
        "Natural Language :: English",

        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",

        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",

        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Display",
    ],
    python_requires='>=3.10',
    command_options={
        "build_sphinx": {
            "project": ("setup.py", name),
            "version": ("setup.py", version),
            "release": ("setup.py", release),
            "source_dir": ("setup.py", "docs")
        }
    }
)
