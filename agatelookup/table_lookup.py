#!/usr/bin/env python

"""
This module contains the Lookup extension to :class:`Table <agate.table.Table>`.
"""

import agateremote
import six

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
            The key (string) or keys (sequence) in the lookup table to be
            matched. For example :code:`'naics'` or :code:`['city', 'year']`.
        :param value:
            The value that is being looked up. For example :code:`'description'`
            or :code:`'population'`. This is the column that will be appended.
        :param table_keys:
            The keys in this table to match to the lookup table. This defaults
            the same values specified for `source_keys`, so it only needs
            to be specified if the column names in this table don't match.
        :param version:
            An optional version of the lookup to use, if more than one exists.
            For instance :code:`'2007'` for the 2007 edition of the NAICS codes
            or :code:`'2012'` for the 2012 version.
        """
        table = source.get_table(source_keys, value, version)

        if not table_keys:
            table_keys = source_keys

        if not isinstance(table_keys, six.string_types):
            left_key = lambda r: (r[k] for k in table_keys)
        else:
            left_key = table_keys

        if not isinstance(source_keys, six.string_types):
            right_key = lambda r: (r[k] for k in source_keys)
        else:
            right_key = source_keys

        # TKTK: the following keys were not matched: ...

        return self.join(table, left_key, right_key)
