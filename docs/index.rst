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

* `havsfunc <https://github.com/HomeOfVapourSynthEvolution/havsfunc>`_
* `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_
* `vsutil <https://pypi.org/project/vsutil/>`_

The following VapourSynth libraries are also required for full functionality:

* `combmask <https://mega.nz/#!whtkTShS!JsDhi-_QGs-kZkzWqgcXHX2MQII4Bl9Y4Ft0zHnXDvk>`_
* `d2vsource <https://github.com/dwbuiten/d2vsource>`_
* `dgdecnv <http://rationalqm.us/dgdecnv/dgdecnv.html>`_
* `ffms2 <https://github.com/FFMS/ffms2>`_
* `fmtconv <https://github.com/EleonoreMizo/fmtconv>`_
* `KNLMeansCL <https://github.com/Khanattila/KNLMeansCL>`_
* `L-SMASH-Works <https://github.com/VFR-maniac/L-SMASH-Works>`_
* `RGSF <https://github.com/IFeelBloated/RGSF>`_
* `TIVTC <https://github.com/dubhater/vapoursynth-tivtc>`_
* `VapourSynth-Bilateral <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Bilateral>`_
* `VapourSynth-BM3D <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-BM3D>`_
* `VapourSynth-descale <https://github.com/Irrational-Encoding-Wizardry/VapourSynth-descale>`_
* `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
* `VapourSynth-fillborders <https://github.com/dubhater/vapoursynth-fillborders>`_
* `VapourSynth-nnedi3 <https://github.com/dubhater/VapourSynth-nnedi3>`_
* `VapourSynth-NNEDI3CL <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-NNEDI3CL3>`_
* `VapourSynth-ReadMpls <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-ReadMpls>`_
* `VapourSynth-Retinex <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-Retinex>`_
* `vs-ContinuityFixer <https://github.com/MonoS/VS-ContinuityFixer>`_
* `zimg <https://github.com/sekrit-twc/zimg>`_
* `znedi3 <https://github.com/sekrit-twc/znedi3>`_

This list is non-exhaustive, as dependencies may have their own dependencies.
An attempt has been made to document major dependencies on a per-function basis.
Unfortunately, \*func family modules have complex dependency graphs and documenting
them is beyond the scope of this module.

Disclaimer
----------------

Anything **MAY** change at any time.
The public API **SHOULD NOT** be considered stable.
If you use lvsfunc in any of your projects,
consider hardcoding a version requirement.

Modules
-------

.. autosummary::

   lvsfunc.aa
   lvsfunc.comparison
   lvsfunc.deblock
   lvsfunc.dehalo
   lvsfunc.dehardsub
   lvsfunc.deinterlace
   lvsfunc.denoise
   lvsfunc.kernels
   lvsfunc.mask
   lvsfunc.misc
   lvsfunc.recon
   lvsfunc.render
   lvsfunc.scale
   lvsfunc.types
   lvsfunc.util

Functions
---------

.. autosummary::

   lvsfunc.aa.clamp_aa
   lvsfunc.aa.eedi3
   lvsfunc.aa.nnedi3
   lvsfunc.aa.nneedi3_clamp
   lvsfunc.aa.taa
   lvsfunc.aa.transpose_aa
   lvsfunc.aa.upscaled_sraa
   lvsfunc.comparison.compare
   lvsfunc.comparison.diff
   lvsfunc.comparison.diff_hardsub_mask
   lvsfunc.comparison.interleave
   lvsfunc.comparison.split
   lvsfunc.comparison.stack_compare
   lvsfunc.comparison.stack_horizontal
   lvsfunc.comparison.stack_planes
   lvsfunc.comparison.stack_vertical
   lvsfunc.comparison.tile
   lvsfunc.deblock.autodb_dpir
   lvsfunc.deblock.vsdpir
   lvsfunc.dehalo.bidehalo
   lvsfunc.dehalo.deemphasize
   lvsfunc.dehalo.masked_dha
   lvsfunc.dehardsub.bounded_dehardsub
   lvsfunc.dehardsub.get_all_masks
   lvsfunc.dehardsub.hardsub_mask
   lvsfunc.deinterlace.deblend
   lvsfunc.deinterlace.decomb
   lvsfunc.deinterlace.dir_deshimmer
   lvsfunc.deinterlace.dir_unsharp
   lvsfunc.deinterlace.SIVTC
   lvsfunc.deinterlace.TIVTC_VFR
   lvsfunc.denoise.bm3d
   lvsfunc.mask.detail_mask
   lvsfunc.mask.halo_mask
   lvsfunc.mask.range_mask
   lvsfunc.misc.allow_variable
   lvsfunc.misc.chroma_injector
   lvsfunc.misc.colored_clips
   lvsfunc.misc.edgefixer
   lvsfunc.misc.frames_since_bookmark
   lvsfunc.misc.get_matrix
   lvsfunc.misc.limit_dark
   lvsfunc.misc.load_bookmarks
   lvsfunc.misc.shift_tint
   lvsfunc.misc.source
   lvsfunc.misc.wipe_row
   lvsfunc.recon.chroma_reconstruct
   lvsfunc.render.clip_async_render
   lvsfunc.render.find_scene_changes
   lvsfunc.render.get_render_process
   lvsfunc.scale.descale
   lvsfunc.scale.descale_detail_mask
   lvsfunc.scale.reupscale
   lvsfunc.scale.test_descale
   lvsfunc.util.force_mod
   lvsfunc.util.normalize_ranges
   lvsfunc.util.padder
   lvsfunc.util.pick_removegrain
   lvsfunc.util.pick_repair
   lvsfunc.util.quick_resample
   lvsfunc.util.replace_ranges
   lvsfunc.util.scale_peak
   lvsfunc.util.scale_thresh

