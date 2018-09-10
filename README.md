Contains scripts that ~~stolen from other people~~ combined into a simple function for Vapoursynth.

## Requirements:
- Vapoursynth R28 or newer

## Dependancies:
- [vsTAAmbk](https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk)
- [fvsfunc](https://github.com/Irrational-Encoding-Wizardry/fvsfunc)

## Usage:
```aa = lvf.fix_eedi3(clip, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1)```</br>
Clamps the artifacting caused by eedi3 with nnedi3. For example stuff like [this](https://i.imgur.com/hYVhetS.jpg).

- *Clip:*</br>
A clip to be processed.</br>
Supported format: Gray and YUV with any subsampling whose bit-depth is 8bit, 10bit or 16bit.



```comp = lvf.compare(clips, frames, match_clips=True)```</br>
Merges given frames from two or more clips for easy comparing.

- *Clips:* ([clip1, clip2, clip3])</br>
Clips to be processed.</br>
You need atleast two clips for this to work.</br>
Supported format: Gray and YUV with any subsampling whose bit-depth is 8bit, 10bit or 16bit.</br>

- *Frames:* ([10, 20, 30, 40, 50])</br>
Frames to compare.<br>

- *match_clips* (Default: True)</br>
Matches dimensions of every clip.</br>
Dimensions are taken from the first given clip.</br>

```aa = lvf.super_aa(clip, mode=1)```</br>
Heavy AAing using transposing.

- *Clip:*</br>
Clip to be processed.</br>

- *Mode:* (Default: 1)
Mode to be used. Modes decide what AA is being used.</br>
1: Nnedi3</br>
2: Eedi3</br>
