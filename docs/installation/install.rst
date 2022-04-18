Installation Instructions
-------------------------

.. important::

    | If you have trouble calling lvsfunc functions, double-check that you're not loading in **lvsfunc.py**!
    | If you are, delete it from your `site-packages` and it should work properly.

There are two common ways to install lvsfunc.

The first is to install it through `pypi <https://pypi.org/project/lvsfunc/>`_.
You can install it through pip, as demonstrated below


.. code-block:: console

    pip3 install lvsfunc --no-cache-dir --upgrade

This ensures that any previous versions will be overwritten
and lvsfunc will be upgraded if already installed.

The second way is to build the latest version.
This will be less stable,
but will feature the most up-to-date functions,
as well as accurately reflect the documentation.

.. code-block:: console

    python3 -m pip install --no-cache-dir --upgrade git+https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git -U
