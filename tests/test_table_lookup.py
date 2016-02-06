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
            ('WA',),
            ('VA',),
            ('TX',)
        )

        self.column_names = ['usps']
        self.column_types = [agate.Text()]

        self.table = agate.Table(self.rows, self.column_names, self.column_types)
        self.source = agatelookup.Source()

    def test_lookup(self):
        result = self.table.lookup(self.source, 'usps', 'state')

        self.assertColumnNames(result, ['usps', 'state'])
        self.assertColumnTypes(result, [agate.Text, agate.Text])

        self.assertSequenceEqual(result.rows[1].values(), ['VA', 'Virginia'])
