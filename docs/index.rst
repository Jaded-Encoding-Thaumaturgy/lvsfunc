lvsfunc documentation
---------------------

.. toctree::
   :maxdepth: 4
   :caption: Contents:

About
---------------

.. automodule:: lvsfunc
   :members:
   :undoc-members:
   :show-inheritance:


Dependencies
----------------

lvsfunc depends on the following third-party scripts:

* `debandshit <https://github.com/LightArrowsEXE/debandshit>`_
* `edi_rpow2 <https://gist.github.com/YamashitaRen/020c497524e794779d9c>`_
* `havsfunc <https://github.com/HomeOfVapourSynthEvolution/havsfunc>`_
* `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_
* `mvsfunc <https://github.com/HomeOfVapourSynthEvolution/mvsfunc>`_
* `vsTAAmbk <https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk>`_
* `vsutil <https://github.com/Irrational-Encoding-Wizardry/vsutil>`_

The following Vapoursynth libraries are also required for full functionality:

* `adaptivegrain <https://git.kageru.moe/kageru/adaptivegrain>`_
* `combmask <https://mega.nz/#!whtkTShS!JsDhi-_QGs-kZkzWqgcXHX2MQII4Bl9Y4Ft0zHnXDvk>`_
* `d2vsource <https://github.com/dwbuiten/d2vsource>`_
* `dgdecnv <http://rationalqm.us/dgdecnv/dgdecnv.html>`_
* `fmtconv <https://github.com/EleonoreMizo/fmtconv>`_
* `knlmeanscl <https://github.com/Khanattila/KNLMeansCL>`_
* `rgsf <https://github.com/IFeelBloated/RGSF>`_
* `vapoursynth-descale <https://github.com/Irrational-Encoding-Wizardry/vapoursynth-descale>`_
* `vapoursynth-nnedi3 <https://github.com/dubhater/vapoursynth-nnedi3>`_
* `vapoursynth-eedi3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
* `vapoursynth-readmpls <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-ReadMpls>`_
* `vapoursynth-retinex <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Retinex>`_
* `vapoursynth-tcanny <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-TCanny>`_
* `vs-continuityfixer <https://github.com/MonoS/VS-ContinuityFixer>`_
* `zimg <https://github.com/sekrit-twc/zimg>`_
* `znedi3 <https://github.com/sekrit-twc/znedi3>`_

This list is non-exhaustive, as dependencies may have their own dependencies.
An attempt has been made to document major dependencies on a per-function basis.
Unfortunately, \*func family modules have complex dependency graphs and documenting
them is beyond the scope of this module.

Modules
-------

.. autosummary::

   lvsfunc.aa
   lvsfunc.comparison
   lvsfunc.deinterlace
   lvsfunc.denoise
   lvsfunc.kernels
   lvsfunc.misc
   lvsfunc.scale
   lvsfunc.util

Functions
---------

.. autosummary::

   lvsfunc.aa.nneedi3_clamp
   lvsfunc.aa.transpose_aa
   lvsfunc.aa.upscaled_sraa
   lvsfunc.comparison.compare
   lvsfunc.comparison.stack_compare
   lvsfunc.comparison.stack_planes
   lvsfunc.comparison.tvbd_diff
   lvsfunc.deinterlace.deblend
   lvsfunc.deinterlace.decomb
   lvsfunc.deinterlace.dir_deshimmer
   lvsfunc.deinterlace.dir_unsharp
   lvsfunc.denoise.adaptive_mask
   lvsfunc.denoise.detail_mask
   lvsfunc.denoise.quick_denoise
   lvsfunc.misc.edgefixer
   lvsfunc.misc.fix_cr_tint
   lvsfunc.misc.frames_since_bookmark
   lvsfunc.misc.limit_dark
   lvsfunc.misc.load_bookmarks
   lvsfunc.misc.replace_ranges
   lvsfunc.misc.source
   lvsfunc.misc.wipe_row
   lvsfunc.scale.descale
   lvsfunc.scale.descale_detail_mask
   lvsfunc.scale.reupscale
   lvsfunc.scale.test_descale
   lvsfunc.util.pick_removegrain
   lvsfunc.util.pick_repair
   lvsfunc.util.quick_resample

lvsfunc.aa
---------------

.. autosummary::

   lvsfunc.aa.nneedi3_clamp
   lvsfunc.aa.transpose_aa
   lvsfunc.aa.upscaled_sraa

.. automodule:: lvsfunc.aa
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.comparison
-------------------

.. autosummary::

   lvsfunc.comparison.compare
   lvsfunc.comparison.stack_compare
   lvsfunc.comparison.stack_planes
   lvsfunc.comparison.tvbd_diff

.. automodule:: lvsfunc.comparison
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.deinterlace
-------------------

.. autosummary::

   lvsfunc.deinterlace.deblend
   lvsfunc.deinterlace.decomb
   lvsfunc.deinterlace.dir_deshimmer
   lvsfunc.deinterlace.dir_unsharp

.. automodule:: lvsfunc.deinterlace
   :members:
   :undoc-members:
   :show-inheritance:


lvsfunc.denoise
-------------------

.. autosummary::

   lvsfunc.denoise.adaptive_mask
   lvsfunc.denoise.detail_mask
   lvsfunc.denoise.quick_denoise

.. automodule:: lvsfunc.denoise
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.kernels
-------------------

.. automodule:: lvsfunc.kernels
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.misc
-------------------

.. autosummary::

   lvsfunc.misc.allow_vres
   lvsfunc.misc.chroma_injector
   lvsfunc.misc.edgefixer
   lvsfunc.misc.fix_cr_tint
   lvsfunc.misc.frames_since_bookmark
   lvsfunc.misc.limit_dark
   lvsfunc.misc.load_bookmarks
   lvsfunc.misc.replace_ranges
   lvsfunc.misc.source
   lvsfunc.misc.wipe_row

.. automodule:: lvsfunc.misc
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.scale
-------------------

.. autosummary::

   lvsfunc.scale.descale
   lvsfunc.scale.descale_detail_mask
   lvsfunc.scale.reupscale
   lvsfunc.scale.test_descale

.. autoclass:: lvsfunc.scale.Resolution
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.scale.ScaleAttempt
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. automodule:: lvsfunc.scale
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: Resolution, ScaleAttempt

lvsfunc.util
-------------------

.. autosummary::

   lvsfunc.util.one_plane
   lvsfunc.util.pick_removegrain
   lvsfunc.util.pick_repair
   lvsfunc.util.quick_resample

.. automodule:: lvsfunc.util
   :members:
   :undoc-members:
   :show-inheritance:


Special credits
-------------------
A special thanks to every contributor that contributed to lvsfunc.

`The list of contributors can be found here. <https://github.com/Irrational-Encoding-Wizardry/lvsfunc/graphs/contributors>`_



Footer
---------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
