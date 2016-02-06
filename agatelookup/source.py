#!/usr/bin/env python

import agate
import agateremote
import random
import requests
import six
import yaml

agateremote.patch()

# TKTK: host file somewhere we won't need cache busters

def default_table_url_func(root, keys, value, version=None):
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    url = '%s/%s/%s' % (root, keys, value)

    if version:
        url += '.%s' % version

    url += '.csv?%s' % str(random.randrange(0, 9999))

    return url

def default_metadata_url_func(root, keys, value, version=None):
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    url = '%s/%s/%s' % (root, keys, value)

    if version:
        url += '.%s' % version

    url += '.csv.yml?%s' % str(random.randrange(0, 9999))

    return url

def make_type_tester(meta):
    force = {}

    for k, v in meta['columns'].items():
        force[k] = getattr(agate, v)()

    return agate.TypeTester(force=force)

class Source(object):
    """
    TKTK
    """
    def __init__(self, root='https://github.com/onyxfish/lookup/raw/master', table_url_func=default_table_url_func, metadata_url_func=default_metadata_url_func, callback=agate.Table.from_csv):
        self._root = root
        self._table_url_func = table_url_func
        self._metadata_url_func = metadata_url_func
        self._callback = callback

    def get_metadata(self, keys, value, version=None):
        url = self._metadata_url_func(self._root, keys, value, version)
        r = requests.get(url)

        return yaml.load(r.text)

    def get_table(self, keys, value, version=None):
        meta = self.get_metadata(keys, value, version)
        tester = make_type_tester(meta)

        url = self._table_url_func(self._root, keys, value, version)

        return agate.Table.from_url(url, column_types=tester, callback=self._callback)
