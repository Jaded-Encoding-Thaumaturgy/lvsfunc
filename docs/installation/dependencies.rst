Dependencies
------------

lvsfunc depends on the following third-party scripts:

* `havsfunc <https://github.com/HomeOfVapourSynthEvolution/havsfunc>`_
* `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_
* `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_
* `vsutil <https://pypi.org/project/vsutil/>`_

The following VapourSynth libraries are also required for full functionality:

* `akarinVS <https://github.com/AkarinVS/vapoursynth-plugin>`_
* `combmask <https://drive.google.com/file/d/15E0Ua27AndT-0zSHHCC1iL5SZO09Ntbv/view?usp=sharing>`_
* `dgdecode <https://www.rationalqm.us/dgmpgdec/dgmpgdec.html>`_
* `dgdecodenv <https://www.rationalqm.us/dgdecnv/binaries/>`_
* `fmtconv <https://github.com/EleonoreMizo/fmtconv>`_
* `L-SMASH-Works <https://github.com/AkarinVS/L-SMASH-Works>`_
* `RGSF <https://github.com/IFeelBloated/RGSF>`_
* `TIVTC <https://github.com/dubhater/vapoursynth-tivtc>`_
* `VapourSynth-Bilateral <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Bilateral>`_
* `VapourSynth-BM3D <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-BM3D>`_
* `VapourSynth-descale <https://github.com/Irrational-Encoding-Wizardry/VapourSynth-descale>`_
* `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
* `VapourSynth-fillborders <https://github.com/dubhater/vapoursynth-fillborders>`_
* `VapourSynth-nnedi3 <https://github.com/dubhater/VapourSynth-nnedi3>`_
* `VapourSynth-NNEDI3CL <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-NNEDI3CL>`_
* `VapourSynth-RemapFrames <https://github.com/Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames>`_
* `vapoursynth-scxvid <https://github.com/dubhater/vapoursynth-scxvid>`_
* `VapourSynth-TDeintMod <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-TDeintMod>`_
* `vapoursynth-wwxd <https://github.com/dubhater/vapoursynth-wwxd>`_
* `vs-ContinuityFixer <https://github.com/MonoS/VS-ContinuityFixer>`_
* `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_
* `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_
* `vs-placebo <https://github.com/Lypheo/vs-placebo>`_
* `znedi3 <https://github.com/sekrit-twc/znedi3>`_

This list is non-exhaustive, as dependencies may have their own dependencies.
An attempt has been made to document major dependencies on a per-function basis.
Unfortunately, \*func family modules have complex dependency graphs and documenting
them is beyond the scope of this module.

You can install most of these dependencies by running ``lvsfunc`` directly:

.. code-block:: console

    python -m lvsfunc
        Install/update lvsfunc dependencies? [y/n]:

| Note that this does _not_ install every single dependency!
| Just the ones that are easy to obtain through package managers!
