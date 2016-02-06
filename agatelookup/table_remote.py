#!/usr/bin/env python

"""
This module contains the Remote extension to :class:`Table <agate.table.Table>`.
"""

import agate
import agateremote
import six

agateremote.patch()

class TableSource(object):
    pass
