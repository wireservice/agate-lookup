#!/usr/bin/env python
# -*- coding: utf8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import agate
import agatelookup

agatelookup.patch()

class TestSource(agate.AgateTestCase):
    def setUp(self):
        self.source = agatelookup.Source()

    def test_get_table(self):
        table = self.source.get_table('usps', 'state')

        self.assertColumnNames(table, ['usps', 'state'])
        self.assertColumnTypes(table, [agate.Text, agate.Text])
