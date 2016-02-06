#!/usr/bin/env python

import agate
import agateremote
import six

agateremote.patch()

def default_url_func(root, keys, value):
    return '%s/%s/%s.csv' % (root, '/'.join(keys), value)

class Source(agateremote.Archive):
    """
    TKTK
    """
    def __init__(self, root='https://github.com/onyxfish/lookup/raw/master', url_func=default_url_func, callback=agate.Table.from_csv):
        super(Source, self).__init__(root, url_func, callback)

    def get_table(self, keys, value):
        if isinstance(keys, six.string_types):
            keys = [keys]

        url = self._url_func(self._root, keys, value)

        return agate.Table.from_url(url, callback=self._callback)
