#!/usr/bin/env python

import os

import agate

def default_url_func(root, key):
    return os.path.join(root, key)

class Source(object):
    """
    Allows for fast access to respository of remote datasets with a known path
    structure.
    """
    def __init__(self, root, url_func=default_url_func, callback=agate.Table.from_csv):
        self._root = root
        self._url_func = url_func
        self._callback = callback

        if not hasattr(agate.Table, 'from_url'):
            raise AttributeError('Table.lookup is missing. Did you forget to run agatelookup.patch()?')

    def get_table(self, key):
        url = self._url_func(self._root, key)

        return agate.Table.from_url(url, callback=self._callback)
