#!/usr/bin/env python

import agate
import agateremote
import random
import requests
import six
import yaml

agateremote.patch()

# TKTK: host file somewhere we won't need cache busters

def default_url_func(root, keys, value):
    if isinstance(keys, six.string_types):
        keys = [keys]

    return '%s/%s/%s.csv' % (root, '/'.join(keys), value)

class Source(agateremote.Archive):
    """
    TKTK
    """
    def __init__(self, root='https://github.com/onyxfish/lookup/raw/master', url_func=default_url_func, callback=agate.Table.from_csv):
        super(Source, self).__init__(root, url_func, callback)

    def get_metadata(self, keys, value):
        url = '%s.yml' % self._url_func(self._root, keys, value) + '?' + str(random.randrange(0, 9999))

        r = requests.get(url)

        return yaml.load(r.text)

    def make_type_tester(self, meta):
        force = {}

        for k, v in meta.items():
            force[k] = getattr(agate, v)()

        return agate.TypeTester(force=force)

    def get_table(self, keys, value):
        meta = self.get_metadata(keys, value)
        tester = self.make_type_tester(meta)

        url = self._url_func(self._root, keys, value) + '?' + str(random.randrange(0, 9999))

        return agate.Table.from_url(url, column_types=tester, callback=self._callback)
