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

If your table has different keys from the lookup table, you can specify them using the :code:`table_key` argument. For example, if your table had the column name :code:`postal` then you could achieve the same result by running:

.. code-block:: python

    joined = table.lookup('usps', 'state', 'postal')

You can also select a particular version of the lookup table using the :code:`version` argument. For example, to join the :code:`2012` edition of the NAICS codes, you would run:

.. code-block:: python

    joined = table.lookup('naics', 'description', version='2012')

By default, agate-lookup will use the `wireservice/lookup <https://github.com/wireservice/lookup>`_ repository of lookup tables. Look there to see what key/value combinations and versions you can use with lookup.

You can specify your own repository of lookupt ables by constructing an instance of :class:`.Source` and passing it into the :meth:`.TableLookup.lookup` method.

You can also fetch a lookup table without joining it. For example, to get the Consumer Price Index by year and month:

.. code-block:: python

    cpi = agate.Table.from_lookup(['year', 'month'], 'cpi')

+-------+-------+--------+
|  year | month |   cpi  |
+=======+=======+========+
|  1947 | 1     | 21.48  |
+-------+-------+--------+
|  1947 | 2     | 21.62  |
+-------+-------+--------+
|  1947 | 3     | 22.00  |
+-------+-------+--------+
|  ...  | ...   |   ...  |
+-------+-------+--------+

Lookup tables automatically have :code:`row_names` assigned. In this case the row names are a tuple of :code:`(year, month)`. We can use this to quickly calculate inflation-adjusted prices in another table.

.. code-block:: python

    BASE_CPI = cpi.rows[('2015', '12')]['cpi']

    deflator = lambda r: r['price'] * cpi.rows[(r['year'], r['month'])]['cpi'] / BASE_CPI)

    adjusted = table.compute([
        ('real_price', agate.Formula(agate.Number(), deflator)
    ])

The :code:`adjusted` table will now have a :code:`real_price` column with prices in December, 2015 dollars.

Caching
=======

Lookup tables are cached each time they are downloaded. The default cache location is :code:`~/lookup`. In order to ensure you have the latest version, tables are redownloaded each time that they are used, unless a network connection can not be made. If there is a connection issue, the cached copy will be read from disk.

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
