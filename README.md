Contains functions I've written or modified for use in VapourSynth.

This function offers the following (sorted by category):</br>

| # | Category | Function | Shorthand | Short Description | Parameters |
|---|----------|----------|-----------|-------------|------------|
| 1 | **Comparison and Analysis** | compare  | comp | Compare two clips by putting them side-by-side in a list | clip_a, clip_b, frames, rand_frames, rand_total, disable_resample |
| 2 | **Comparison and Analysis** | stack_compare | scomp | Compare two clips by stacking | clips, width, height, stack_vertical, make_diff |
| 3 | **Comparison and Analysis** | stack_planes| | Split and stack the planes of a given clip | clip, stack_vertical |
| 4 | **Comparison and Analysis** | tvbd_diff | | Return frames with differences between the tv and bd clips | tv, bd, threshold |
| 5 | **Scaling and Resizing** | conditional_descale | cond_desc | Descale a frame if the error doesn't exceed the given threshold | clip, height, b, c, threshold, w2x
| 6 | **Scaling and Resizing** | smart_descale | | A descaling function that compares relative errors between multiple resolutions and descales accordingly | clip, res, b, c, thresh1, thresh2, show_mask, show_dmask, single_rate_upscale, rfactor |
| 7 | **Scaling and Resizing** | test_descale | | Descales and reupscales the given clip for comparison | clip, height, kernel, b, c, taps |
| 8 | **Antialiasing** | transpose_aa | | AA's a clip by transposing it | clip, eedi3 |
| 9 | **Antialiasing** | upscaled_sraa | | AA's through a upscaled single-rate AA | clip, rfactor, rep, h |
| 10 | **Antialiasing** | nneedi3_clamp | | Clamps the change between nnedi3 and eedi3, fixing the artifacting caused by eedi3 | clip, mask, strong_mask, show_mask, opencl, strength, alpha, beta, gamma, nrad, mdis, nsize, nns, qual |
| 11 | **Deinterlacing** | deblend | | Deblends a clip in an AABBA pattern and returns a decimated clip | clip, rep |
| 12 | **Denoising and Debanding** | quick_denoise | qden | Quick denoising function, allowing for different denoisers to be set for the chroma | clip, sigma, cmode, ref, **kwargs |
| 13 | **Masking, Limiting, and Color Handling** | limit_dark | | Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold | clip, filtered, threshold, threshold_range |
| 14 | **Masking, Limiting, and Color Handling** | fix_cr_tint | | Does a rough fix to the green tint present in Crunchyroll encodes | clip, value |
| 15 | **Masking, Limiting, and Color Handling** | wipe_row | | Simple function to wipe a row with a blank or given clip. | clip, secondary, width, height, offset_x, offset_y, width2, height2, offset_x2, offset_y2, show_mask |
| 16 | **Miscellaneous** | source | src | Automatically determines how a clip or image should be imported | scr, force_lsmas, ref, fpsnum, fpsden


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

### Optional dependencies:
- waifu2x-caffe
- L-SMASH Source
- d2vsource
- FFMS2

These can all be found at <http://www.vapoursynth.com/doc/pluginlist.html>
<br>
<br>
**For more information on how to use every funtion, please refer to the docstrings.**