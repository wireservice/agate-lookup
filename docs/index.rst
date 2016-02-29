======================
agate-lookup |release|
======================

.. include:: ../README.rst

Install
=======

To install:

.. code-block:: bash

    pip install agatelookup

For details on development or supported platforms see the `agate documentation <http://agate.readthedocs.org>`_.

Usage
=====

agate-lookup is an agate extension. To use it, first import it and patch its functionality into agate:

.. code-block:: python

  import agate
  import agatelookup

  agatelookup.patch()

Calling :func:`.patch` attaches all the methods of :class:`.Tablelookup` to :class:`agate.Table <agate.table.Table>`.

After that, you simply use the :meth:`.TableLookup.lookup` method on your table, passing in the number of the columns to match on and the value you wish to lookup. For example, if you have this table:

+---------+------+
| company | usps |
+=========+======+
| Walmart | AR   |
+---------+------+
| Exxon   | TX   |
+---------+------+
| Chevron | CA   |
+---------+------+

You could add the state name to the table by running:

.. code-block:: python

    joined = table.lookup('usps', 'state')

The resulting table would be:

+---------+------+------------+
| company | usps | state      |
+=========+======+============+
| Walmart | AR   | Arkansas   |
+---------+------+------------+
| Exxon   | TX   | Texas      |
+---------+------+------------+
| Chevron | CA   | California |
+---------+------+------------+

If your table has different keys from the lookup table, you can specify them using the :code:`table_keys` keyword argument. You can also select a particular version of the lookup table using the :code:`version` argument.

By default, agate-lookup will use the `wireservice/lookup <https://github.com/wireservice/lookup>`_ repository of lookup tables. Look there to see what key/value combinations and versions you can use with lookup.

You can also specify your own repository of lookupt ables by constructing an instance of :class:`.Source` and passing it into the :meth:`.TableLookup.lookup` method.

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
