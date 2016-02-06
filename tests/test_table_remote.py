#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate
import agatelookup

agatelookup.patch()

class TestLookup(agate.AgateTestCase):
    def setUp(self):
        self.rows = (
            (1, 'a', True, '11/4/2015', '11/4/2015 12:22 PM', '4:15'),
            (2, u'👍', False, '11/5/2015', '11/4/2015 12:45 PM', '6:18'),
            (None, 'b', None, None, None, None)
        )

        self.column_names = [
            'number', 'text', 'boolean', 'date', 'datetime', 'timedelta'
        ]

        self.column_types = [
            agate.Number(),
            agate.Text(),
            agate.Boolean(),
            agate.Date(),
            agate.DateTime(),
            agate.TimeDelta()
        ]

        self.table = agate.Table(self.rows, self.column_names, self.column_types)

    def test_lookup(self):
        [table = agate.Table.from_url('https://raw.githubusercontent.com/onyxfish/agate/master/examples/test.csv')

        self.assertColumnNames(table, self.table.column_names)
        self.assertColumnTypes(table, [agate.Number, agate.Text, agate.Boolean, agate.Date, agate.DateTime, agate.TimeDelta])

        self.assertRows(table, self.table.rows)
