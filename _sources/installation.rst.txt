.. highlight:: shell

============
Installation
============


Stable release
--------------

To install orsopy, run this command in your terminal:

.. code-block:: console

    $ pip install EasyReflectometry

This is the preferred method to install EasyReflectometry, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Developer Instrutions
---------------------

Clone the public repository:

.. code-block:: console

    $ git clone git://github.com/easyScience/EasyReflectometryLib

And install the latest developer version with:

.. code-block:: console

    $ cd EasyReflectometryLib
    $ git checkout develop
    $ pip install -e ".[dev]"
