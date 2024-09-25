#!/usr/bin/env python3

from pathlib import Path

import setuptools  # type:ignore[import-untyped]

long_description = Path("README.md").read_text(encoding='utf-8')
install_requires = Path("requirements.txt").read_text(encoding='utf-8')

package_name = "lvsfunc"

exec(Path(f'{package_name}/_metadata.py').read_text(encoding='utf-8'), meta := dict[str, str]())

setuptools.setup(
    name=package_name,
    version=meta['__version__'],
    author=meta['__author_name__'],
    author_email=meta['__author_email__'],
    maintainer=meta['__maintainer_name__'],
    maintainer_email=meta['__maintainer_email__'],
    description=meta['__doc__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        package_name,
        f"{package_name}.dependency",
        f"{package_name}.hdcam",
        f"{package_name}.models",
        f"{package_name}.nn",
    ],
    package_data={
        package_name: ['py.typed', 'models/shaders/*/*.onnx'],
    },
    install_requires=install_requires,
    project_urls={
        "Source Code": 'https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc',
        "Contact": 'https://discord.gg/XTpc6Fa9eB',
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
    python_requires='>=3.12',
)
