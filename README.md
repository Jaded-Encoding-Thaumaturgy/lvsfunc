Contains functions I've written (and rewritten from others) for use in VapourSynth.

This function offers the following:</br>

- compare(clip_a, clip_b, frames: int, force_resample: bool, rand_frames: bool, rand_total: int)
- stack_compare(clips, width: int, height: int, stack_vertical: bool)
- conditional_descale(clip, height: int, b: float, c: float, threshold: float, w2x: bool)
- transpose_aa(clip, eedi3: bool)
- nneedi3_clamp(clip, mask, strong_mask: bool, show_mask: bool, opencl: bool, strength=1, alpha: float, beta: float, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1)
- quick_denoise(clip, sigma=4, cmode='knlm', ref, **kwargs)
- stack_planes(clip, stack_vertical: bool)
- source(file, force_lsmas: bool, ref, fpsnum: int, fpsden: int)

## Requirements:

- Vapoursynth R28 or newer</br>

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

Can be found at <http://www.vapoursynth.com/doc/pluginlist.html>

## Functions:

### Compare
Allows for the same frames from two different clips to be compared by putting them next to each other in a list. <br>
Shorthand for this function is `comp`.

**Example usage:**

Standard usage
```py
import lvsfunc as lvf

comp = lvf.compare(clip_a, clip_b, frames=[100,200,300])
```

Randomly pick 15 frames and force clips to match
```py
import lvsfunc as lvf

comp = lvf.compare(clip_a, clip_b, force_resample=True, rand_frames=True, rand_total=15)
```

### stack_compare
A simple wrapper that allows you to compare two clips by stacking them. <br>
You can stack an infinite amount of clips. <br>
Shorthand for this function is `scomp`.

**Example usage:**
```py
import lvsfunc as lvf

scomp = lvf.stack_compare(clip_a, clip_b, clip_c, height=480)
```

### conditional_descale

Descales and reupscales a clip. If the difference exceeds the threshold, the frame will not be descaled. <br>
If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe. <br>
This function currently only supports bicubic descaling. <br>

It is adviced to scenefilter scenes that have credits or other native 1080p elements over them, as those will not be descaled otherwise.

**Example usage:**

Standard usage
```py
import lvsfunc as lvf

descaled = lvf.conditional_descale(clip, height=540, b=0, c=1)
```

Scenefiltering the Opening and Ending of an anime
```py
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
from nnedi3_rpow2 import nnedi3_rpow2

descaled_a = lvf.conditional_descale(clip, height=540, b=0, c=1, w2x=True)
descaled_b = kgf.inverse_scale(clip, height=540, kernel='bicubic', b=0, c=1, mask_detail=True)
descaled_b = nnedi3_rpow2(descaled_b).resize.Spline36(clip.width, clip.height)

descaled = fvf.rfs(descaled_a, descaled_b, mappings=f"[{opstart} {opstart+2159}] [{edstart} {edstart+2157}]")
```

### transpose_aa

Function written by Zastin and modified by me. <br>
Performs anti-aliasing over a clip by using nnedi3, transposing, using nnedi3 again, and transposing a final time. <br>
This results in overall stronger aliasing. <br>
Useful for shows like Yuru Camp with bad lineart problems.

If eedi3=False, it will use Nnedi3 instead.

### nneedi3_clamp

Function written by Zastin. <br>
What it does is clamp the "change" done by Eedi3 to the "change" of Nnedi3. <br>
This should fix every issue created by Eedi3.


### stack_planes

Stacks the planes of a clip.


### source

Generic clip import function. <br>
Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced. <br>
It also automatically determines if an image has been imported. You can set its fps using `fpsnum` and `fpsden`, or using a reference clip with `ref`. <br>
Shorthand for this function is `src`.

**Example usage:**

Importing a standard clip
```py
import lvsfunc as lvf

bluray = lvf.src("BDMV/STREAM/00000.m2ts")
```

Importing a custom mask, converting it to GRAY, binarizing it, and making is 2156 frames long.
```py
import lvsfunc as lvf

mask = lvf.src(r'mask.png', ref=clip_a).resize.Point(format=vs.GRAY8, matrix_s='709').std.Binarize()*2156
```
