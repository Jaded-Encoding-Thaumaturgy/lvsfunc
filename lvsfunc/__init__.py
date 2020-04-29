"""
    lvsfunc, a collection of VapourSynth functions and wrappers written and/or "borrowed" by LightArrowsEXE.
    Information on how every function/wrapper works can be found in the docstrings,
    and a full list of functions can be found in the README.

    If you spot any issues, please do not hesitate to send in a Pull Request
    or reach out to me on Discord (LightArrowsEXE#0476)!
"""

from . import aa, comparison, deinterlace, denoise, util, misc, scale

nneedi3_clamp = aa.nneedi3_clamp
tranpose_aa = aa.transpose_aa
upscaled_sraa = aa.upscaled_sraa

stack_compare = comparison.stack_compare
stack_planes = comparison.stack_planes
tvbd_diff = comparison.tvbd_diff
compare = comparison.compare

deblend = deinterlace.deblend
decomb = deinterlace.decomb
dir_deshimmer = deinterlace.dir_deshimmer
dir_unsharp = deinterlace.dir_unsharp

quick_denoise = denoise.quick_denoise

edgefixer = misc.edgefixer
fix_cr_tint = misc.fix_cr_tint
limit_dark = misc.limit_dark
replace_ranges = misc.replace_ranges
source = misc.source
wipe_row = misc.wipe_row

conditional_descale = scale.conditional_descale
smart_descale = scale.smart_descale
smart_reupscale = scale.smart_reupscale
test_descale = scale.test_descale


# Aliases
sraa = upscaled_sraa
comp = compare
scomp = stack_compare
qden = quick_denoise
src = source
rfs = replace_ranges
cond_desc = conditional_descale
