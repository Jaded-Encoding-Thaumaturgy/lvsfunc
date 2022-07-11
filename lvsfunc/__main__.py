import subprocess
import sys
import os
from typing import List

import pkg_resources


class InstallationException(Exception):
    """Throw when some kind of exception occurs during installation."""

    ...


pkg = 'lvsfunc'

vsrepo_deps: List[str] = [
    'akarin',
    'BM3D',
    'Descale',
    'EEDI3 (obsolete)',
    'fillborders',
    'fmtconv',
    'havsfunc',
    'kagefunc',
    'lsmas',
    'NNEDI3CL',
    'RemapFrames',
    'rgsf',
    'Scxvid',
    'TDeintMod',
    'TIVTC',
    'vs-placebo',
    'ZNEDI3',
]

pypi_deps: List[str] = [
]


def prompt_user() -> bool:
    """Prompt user to install/update dependencies."""
    prompt = input(f"Install/update {pkg} dependencies? [y/n]: ").lower().strip()

    match prompt:
        case 'y' | 'yes': return True
        case _: return False


def main() -> None:
    """Prompt user to install/update dependencies."""
    if not prompt_user():
        exit()

    pkg_version = pkg_resources.get_distribution(pkg).version
    pkg_ghrepo = "https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git"

    update_reqs = [sys.executable, '-m', 'pip', 'install', '-U']
    update_reqs.append(f"git+{pkg_ghrepo}@v{pkg_version}")

    vsrepo = ['vsrepo', 'install']
    vsrepo.extend(vsrepo_deps)
    vsrepo.extend(['--stub-output-file', '@'])

    try:
        subprocess.run(update_reqs, cwd=os.getcwd())

        if vsrepo_deps:
            subprocess.run(['vsrepo', 'update'])
            subprocess.run(vsrepo)
    except subprocess.CalledProcessError as e:
        raise InstallationException(e.output)


if __name__ == '__main__':
    main()
