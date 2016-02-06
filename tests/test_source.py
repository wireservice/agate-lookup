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
    pass
