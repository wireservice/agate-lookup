#!/usr/bin/env python

"""
This module contains the Lookup extension to :class:`Table <agate.table.Table>`.
"""

import agateremote
import six

agateremote.patch()

class TableLookup(object):
    def lookup(self, source, source_keys, value, table_keys=None):
        """
        TKTK
        """
        table = source.get_table(source_keys, value)

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

        return self.join(table, left_key, right_key)
