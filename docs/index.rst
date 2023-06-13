======================
agate-lookup |release|
======================

.. include:: ../README.rst

Install
=======

To install:

.. code-block:: bash

    pip install agate-lookup

For details on development or supported platforms see the `agate documentation <https://agate.readthedocs.org>`_.

Import
======

agate-lookup is an agate `extension <https://agate.readthedocs.org/en/latest/extensions.html>`_. To use it, first import it and patch its functionality into agate:

.. code-block:: python

  import agate
  import agatelookup

Importing agate-lookup adds methods to :class:`agate.Table <agate.table.Table>`.

Basic lookup
============

agate-lookup allows you to join your tables to data from the `lookup <https://github.com/wireservice/lookup>`_ project. The basic mechanism for doing this is the :meth:`.TableLookup.lookup` method. For example, if you have this table:

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

    joined = table.lookup('postal', 'state', lookup_key='usps')

Multi-column lookup
===================

Some lookup tables have multiple key columns, for example :code:`year` and :code:`month`. To join to a table like this, pass a sequence of column names as the first argument. For example, consider this table:

+-------+-------+
|  usps | year  |
+=======+=======+
|  AZ   | 1985  |
+-------+-------+
|  WY   | 2014  |
+-------+-------+
|  SC   | 1994  |
+-------+-------+

We can join the population of the state for each year with this code:

.. code-block:: python

    joined = table.lookup(['usps', 'year'], 'population')

+-------+------+-------------+
|  usps | year | population  |
+=======+======+=============+
|  AZ   | 1985 |  3,183,538  |
+-------+------+-------------+
|  WY   | 2014 |    584,153  |
+-------+------+-------------+
|  SC   | 1994 |  3,705,397  |
+-------+------+-------------+

Versioned lookup
================

Some lookup tables have several versions. For example, the NAICS business code classification is revised every 5 years. You can also select a particular version of the lookup table using the :code:`version` argument. To join the :code:`2012` edition of the NAICS codes, you would run:

.. code-block:: python

    joined = table.lookup('naics', 'description', version='2012')

Fetch a table without joining
=============================

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

Using a custom repository
=========================

By default, agate-lookup will use the `wireservice/lookup <https://github.com/wireservice/lookup>`_ repository of lookup tables. Look there to see what key/value combinations and versions you can use with lookup.

You can specify your own repository of lookup tables by constructing an instance of :class:`.Source` and passing it into the :meth:`.TableLookup.lookup` method.

Caching
=======

Lookup tables are cached each time they are downloaded. The default cache location is :code:`~/lookup`. In order to ensure you have the latest version, tables are redownloaded each time that they are used, unless a network connection can not be made. If there is a connection issue, the cached copy will be read from disk.

You can override the default caching location by creating a custom :class:`Source` and passing the :code:`cache` argument.

API
===

.. autofunction:: agatelookup.table.lookup

.. autofunction:: agatelookup.table.from_lookup

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
