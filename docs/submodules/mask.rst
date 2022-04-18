lvsfunc.mask
-------------------

Masks are used to limit where filtering takes place, and how strong the filtering applied is.
`lvsfunc` offers a couple of masks, and they're often used internally in other functions.

All masks also come limited by default, so you don't need to worry about illegal ranges messing with your masked output.

.. autosummary::

    lvsfunc.mask.BoundingBox
    lvsfunc.mask.DeferredMask
    lvsfunc.mask.detail_mask
    lvsfunc.mask.detail_mask_neo
    lvsfunc.mask.halo_mask
    lvsfunc.mask.mt_xxpand_multi
    lvsfunc.mask.range_mask

.. autoclass:: lvsfunc.mask.BoundingBox
    :members:
    :undoc-members:
    :show-inheritance:
    :member-order: bysource

.. autoclass:: lvsfunc.mask.DeferredMask
    :members:
    :undoc-members:
    :show-inheritance:
    :member-order: bysource

.. automodule:: lvsfunc.mask
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: BoundingBox, DeferredMask, minm, maxm
