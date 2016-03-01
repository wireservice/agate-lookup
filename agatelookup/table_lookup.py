#!/usr/bin/env python

"""
This module contains the Lookup extension to :class:`Table <agate.table.Table>`.
"""

import agateremote

from agatelookup.source import Source

agateremote.patch()

DEFAULT_SOURCE = Source()

class TableLookup(object):
    def lookup(self, source_keys, value, table_keys=None, version=None, source=None, require_match=False):
        """
        Fetch a lookup table from the remote source, matches it this table by
        its key columns, appends the value column and returns a new table
        instance.

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
        :param source:
            An instance of :class:`.Source` that defines where lookup tables
            are located. If not specified a default source will be used that
            points to the
            `wireservice/lookup <https://github.com/wireservice/lookup>`_
            repository.
        :param require_match:
            If :code:`True`, an exception will be raised if there is a value in
            this table with no matching entry in the lookup table.
        """
        if source is None:
            source = DEFAULT_SOURCE

        table = source.get_table(source_keys, value, version)

        return self.join(table, table_keys or source_keys, source_keys, require_match=require_match)

    @classmethod
    def from_lookup(cls, source_keys, value, version=None, source=None):
        """
        Fetch a lookup table, but don't join it to anything. See
        :meth:`.TableLookup.lookup` for arguments.
        """
        if source is None:
            source = DEFAULT_SOURCE

        return source.get_table(source_keys, value, version)
