Contains functions I've written (and rewritten from others) for use in VapourSynth.

This function offers the following:</br>

- compare(clip_a, clip_b, frames: int, mark=False, mark_a=' Clip A ', mark_b=' Clip B ', fontsize=57)
- stack_compare(clips, width=None, height=None, stack_vertical=False):
- conditional_descale(src, height, b=1/3, c=1/3, threshold=0.003, w2x=False)
- transpose_aa(clip, eedi3=False)
- NnEedi3(clip, mask, strong_mask, show_mask, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1)
- quick_denoise(clip, mode='knlm', bm3d=True, sigma=3, h=1.0, refine_motion=True, sbsize=16, resample=True)
- stack_planes(src, stack_vertical=False)
- source(file, force_lsmas=False, src=None, fpsnum=None, fpsden=None)

## Requirements:

- Vapoursynth R28 or newer</br>

## Dependencies:

- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)
- [mvsfunc](https://github.com/HomeOfVapourSynthEvolution/mvsfunc)
- [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [kagefunc](https://github.com/Irrational-Encoding-Wizardry/kagefunc)
- [vsutil](https://github.com/Irrational-Encoding-Wizardry/vsutil)
- [nnedi3_rpow2](https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py)


## Functions:

### Compare
Allows for the same frames from two different clips to be compared by putting them next to each other in a list. <br>
Shorthand for this function is *"comp"*.

**Example usage:**
```py
import lvsfunc as lvf

comp = lvf.compare(src_a, src_b, frames=[100,200,300])
```

### stack_compare
A simple wrapper that allows you to compare two clips by stacking them. <br>
You can stack an infinite amount of clips. <br>
Shorthand for this function is *"scomp"*.

**Example usage:**
```py
import lvsfunc as lvf

scomp = lvf.stack_compare(src_a, src_b, src_c, height=480)
```

### conditional_descale

Descales and reupscales a clip. If difference exceeds the threshold, the frame will not be descaled. <br>
If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe. <br>
This function currently only supports bicubic descaling. <br>

It is adviced to scenefilter scenes that have credits or other native 1080p elements over them, as those will not be descaled otherwise.

**Example usage:**

Standard usage
```py
import lvsfunc as lvf

descaled = lvf.conditional_descale(src, height=540, b=0, c=1)
```

Scenefiltering the Opening and Ending of an anime
```py
import lvsfunc as lvf
import fvsfunc as fvf
import kagefunc as kgf
from nnedi3_rpow2 import nnedi3_rpow2

descaled_a = lvf.conditional_descale(src, height=540, b=0, c=1, w2x=True)
descaled_b = kgf.inverse_scale(src, height=540, kernel='bicubic', b=0, c=1, mask_detail=True)
descaled_b = nnedi3_rpow2(descaled_b).resize.Spline36(src.width, src.height)

descaled = fvf.rfs(descaled_a, descaled_b, mappings=f"[{opstart} {opstart+2159}] [{edstart} {edstart+2157}]")
```

### transpose_aa

Function written by Zastin and modified by me. <br>
Performs anti-aliasing over a clip by using nnedi3, transposing, using nnedi3 again, and transposing a final time. <br>
This results in overall stronger aliasing. <br>
Useful for shows like Yuru Camp with bad lineart problems.

If Eedi3=False, it will use Nnedi3 instead.

### NnEedi3

Function written by Zastin. <br>
What it does is clamp the "change" done by Eedi3 to the "change" of Nnedi3. <br>
This should fix every issue created by Eedi3.


### stack_planes

Stacks the planes of a clip.


### source

Generic clip import function. <br>
Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced. <br>
It also automatically determines if an image has been imported. You can set its fps using `fpsnum` and `fpsden`, or using a reference clip with `src`.

**Example usage:**

Importing a standard clip
```py
import lvsfunc as lvf

src = lvf.src("BDMV/STREAM/00000.m2ts")
```

Importing a custom mask, converting it to GRAY, binarizing it, and making is 2156 frames long.
```py
import lvsfunc as lvf

mask = lvf.src(r'mask.png', src).resize.Point(format=vs.GRAY8, matrix_s='709').std.Binarize()*2156
```
