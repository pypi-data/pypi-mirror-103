====================================================
exconfig: Create and configure input parameter files
====================================================

.. image:: https://img.shields.io/travis/mcflugen/exconfig.svg
        :target: https://travis-ci.org/mcflugen/exconfig

.. image:: https://ci.appveyor.com/api/projects/status/380ox1dv8hekefq9?svg=true
    :target: https://ci.appveyor.com/project/mcflugen/exconfig/branch/master

.. image:: https://readthedocs.org/projects/exconfig/badge/?version=latest
        :target: https://exconfig.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

About
-----

*exconfig* is a Python library for working with input parameter files. It
provides parameter description and validation, as well as ways of working
with various file formats.


Requirements
------------

*exonfig* requires Python 3.

Apart from Python, *exconfig* has a number of other requirements, all of which
can be obtained through either *pip* or *conda*, that will be automatically
installed when you install *exconfig*.

To see a full listing of the requirements, have a look at the project's
*requirements.txt* file.

If you are a developer of *exconfig* you will also want to install
additional dependencies for running *exconfig*'s tests to make sure
that things are working as they should. These dependencies are listed
in *requirements-testing.txt*.

Installation
------------

Stable Release
++++++++++++++

*exconfig*, and its dependencies, can be installed either with *pip*
or *conda*. Using *pip*::

    $ pip install exconfig

Using *conda*::

    $ conda install exconfig -c conda-forge

From Source
+++++++++++

After downloading the *exconfig* source code, run the following from
*exconfig*'s top-level folder (the one that contains *setup.py*) to
install *exconfig* into the current environment::

  $ pip install -e .
