==========
Quickstart
==========

.. _quickstart:

lvsfunc is a Python package for `VapourSynth <http://www.vapoursynth.com/>_` scripting.
It contains a multitude of useful functions for video filtering, VapourSynth-script developing, and image processing.


Prerequisites
=============

lvsfunc requires the following programs:

* `Python 3.10 or higher <https://www.python.org/>`_
* `VapourSynth R59 or above <http://www.vapoursynth.com/>`_
* vsrepo *(Optional, can be installed along with VapourSynth)*


Usage Instructions
==================

1. Install the :ref:`prequisites <install>`
2. Install lvsfunc through pip

.. code-block:: console

    pip3 install lvsfunc --no-cache-dir -U

3. Install additional dependencies via vsrepo or manual installation
4. Open your VapourSynth script and import lvsfunc

.. code-block:: python

    import vapoursynth as vs
    import lvsfunc as lvf

    core = vs.core

5. Call functions as necessary

.. code-block:: python

    src = lvf.misc.source("C:/PATH/TO/VIDEO.mkv")

.. important::

    lvsfunc offers basic support to help install most of the required external filters.
    Simply run the following command in your terminal: ``python3 -m lvsfunc``

If you encounter any issues during this process,
double-check you have installed all the required :ref:`prequisites <install>`.

.. important::

    If you have trouble calling lvsfunc functions,
    double-check that you're not loading in the old **lvsfunc.py**!
    If you are, delete it from your ``site-packages`` and it should work properly.
