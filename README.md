Contains scripts ~~stolen from other people~~ combined into a simple function for Vapoursynth.

This function offers the following:</br>

- compare(clip_a, clip_b, frames: int, mark=False, mark_a=' Clip A ', mark_b=' Clip B ', fontsize=57)
- stack_compare(clips, width=None, height=None, stack_vertical=False):
- transpose_aa(clip, eedi3=False)
- NnEedi3(clip, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1)
- quick_denoise(clip, mode='knlm', bm3d=True, sigma=3, h=1.0, refine_motion=True, sbsize=16, resample=True)
 
For more information, check the docstrings in the func.

## Requirements:

- Vapoursynth R28 or newer</br>

## Dependencies:

- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)
- [mvsfunc](https://github.com/HomeOfVapourSynthEvolution/mvsfunc)
- [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [nnedi3_rpow2](https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py)