lvsfunc.aa
---------------

.. autosummary::

   lvsfunc.aa.clamp_aa
   lvsfunc.aa.eedi3
   lvsfunc.aa.nnedi3
   lvsfunc.aa.nneedi3_clamp
   lvsfunc.aa.taa
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
   lvsfunc.comparison.diff
   lvsfunc.comparison.diff_hardsub_mask
   lvsfunc.comparison.interleave
   lvsfunc.comparison.split
   lvsfunc.comparison.stack_compare
   lvsfunc.comparison.stack_horizontal
   lvsfunc.comparison.stack_planes
   lvsfunc.comparison.stack_vertical
   lvsfunc.comparison.tile

.. automodule:: lvsfunc.comparison
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.deblock
-------------------

.. autosummary::

   lvsfunc.deblock.autodb_dpir
   lvsfunc.deblock.vsdpir

.. automodule:: lvsfunc.deblock
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.dehalo
-------------------

.. autosummary::

   lvsfunc.dehalo.bidehalo
   lvsfunc.dehalo.deemphasize
   lvsfunc.dehalo.masked_dha

.. automodule:: lvsfunc.dehalo
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.dehardsub
-----------------

.. autosummary::

   lvsfunc.dehardsub.bounded_dehardsub
   lvsfunc.dehardsub.get_all_masks
   lvsfunc.dehardsub.hardsub_mask

.. autoclass:: lvsfunc.dehardsub.HardsubMask
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.dehardsub.HardsubSign
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.dehardsub.HardsubSignKgf
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.dehardsub.HardsubLine
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.dehardsub.HardsubLineFade
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. automodule:: lvsfunc.dehardsub
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: HardsubMask, HardsubSign, HardsubSignKgf, HardsubLine, HardsubLineFade

lvsfunc.deinterlace
-------------------

.. autosummary::

   lvsfunc.deinterlace.deblend
   lvsfunc.deinterlace.decomb
   lvsfunc.deinterlace.dir_deshimmer
   lvsfunc.deinterlace.dir_unsharp
   lvsfunc.deinterlace.SIVTC
   lvsfunc.deinterlace.TIVTC_VFR

.. automodule:: lvsfunc.deinterlace
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.denoise
-------------------

.. autosummary::

   lvsfunc.denoise.bm3d

.. automodule:: lvsfunc.denoise
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.mask
-------------------

.. autosummary::

   lvsfunc.mask.detail_mask
   lvsfunc.mask.halo_mask
   lvsfunc.mask.range_mask

.. autoclass:: lvsfunc.mask.BoundingBox
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. autoclass:: lvsfunc.mask.DeferredMask
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

.. automodule:: lvsfunc.mask
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: BoundingBox, DeferredMask

lvsfunc.kernels
-------------------

.. automodule:: lvsfunc.kernels
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.misc
-------------------

.. autosummary::

   lvsfunc.misc.allow_variable
   lvsfunc.misc.chroma_injector
   lvsfunc.misc.colored_clips
   lvsfunc.misc.edgefixer
   lvsfunc.misc.frames_since_bookmark
   lvsfunc.misc.get_matrix
   lvsfunc.misc.limit_dark
   lvsfunc.misc.load_bookmarks
   lvsfunc.misc.shift_tint
   lvsfunc.misc.source
   lvsfunc.misc.wipe_row

.. automodule:: lvsfunc.misc
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.recon
-------------------

.. autosummary::

   lvsfunc.recon.chroma_reconstruct

.. automodule:: lvsfunc.recon
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.render
-------------------

.. autosummary::

   lvsfunc.render.clip_async_render
   lvsfunc.render.find_scene_changes
   lvsfunc.render.get_render_process

.. automodule:: lvsfunc.render
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

lvsfunc.types
-------------

.. automodule:: lvsfunc.types
   :members:
   :undoc-members:
   :show-inheritance:

lvsfunc.util
-------------------

.. autosummary::

   lvsfunc.util.force_mod
   lvsfunc.util.get_prop
   lvsfunc.util.normalize_ranges
   lvsfunc.util.padder
   lvsfunc.util.pick_removegrain
   lvsfunc.util.pick_repair
   lvsfunc.util.quick_resample
   lvsfunc.util.replace_ranges
   lvsfunc.util.scale_peak
   lvsfunc.util.scale_thresh

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
