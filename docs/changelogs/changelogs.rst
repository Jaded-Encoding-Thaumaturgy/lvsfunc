Changelogs
----------

.. image::
    https://img.shields.io/github/commits-since/Irrational-Encoding-Wizardry/lvsfunc/v0.4.1

This page may be outdated, but the `releases page <https://github.com/Irrational-Encoding-Wizardry/lvsfunc/releases>`_
on Github should always be up-to-date.

------------------

v0.4.2
^^^^^^

**lvsfunc now requires Python 3.10 and VapourSynth 58!**

**Changelog**
* setup.py updates, should now show extra info on pypi
* Docs overhaul
* Lots of docstrings updated to include additional information and warnings
* Add shields to README
* Create unittests for most lvsfunc functions
* Move around certain functions (mainly to `types` and `util`)
* `denoise` renamed to `noise`. Temporary alias still exists.

**New additions**
* `get_matrix_curve`
    - Returns a `TransferCharacteristics` based on a given `matrix`.
* `chickendream`
    - A wrapper around the graining plugin, chickendream, a plug-in that implements a realistic film grain generator.
* `check_variable_format`
* `check_variable_resolution`
    - Separated functionality from `check_variable` into their own functions. `check_variable` still checks both.
* New custom exceptions. Please check [the documentation for a full list](https://lvsfunc.encode.moe/en/latest/submodules/exceptions.html).

**Updates**
* All masking functions now automatically limit their output (This means no weird masking shenanigans because of out-of-range values)
* `get_matrix`: New option to return `types.Matrix` instead of an int. This will at some point become the default behaviour.
* `tivtc_vfr`: Should now properly allow users to do an analysis pass without erroring (See: #90. Thanks @Setsugennoao and @RivenSkaye!)
* `tivtc_vfr`: `mode=4` during the analysis pass can now be overridden
* `ssim_downsample`: Automatically determine `curve` if None is passed
* `taa`: Fix the wrong width being passed
* `overlay_sign`: Fix float clip range issues
* Remove the following aliases: `misc.get_matrix`, `misc.replace_ranges`, `misc.scale_thresh`, `recon.ChromaReconstruct`, `recon.crecon`, `recon.demangle`.
* A lot of other minor changes and fixes

* Move the following functions to `util`:
    - misc.get_matrix
    - misc.allow_variable
    - misc.colored_clips
    - misc.frames_since_bookmark
    - misc.load_bookmarks
    - misc.get_prop
    - misc.check_variable
    - misc.chroma_injector
    - misc.get_neutral_value

* Move the following types to `types`:
    - CURVES
    - CreditMask
    - CustomScaler
    - Direction
    - F
    - RegressClips
    - Resolution
    - ScaleAttempt
    - SceneChangeMode
    - T
    - VideoProp


------------------


v0.4.1
^^^^^^

**Changelog**

* Fix docs building
* Remove decorators in favour of a simple function. This makes the docs build again, and will be a bit easier to maintain myself.
* Add some missing functions to the docs
* Set all the outputs per submodule (`__all__`). This means that if you were relying on lvsfunc to import your vsutil functions, stop it. Just import vsutil.
* Docstring updates
* Changed some ALLCAPS function names to camel case. These will remain for the time being, but be deprecated before 0.5.0.

**New additions**

* `vinverse`
    * @Setsugennoao's implementation of `vinverse`
* `get_neutral_value`
* kernels (#91)
    * Add a *lot* of new kernels. See the documentation for a full list.
* `get_kernel` and `get_all_kernels`
    * This should allow for developers using the lvsfunc `kernel` setup to allow its users to fall back on strings.
* `check_variable`
    * Checks whether the clip has a variable format or resolution, and returns an error if so. Replaces the decorators.
* `mixed_rescale`
    * WIP scaling function that mimics some of the ideas of `insaneAA` while trying to limit the amount of damage caused by its default options. This should also be easier to modify to your needs.
* `fine_dehalo`
    * Ported over the module floating around to use lvsfunc functions and style. Has the added `ref` parameter as well.
* `mt_xxpand_multi`

**Updates**

* Use lambdas or `None` for params where necessary
* `decomb`: Use `lvsfunc.deinterlace.vinverse` instead of `havsfunc.vinverse`
* `stack_planes`: Fix `split` call referencing `comparison.split`
* `upscaled_sraa`: Generalize `supersampler` param (#89)
* `vsdpir`: Fix error on non mod8 clips (#88)
* `unsharpen`: Add `GRAY` support
* `TIVTC_VFR`: Add main file name to output filenames
* Multiple functions: Add string support for calling `kernels`
* `masked_dha`: Add `ref` param
* `replace_ranges`: Call Remap plugin if possible
* Other minor updates I forgot about

**Deprecations**

* SIVTC, TIVTC_VFR: both use camel case now. The FULLCAPS calls will be support for the time being, but support will be dropped before 0.5.0.


------------------


v0.4.0
^^^^^^

**Changelog**

* Update stubs
* Update requirements.txt
* Other miscellaneous fixes and speed-ups
* Docstring and typing updates
* Remaining ports to APIv4.0

**New additions**

* `descale_fields`
    - Simple descaling wrapper for interwoven upscaled fields.
* `ssim_downsample`
    - muvsfunc.ssim_downsample rewrite taken from a Vardë gist. Unlike muvsfunc's implementation, this function also works in float and does not use nnedi3_resample.
* `gamma2linear`
* `linear2gamma`
* `fix_telecined_fades`
    - A filter that gives a mathematically perfect solution to fades made *after* telecining (which made perfect IVTC impossible). This is an improved version of the Fix-Telecined-Fades plugin that deals with overshoot/undershoot by adding a check.
* `overlay_sign`
    - Wrapper to overlay a logo or sign onto another clip. Rewrite of fvsfunc.InsertSign.
* `comparative_descale`
    - Easy wrapper to descale to SharpBicubic and an additional kernel,  compare them, and then pick one or the other.
* `comparative_rescale`
    - Companion function to go with comparative_descale to reupscale the clip for descale detail masking.
* `detail_mask_neo`
    - A new detail mask aimed at preserving as much detail as possible within darker areas, even if it winds up being mostly noise.
* `seek_cycle`
    - Purely visual tool to view telecining cycles.
* `bob`
    - Very simple bobbing function. Shouldn't be used for regular filtering, but as a very cheap bobber for other functions.
* `ivtc_credits`
    - Deinterlacing function for interlaced credits (60i/30p) on top of telecined video (24p). This is a combination of havsfunc's dec_txt60mc, ivtc_txt30mc, and ivtc_txt60mc functions. The credits are interpolated and decimated to match the output clip.
* `unsharpen`
    - Diff'd unsharpening function. Performs one-dimensional sharpening as such: "Original + (Original - blurred) * Strength". It then merges back noise and detail that was prefiltered away,

**Updates**

* `kernels.lanczos`: Set taps to use the default zimg amount
* all named `kernels`: Default values added to docstring, allowing for easy checking what values are passed
* all `kernels`: Add `resample` and `shift` methods
* `based_aa`: Fix sclip, new lmask, tff param, set ssim_downsample as default downscaler
* `vsdpir`: Now uses `vs-mlrt` instead of `vs-dpir` internally, allowing users to force tensorrt usage

**Deprecations**

* dir_deshimmer
* dir_unsharpen
* deemphasize
* test_descale

------------------

v0.3.11
^^^^^^^

**Changelog**

* Update stubs
* Update required packages
* Other miscellaneous fixes and speed-ups
* Docstring and typing updates
* APIv4.0 fixes (turns out I had a few things to change...)

**New additions**

* `based_aa`
    - As the name implies, this is a based anti-aliaser. Thank you, based Zastin. This relies on FSRCNNX being very sharp, and as such it very much acts like the main “AA” here.
* `clamp_values`
    - Forcibly clamps the given value x to a max and/or min value.
* `fun` submodule for dumb stuff
    - These additions will be excluded from future changelogs.
* `BicubicDidee`
    - Kernel inspired by a Didée post. See: https://forum.doom9.org/showthread.php?p=1748922#post1748922.

**Updates**

* `vsdpir`: Fix `matrix=None` behaviour, add a check for clip format, add a vsdpir version check, kwargs, etc.
* `masked_dha`: Fix darkstr range
* `diff`: Overloading, add `exclusion_ranges` and `return_ranges`
* aa functions: Change shifting kernel from `Spline36` to `Catrom`
* `tivtc_vfr`: Add decimation parameters (see docstrings for further info), allow overriding of `hybrid` and `vfrDec` for tdec,
* `deblend`: Add `start` option, `decimation` options
* `decomb`: Remove `sharpen` arg, individual kwargs for specific operations, replace vinverse plugin with havsfunc's Vinverse
* `source`: Add mp4 handling
* Other changes and fixes I probably forgot about.

**Notices**
I forgot to leave a warning for it in this version, but `dir_deshimmer` and `dir_unsharp` will *no longer be support in the next version*. If you're using them, first of all *why*, and second, you'll want to update your scripts.

------------------

v0.3.10
^^^^^^^

**Changelog**

* Updated stubs
* Woke up to not needing to update anything for APIv4! \o/
* Minor typo fixes
* Deprecation warnings added to certain functions. The following functions are deprecated and will be removed for v0.4.0:
    - deemphasize
    - dir_deshimmer
* Future warnings added to certain functions. The following functions will likely receive an extensive rewrite in a future commit:
    - dir_unsharp
    - detail_mask ([see branch](https://github.com/Irrational-Encoding-Wizardry/lvsfunc/tree/detail_mask_rewrite))
    - edgefixer

**New additions**

* `deblock.vsdpir`
    - A simple vs-dpir wrapper for convenience. Converts to RGB -> runs vs-dpir -> converts back to original format.
* `dehalo.masked_dha`
    - A combination of the best of DeHalo_alpha and BlindDeHalo3, plus a few minor tweaks to the masking. Adopted from G41Fun.
* `util.padder`
    - New padding utility function. Pads out the pixels on the side by the given amount of pixels.
* `util.force_mod`
    - Force output to fit a specific MOD. Minimum returned value will always be mod².
* `util.scale_peak`
    - Full-range scale function that scales a value from [0, 255] to [0, peak]

**Updates**

* `mask.detail_mask`
    - Remove unnecessary chroma params
* `util.quick_resample`
    - Add float 32bit step

------------------

v0.3.9
^^^^^^

**Changelog**

* Revert vsdpir as hard-dependency.
    - This dependency was removed from the `requirements.txt` due to it forcing you to install the `pytorch` library, which is positively massive. If you want to use `autodb_dpir`, you should `pip install vsdpir` yourself.

------------------

v0.3.8
^^^^^^

**Changelog**

* Update stubs
* Update docs
* Update requirements
* Minor typehinting updates
* Minor internal call changes

**New additions**

* `autodb_dpir`
    - A rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.
    - Thanks @Ichunjo, @louis3939, @Setsugennoao for helping out!

* `deemphasize`
   - A function that attempts to deemphasize ringing common to SD video signals resulting from a playback device in the transfer chain poorly compensating for pre-emphasis baked into the source signal.

* `Matrix`
    - New IntEnum Matrix class to represent matrix coefficients following ITU-T H.265 Table E.5

**Updates**

* `__init__`
    - Add render export (#61)
* `find_scene_changes`
    - Remove duplicate progress callback
* `nneedi3_clamp`
    - Remove Kirsch as a dependency, replace with Prewitt
* `TIVTC_VFR`
    - Free filter, should no longer require a forced preview refresh
* `SIVTC`
    - Add `pattern` frameprop

------------------

v0.3.7
^^^^^^

**Changelog**

* Update stubs
* Update docs


**New Additions:**

* `deinterlace.TIVTC_VFR`
    - Wrapper for performing TFM and TDecimate on a clip that is supposed to be VFR, including generating a metrics/matches/timecodes txt file.
* `dehardsub.HardsubASS`
    - Generate a mask using an ass script, such as for dehardubbing AoD with CR DE.
* `render.get_render_process`


**Updates:**

* Functions with progress bars
    - Update progress method, running them will probably be faster now

* `clip_async_render`
    - Add `progress` param: String to use for render progress display.
    - Fix a bug where it tried to read timecode information from clips that didn't have any

------------------

v0.3.6
^^^^^^

**Changelog**

* Updated various error messages to use the correct function names
* Couple README updates, disclaimer about unstable API included
* Typing fixes in `util`
* Minor docstring corrections

**Updates:**

* `misc.ripe_row`:
    - Rewrite. It now uses a `mask.BoundingBox` instead of `kagefunc.squaremask` and you can no longer wipe two separate rows/columns at once anymore.

* `replace_ranges`:
    - Moved to `util` (still accessible through `misc` and `lvsfunc.rfs`, but the former will be deprecated at some point in the future)
    - Allow for negative and nonetype inputs (for a more apt description, check the docstring)

* `scale_thresh`:
    - Moved to `util` (still accessible through `misc`, but that will be deprecated at some point in the future)

* `nneedi3_clamp`:
    - Fix bug where `strength` would not be used properly

* `bidehalo`:
    - Import dehalo submodule in `__init__` (oops)
    - Add `sigmaS_final` and `sigmaR_final` parameters. By default `sigmaS_final` will be 1/3rd of `sigmaS`, and `sigmaR_final` will be the same as `sigmaR`. For more information, consult the docstrings

------------------

v0.3.5
^^^^^^

**Changelog**

New Additions:

* Add named Bicubic kernels (BSpline, Hermite, Mitchell, Catrom, BicubicSharp, RobidouxSoft, Robidoux, RobidouxSharp)
* Add a keyframe generator (render.find_scene_changes)
    - Outputs a list of scenechanges determined by wwxd, scxvid, frames only found by both, or frames found by either

Updates to functions:

* Update dehalo.bidehalo
    - Remove masking, this is now up to the user to handle
    - Fix bug where float clips would error because bilateral can't handle them

* Source

    - Fix a bug where the improper Matrix params would be passed (int to str param instead of int param which would break clips if you used `ref`)

------------------

Older Versions
^^^^^^^^^^^^^^

This is the bottom of the changelogs.
`lvsfunc` was undocumented before this version.
