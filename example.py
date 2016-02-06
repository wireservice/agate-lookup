#!/usr/bin/env python

import agate
import agatelookup

agatelookup.patch()

source = agatelookup.Source()

table = agate.Table([
    ('WA',),
    ('VA',),
    ('NE',)
], ['usps'])

joined = table.lookup(source, 'usps', 'state')

joined.print_table()
