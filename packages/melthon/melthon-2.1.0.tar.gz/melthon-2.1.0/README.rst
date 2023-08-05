========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |requires|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/python-melthon/badge/?style=flat
    :target: https://readthedocs.org/projects/python-melthon
    :alt: Documentation Status

.. |requires| image:: https://requires.io/github/JenswBE/python-melthon/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/JenswBE/python-melthon/requirements/?branch=master

.. |version| image:: https://img.shields.io/pypi/v/melthon.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/melthon

.. |commits-since| image:: https://img.shields.io/github/commits-since/jenswbe/python-melthon/v2.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/jenswbe/python-melthon/compare/v2.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/melthon.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/melthon

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/melthon.svg
    :alt: Supported versions
    :target: https://pypi.org/project/melthon

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/melthon.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/melthon


.. end-badges

Minimalistic static site generator

* Free software: GNU GPLv3 license

Installation
============

Use Docker (preferred way)::

    # --rm           : Remove container after execution
    # -u ${UID}      : Run container as current user
    # -v"$(pwd):/src": Make source and output accessible inside container
    docker run --rm -u ${UID} -v"$(pwd):/src" jenswbe/melthon

Use pip::

    pip install melthon

Documentation
=============


https://python-melthon.readthedocs.io/
