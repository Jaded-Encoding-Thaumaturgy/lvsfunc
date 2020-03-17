Contains functions I've written or modified for use in VapourSynth.

This function offers the following (sorted by category):</br>

| # | Category | Function | Shorthand | Short Description | Parameters |
|---|----------|----------|-----------|-------------|------------|
| 1 | **Comparison and Analysis** | compare  | comp | Compare two clips by putting them side-by-side in a list | clip_a, clip_b, frames, rand_frames, rand_total, disable_resample |
| 2 | **Comparison and Analysis** | stack_compare | scomp | Compare two clips by stacking | clips, width, height, stack_vertical, make_diff, warn |
| 3 | **Comparison and Analysis** | stack_planes| | Split and stack the planes of a given clip | clip, stack_vertical |
| 4 | **Comparison and Analysis** | tvbd_diff | | Return frames with differences between the tv and bd clips | tv, bd, threshold, print_frame |
| 5 | **Scaling and Resizing** | conditional_descale | cond_desc | Descale a frame if the error doesn't exceed the given threshold | clip, height, b, c, threshold, upscaler |
| 6 | **Scaling and Resizing** | smart_descale | sraa | A descaling function that compares relative errors between multiple resolutions and descales accordingly | clip, res, b, c, thresh1, thresh2, show_mask, show_dmask, sraa_upscale, rfactor, sraa_sharp |
| 7 | **Scaling and Resizing** | test_descale | | Descales and reupscales the given clip for comparison | clip, height, kernel, b, c, taps, show_error |
| 8 | **Antialiasing** | nneedi3_clamp | | Clamps the change between nnedi3 and eedi3, fixing the artifacting caused by eedi3 | clip, strength, mask, ret_mask, show_mask, opencl  |
| 9 | **Antialiasing** | transpose_aa | | AA's a clip by transposing it | clip, eedi3 |
| 10 | **Antialiasing** | upscaled_sraa | | AA's through a upscaled single-rate AA. Can also be used for scaling | clip, rfactor, rep, h, sharp_downscale |
| 11 | **Deinterlacing** | deblend | | Deblends a clip in an AABBA pattern and returns a decimated clip | clip, rep |
| 11 | **Deinterlacing** | decomb | | Gets rid of the combing on an interlaced/telecined source | clip, TFF, decimate, vinv, sharp, dir, rep |
| 12 | **Deinterlacing** | dir_deshimmer | | Directional deshimmering function | clip, TFF, dh, transpose, show_mask |
| 13 | **Deinterlacing** | dir_unsharp | | Directional deshimmering function | clip, strength, dir, h |
| 14 | **Denoising and Debanding** | quick_denoise | qden | Quick denoising function, allowing for different denoisers to be set for the chroma | clip, sigma, cmode, ref, **kwargs |
| 15 | **Masking, Limiting, and Color Handling** | edgefixer | | A wrapper for ContinuityFixer that fixes under- and overshoot | clip, left, right, top, down, radius, full_range |
| 16 | **Masking, Limiting, and Color Handling** | fix_cr_tint | | Does a rough fix to the green tint present in Crunchyroll encodes | clip, value |
| 17 | **Masking, Limiting, and Color Handling** | limit_dark | | Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold | clip, filtered, threshold, threshold_range |
| 19 | **Masking, Limiting, and Color Handling** | wipe_row | | Simple function to wipe a row with a blank or given clip. | clip, secondary, width, height, offset_x, offset_y, width2, height2, offset_x2, offset_y2, show_mask |
| 19 | **Miscellaneous** | source | src | Automatically determines how a clip or image should be imported | file, ref, force_lsmas, mpls, mpls_playlist, mpls_angle |
| 20 | **Experimental** | smarter_descale | | An updated version of smart_descale, hence smart*er*_descale | src, resolutions, descaler, rescaler, upscaler, thr, rescale, to_src |


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
