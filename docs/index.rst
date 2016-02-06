=====================
agate-lookup |release|
=====================

.. include:: ../README.rst

Install
=======

To install:

.. code-block:: bash

    pip install agatelookup

For details on development or supported platforms see the `agate documentation <http://agate.readthedocs.org>`_.

Usage
=====

agate-lookup uses a monkey patching pattern to add read for xls and xlsx files support to all :class:`agate.Table <agate.table.Table>` instances.

.. code-block:: python

  import agate
  import agatelookup

  agatelookup.patch()

Calling :func:`.patch` attaches all the methods of :class:`.Tablelookup` to :class:`agate.Table <agate.table.Table>`.

===
API
===

.. autofunction:: agatelookup.patch

.. autoclass:: agatelookup.table_lookup.TableLookup
    :members:

.. autoclass:: agatelookup.source.Source
    :members:

Authors
=======

.. include:: ../AUTHORS.rst

Changelog
=========

.. include:: ../CHANGELOG.rst

License
=======

.. include:: ../COPYING

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
