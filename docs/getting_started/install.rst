============
Installation
============

.. _install:

.. important::

    | If you have trouble calling lvsfunc functions, double-check that you're not loading in **lvsfunc.py**!
    | If you are, delete it from your `site-packages` and it should work properly.

There are two common ways to install lvsfunc.

The first is to install the latest release build through `pypi <https://pypi.org/project/lvsfunc/>`_.
You can use pip to do this, as demonstrated below:


.. code-block:: console

    pip3 install lvsfunc --no-cache-dir -U

This ensures that any previous versions will be overwritten
and lvsfunc will be upgraded if you had already previously installed it.

The second method is to build the latest version from git.
This will be less stable,
but will feature the most up-to-date features,
as well as accurately reflect the documentation.

.. code-block:: console

    pip3 install git+https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git --no-cache-dir -U

It's recommended you use a release version over building from git
unless you require new functionality only available upstream.
