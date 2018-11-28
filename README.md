Contains scripts ~~stolen from other people~~ combined into a simple function for Vapoursynth.

This function offers the following:</br>

- fix_eedi3(clip, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1)</br>
- compare(clips, frames, match_clips=True)</br>
- super_aa(clip, mode=1)</br>
- denoise(clip, mode=1, bm3d=True, sigma=4, h=1.0, tr=2, refine_motion=True, sbsize=16, sosize=12)</br>
- autoscale(clip, width=None, height=1080, kernel='bicubic', b=1/3, c=1/3, taps=4, mask_lineart=False, rfactor=None)</br>
- Source(path_to_clip, mode=1, resample=False)</br>

## Requirements:

- Vapoursynth R28 or newer</br>

## Dependancies:

- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)
- [mvsfunc](https://github.com/HomeOfVapourSynthEvolution/mvsfunc)
- [havsfunc](https://github.com/HomeOfVapourSynthEvolution/havsfunc)
- [nnedi3_rpow2](https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py)
