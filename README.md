lvsfunc, a collection of VapourSynth functions and wrappers written and/or "borrowed" by LightArrowsEXE.
Full information on how every function/wrapper works can be found in the docstrings.

## How to use

lvsfunc makes use of submodules, which is a rather foreign concept to most VapourSynth users (considering how bad the whole *func system is). Thus, here is an explanation on how to import these functions.

The function is split up into multiple submodules, each with their own namespace. If you want to, for example, use `upscaled_sraa`, you can call it like so:
```py
import lvsfunc as lvf

aa = lvf.aa.upscaled_sraa()
```

This extends to every function and wrapper in lvsfunc. Below you can find a list of which submodule includes what function/wrapper.

## Included functions and wrappers

This function offers the following (sorted by category):</br>

| Namespace | Function | Shorthand | Short Description | Parameters |
|----------|----------|-----------|-------------|------------|
| aa | nneedi3_clamp | | Clamps the change between nnedi3 and eedi3, fixing the artifacting caused by eedi3 | clip, strength, mask, ret_mask, show_mask, opencl |
| aa | transpose_aa | | AA's a clip by transposing it | clip, eedi3 |
| aa | upscaled_sraa | sraa | AA's through a upscaled single-rate AA. Can also be used for scaling | clip, rfactor, rep, h, sharp_downscale |
| comp | compare | comp | Compare two clips by putting them side-by-side in a list | clip_a, clip_b, frames, rand_total, force_resample, print_frame, mismatch |
| comp | stack_compare | scomp | Compare two clips by stacking | clips, make_diff, height, warn |
| comp | stack_planes | | Split and stack the planes of a given clip | clip, stack_vertical |
| comp | tvbd_diff | | Return frames with differences between the tv and bd clips | tv, bd, thr, return_array |
| deint | deblend | | Deblends a clip in an AABBA pattern and returns a decimated clip | clip, rep |
| deint | decomb | | Gets rid of the combing on an interlaced/telecined source | clip, TFF, decimate, vinv, sharpen, dir, rep |
| deint | dir_deshimmer | | Directional deshimmering function | clip, TFF, dh, transpose, show_mask |
| deint | dir_unsharp | | Directional deshimmering function | clip, strength, dir, h |
| den | quick_denoise | qden | Quick denoising function, allowing for different denoisers to be set for the chroma | clip, ref, cmode, sigma, **kwargs |
| misc | edgefixer | | A wrapper for ContinuityFixer that fixes under- and overshoot | clip, left, right, top, down, radius, full_range |
| misc | fix_cr_tint | | Does a rough fix to the green tint present in Crunchyroll encodes | clip, value |
| misc | limit_dark | | Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold | clip, filtered, threshold, threshold_range |
| misc | replace_ranges | rfs | Replaces frame ranges in a clip with those from another clip | clip_a, clip_b, ranges |
| misc | source | src | Automatically determines how a clip or image should be imported | file, ref, force_lsmas, mpls, mpls_playlist, mpls_angle |
| misc | wipe_row | | Simple function to wipe a row with a blank or given clip. | clip, secondary, width, height, offset_x, offset_y, width2, height2, offset_x2, offset_y2, show_mask |
| scale | conditional_descale | cond_desc | Descale a frame if the error doesn't exceed the given threshold | clip, height, kernel, b, c, taps, threshold, upscaler, **upscale_args |
| scale | smart_descale | | A descaling function that compares relative errors between multiple resolutions and descales accordingly | clip, resolutions, b, c, taps, thr, rescale |
| scale | smart_reupscale | | A quick 'n easy wrapper used to re-upscale a descaled clip using smart_descale | clip, width, height, kernel, b, c, taps, **znargs |
| scale | test_descale | | Descales and reupscales the given clip for comparison | clip, height, kernel, b, c, taps, show_error |
| util | create_dmask | | A wrapper to create a luma mask for denoising, debanding, etc. | clip, luma_scaling |
| util | get_scale_filter | | kagefunc's get_descale_filter, but for the internal resizers | kernel, **kwargs |
| util | one_plane | | Returns True if there's only one plane (lol) | clip |
| util | pick_repair | | Returns rgvs.Repair if the clip is 16 bit or lower, else rgsf.Repair | clip |
| util | quick_resample | | A function to quickly resample to 16 bit and back to the original depth | clip, function, **func_args |
| util | resampler | | Really just a barebones version of fvsfunc's Depth to remove a common dependency | clip, bitdepth |


## Requirements:

- Vapoursynth R28 or newer

## Dependencies:

- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)
- [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [kagefunc](https://github.com/Irrational-Encoding-Wizardry/kagefunc)
- [mvsfunc](https://github.com/HomeOfVapourSynthEvolution/mvsfunc)
- [nnedi3_rpow2](https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py)
- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [vsutil](https://github.com/Irrational-Encoding-Wizardry/vsutil)
- [combmask](https://mega.nz/#!whtkTShS!JsDhi-_QGs-kZkzWqgcXHX2MQII4Bl9Y4Ft0zHnXDvk)
- [descale](https://github.com/Irrational-Encoding-Wizardry/vapoursynth-descale) (Specifically the library)

### Optional dependencies:
- waifu2x-caffe
- L-SMASH Source
- d2vsource
- FFMS2

These can all be found at <http://www.vapoursynth.com/doc/pluginlist.html>
<br>
<br>
**For more information on how to use every funtion, please refer to the docstrings.<br>
If you run into any issues, feel free to leave a PR or otherwise contact me on Discord (LightArrowsEXE#0476)**
