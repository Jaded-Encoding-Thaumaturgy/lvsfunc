============
Quick Primer
============

.. _primer:

VapourSynth scripts are all written using Python. This includes lvsfunc.
To write a basic VapourSynth script, there are a couple fundamentals you must understand about Python.
This page is written to give you a very basic overview, as well as to explain some common terminology.

Before you begin, I highly encourage you read `this <https://wiki.python.org/moin/BeginnersGuide/NonProgrammers>`_ page.
This includes links to a lot of rudimentary Python exercises and learning material.

-----------
Basic usage
-----------

lvsfunc is a Python module,
which means you must import it into your script
before it can be accessed.
You can import it by doing the following:

.. code-block:: py

    import lvsfunc

Simple, right?
But writing "lvsfunc" every time is cumbersome,
so we recommend you give it an alias.

.. code-block:: py

    import lvsfunc as lvf

.. note::

    The rest of the documentation will assume you alias lvsfunc as `lvf`.

With the module now imported,
you can call functions in your script by referencing the module
and writing the function name behind it.

.. code-block:: py

    import lvsfunc as lvf

    clip = lvf.source("PATH/TO/YOUR/VIDEO")

lvsfunc exposes every function in the global scope,
but also exposes every sub-module individually.
Both of the following calls will call the same function:

.. code-block:: py

    import lvsfunc as lvf

    descaled_clip_a = lvf.descale(clip)  # global scope
    descaled_clip_b = lvf.scale.descale(clip)  # local scope

Calling them from the relevant sub-module is considered good practice,
but for convenience,
it may be easier to call the function
from the global scope instead.

You can also import individual functions from sub-modules.

.. code-block:: py

    from lvsfunc.noise import chickendream

    grained_clip = chickendream(clip)

This is useful if you only need a single function
and don't want to pollute your auto-completion
with all the other lvsfunc functions.

For further information about specific functions,
please refer to their individual documentation.
You can find them by scouring the :ref:`"filters" <_filters>` pages to the left,
or using the search bar.


------------------
Common terminology
------------------

The following video, programming, and VapourSynth-related terminology may be used throughout the documentation:

Functions
^^^^^^^^^

A `Python function <https://www.pythontutorial.net/python-basics/python-functions/>`_ is simply code that performs a specific task.
lvsfunc comes with a lot of functions that are written to handle with specific video artifacting,
and can be adjusted to help solve problematic issues with your video.

Kernel
^^^^^^

A *kernel* in VS lingo often refers to the setting used for a scaling operation.
A common example of this is `Bicubic <https://en.wikipedia.org/wiki/Bicubic_interpolation>`_.
lvsfunc makes extensive use of the `vskernels package <https://vskernels.encode.moe/en/latest/>`_
for most scaling and format-conversion related tasks.

A kernel, in essence, is simply a `class <https://www.pythontutorial.net/python-oop/python-class/>`_.
They must be used as such:

.. code-block:: python

    from vskernels import Bicubic

    kernel = Bicubic().scale()

The "Bicubic" that was imported is simply a preset that defines the base parameters for the scaling operation.
It can be further tweaked by changing the values as such:

.. code-block:: python

    kernel = Bicubic(b=0, c=1).scale()

As Bicubic is a class, it has `methods <https://www.pythontutorial.net/python-oop/python-methods/>`_.
These are the following:

.. code-block:: python

    Bicubic().scale()
    Bicubic().descale()
    Bicubic().resample()
    Bicubic().shift()

A lot of functions accept a Kernel object.
All you need to do is simply pass a Kernel you want to use to the function,
and it will use the methods as necessary internally.

.. code-block:: python

    lvf.a_function(clip, kernel=Bicubic())

If you run into a kernel-related error, you may need to simply pass the class, not an object!

.. code-block:: python

    lvf.a_function(clip, kernel=Bicubic)
