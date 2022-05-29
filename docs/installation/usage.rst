Basic Usage
-----------

`lvsfunc` is a Python module,
meaning it must be imported into your script before it can be accessed.
You can import it by doing the following:

.. code-block:: py

    import lvsfunc

Simple, right?
But writing "lvsfunc" every time is cumbersome,
so we recommend you give it an alias.

.. code-block:: py

    import lvsfunc as lvf

.. note::

    The rest of the documentation will assume you alias `lvsfunc` as `lvf`.

With the module now imported,
you can call functions in your script by referencing the module
and writing a function name behind it.

.. code-block:: py

    import lvsfunc as lvf

    clip = lvf.source("PATH/TO/YOUR/VIDEO")

`lvsfunc` exposes every function in the global scope,
but also exposes every submodule individually.
Both of the following calls will call the same function:

.. code-block:: py

    import lvsfunc as lvf

    descaled_clip_a = lvf.descale(clip)
    descaled_clip_b = lvf.scale.descale(clip)

Calling them from the relevant submodule is considered good practice,
but for convenience, it may be easier to call the function directly.

You can also import individual functions from submodules.

.. code-block:: py

    from lvsfunc.noise import chickendream

    upscaled_clip = chickendream(clip)

This is useful if you only need a single function and don't want to pollute your autocompletion
with all the other `lvsfunc` functions.

For further information about specific functions, please refer to their individual documentations.
You can find them by scouring the "functions" pages to the left, or using the search bar.
