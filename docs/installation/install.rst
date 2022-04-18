Basic Installation
------------------

There are two common ways to install lvsfunc.

The first is to install it through `pypi <https://pypi.org/project/lvsfunc/>`_. You can install it through pip, as demonstrated below::

    $ pip3 install lvsfunc --no-cache-dir --upgrade

This ensures that any previous versions will be overwritten and lvsfunc will be upgraded if already installed.

The second way is to build the latest version. This is considered a lot more unstable, but will feature the most up-to-date functions, as well as accurately reflect the documentation.::

    $ python3 -m pip install --no-cache-dir --upgrade git+https://github.com/Irrational-Encoding-Wizardry/lvsfunc.git -U

Please be careful with installing lvsfunc through any other means, such as by downloading a fatpack or using vsrepo, as these may feature outdated versions.

If you continually run into issues loading lvsfunc, please double check your `site-packages` directory and make sure to delete the `lvsfunc.py` file if it's present. This may have accidentally been installed through a fatpack or an outdated manager.
