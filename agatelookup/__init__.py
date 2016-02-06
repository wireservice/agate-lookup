#!/usr/bin/env python

from agatelookup.source import Source

def patch():
    """
    Patch the features of this library onto agate's core
    :class:`Table <agate.table.Table>` and
    :class:`TableSet <agate.tableset.TableSet>`.
    """
    import agate
    from agatelookup.table_lookup import TableLookup

    agate.Table.monkeypatch(TableLookup)
