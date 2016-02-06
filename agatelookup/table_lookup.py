#!/usr/bin/env python

"""
This module contains the Lookup extension to :class:`Table <agate.table.Table>`.
"""

import agateremote

agateremote.patch()

class TableLookup(object):
    def lookup(self, source, source_keys, value, table_keys=None, version=None):
        """
        Fetch a lookup table from the remote source, matches it this table by
        its key columns, appends the value column and returns a new table
        instance.

        :param source:
            An instance of :class:`.Source` that defines where lookup tables
            are located.
        :param source_keys:
            A column name or a sequence of such names to match in the lookup
            table. For example :code:`'naics'` or :code:`['city', 'year']`.
        :param value:
            The value that is being looked up. For example :code:`'description'`
            or :code:`'population'`. This is the column that will be appended.
        :param table_keys:
            A column name or a sequence of such names to match in this table.
            This defaults the same values specified for `source_keys`, so it
            only needs to be specified if the column names in this table don't
            match.
        :param version:
            An optional version of the lookup to use, if more than one exists.
            For instance :code:`'2007'` for the 2007 edition of the NAICS codes
            or :code:`'2012'` for the 2012 version.
        """
        table = source.get_table(source_keys, value, version)

        return self.join(table, table_keys or source_keys, source_keys)
