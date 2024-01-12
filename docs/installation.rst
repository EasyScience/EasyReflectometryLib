.. highlight:: shell

============
Installation
============


Stable release
--------------

To install EasyReflectometry, run this command in your terminal:

.. code-block:: console

    $ pip install git+https://github.com/easyScience/EasyReflectometryLib.git

This is the preferred method to install EasyReflectometry, soon EasyReflectometry will also be available on PyPI.

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
    $ pip install -r requirements-dev.txt
    $ pip install -e .
