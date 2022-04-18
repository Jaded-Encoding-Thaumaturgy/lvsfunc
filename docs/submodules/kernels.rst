lvsfunc.kernels
---------------

.. autosummary::

    lvsfunc.kernels.get_kernel
    lvsfunc.kernels.get_all_kernels

`Kernels` are a collection of wrappers pertaining to (de)scaling, format conversion, and other related operations, all while providing a consistent and clean interface. This allows for easy expansion and ease of use for any other maintainers who wishes to use them in their own functions.

You can create presets for common scaling algorithms or settings, while ensuring the interface will always remain the same, even across different plugins with their own settings and expected behavior.

For example, if you want to downscale a video clip to 1280x720 using Bicubic (b=0, c=1), you can call the preset, :py:class:`lvsfunc.kernels.SharpBicubic`, like so:

.. code-block:: py

    kernels.SharpBicubic().scale(clip, width=1280, height=720)

Of course, there is also a generic Bicubic class should you want to assign the values manually.

.. code-block:: py

    kernels.Bicubic(b=0, c=1).scale(clip, width=1280, height=720)

This allows for easy customizability, and every kernel can be given unique parameters if required.

.. code-block:: py

    kernels.Bicubic(b=0, c=0.5)
    kernels.Lanczos(taps=3)
    kernels.Impulse(impulse, oversample=8, taps=1)

Using this interface allows for consistency, which makes supporting a wide array of kernels in your own function very simple.

Supporting Kernels in Your Own Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kernels are very flexible, so if you want to use them as-is, they're simple enough to add. However, you should also consider newer users and their inexperience with Kernels, but potential exposure to abusing strings for "presets".

With that in mind, we believe the most optimal method to implement kernels is by allowing your function to accept both a `Kernel` object and a string. This allows users who want to make full use of kernels to do so while not making it any harder for newer users to rely on strings.

Below is some example code for implementing kernel support into a simple descaling function:

.. code-block:: py

    from lvsfunc.kernels import Kernel, get_kernel

    def descale(clip: vs.VideoNode,
                width: int = 1280, height: int = 720,
                kernel: Kernel | str = 'bicubic') -> vs.VideoNode:
        """A simple descaling function"""

        if isinstance(kernel, str):
            kernel = get_kernel(kernel)()

        descaled_clip = kernel.descale(clip, width, height)
        return descaled_clip

Which in turn allows users to call the function in multiple ways:

.. code-block:: py

    import lvsfunc as lvf

    example1 = descale(clip, 1280, 720, lvf.kernels.Bicubic())
    example2 = descale(clip, 1280, 720, 'bicubic')

Easy as pie!

Methods
^^^^^^^

Every `Kernel` class comes with a set of methods:

.. autoclass:: lvsfunc.kernels.Example.scale
    :members:

.. autoclass:: lvsfunc.kernels.Example.descale
    :members:

.. autoclass:: lvsfunc.kernels.Example.shift
    :members:

.. autoclass:: lvsfunc.kernels.Example.resample
    :members:

All Available Kernels
^^^^^^^^^^^^^^^^^^^^^

.. automodule:: lvsfunc.kernels
    :members:
    :show-inheritance:
    :exclude-members: Example
