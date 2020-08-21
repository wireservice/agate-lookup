#!/usr/bin/env python

import io
import os

import agate
import six
import requests
import yaml

def make_table_path(keys, value, version=None):
    """
    Generate a path to find a given lookup table.
    """
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    path = '%s/%s' % (keys, value)

    if version:
        path += '.%s' % version

    path += '.csv'

    return path

def make_metadata_path(keys, value, version=None):
    """
    Generate a path to find a given lookup table.
    """
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    path = '%s/%s' % (keys, value)

    if version:
        path += '.%s' % version

    path += '.csv.yml'

    return path

def make_type_tester(meta):
    """
    Uses parsed lookup table metadata to create a :class:`.agate.TypeTester`
    that will always use correct types for the table columns. (And avoid
    the overhead of type inference.)
    """
    force = {}

    for k, v in meta['columns'].items():
        force[k] = getattr(agate, v['type'])()

    return agate.TypeTester(force=force)

class Source(object):
    """
    A reference to an archive of lookup tables. This is a remote location with
    lookup table and metadata files at a known path structure.

    :param root:
        The root URL to prefix all data and metadata paths.
    :param cache:
        A path in which to store cached copies of any tables that are used, so
        they can continue to be used offline.
    """
    def __init__(self, root='http://wireservice.github.io/lookup', cache='~/.lookup'):
        self._root = root
        self._cache = os.path.expanduser(cache) if cache else None

    def _read_cache(self, path):
        """
        Read a file from the lookup cache.
        """
        if self._cache:
            cache_path = os.path.join(self._cache, path)

            if os.path.exists(cache_path):
                with io.open(cache_path, encoding='utf-8') as f:
                    text = f.read()

                return text

        raise RuntimeError('Unable to download remote file "%s" and local cache is not available.' % path)

    def _write_cache(self, path, text):
        """
        Write a file to the lookup cache.
        """
        if self._cache:
            cache_path = os.path.join(self._cache, path)

            folder = os.path.split(cache_path)[0]

            if not os.path.exists(folder):
                os.makedirs(folder)

            with io.open(cache_path, 'w', encoding='utf-8') as f:
                f.write(text)

    def get_metadata(self, keys, value, version=None):
        """
        Fetches metadata related to a specific lookup table.

        See :meth:`Source.get_table` for parameter details.
        """
        path = make_metadata_path(keys, value, version)
        url = '%s/%s' % (self._root, path)

        try:
            r = requests.get(url)
            text = r.text

            self._write_cache(path, text)
        except (requests.ConnectionError, requests.Timeout):
            text = self._read_cache(path)

        try:
            data = yaml.load(text)
        except:
            raise ValueError('Failed to read or parse YAML at %s' % url)

        return data

    def get_table(self, keys, value, version=None):
        """
        Fetches and creates and agate table from a specified lookup table.

        The resulting table will automatically have row names created for the
        key columns, thus allowing it to be used as a lookup.

        :param keys:
            Either a single string or a sequence of keys that identify the
            "left side" of the table. For example :code:`'fips'` or
            :code:`['city', 'year']`.
        :param value:
            The value that is being looked up from the given keys. For example
            :code:`'state'` or :code:`'population'`.
        :param version:
            An optional version of the given lookup, if more than one exists.
            For instance :code:`'2007'` for the 2007 edition of the NAICS codes
            or :code:`'2012'` for the 2012 version.
        """
        meta = self.get_metadata(keys, value, version)
        tester = make_type_tester(meta)

        path = make_table_path(keys, value, version)
        url = '%s/%s' % (self._root, path)

        if agate.utils.issequence(keys):
            row_names = lambda r: tuple(r[k] for k in keys)
        else:
            row_names = keys

        try:
            r = requests.get(url)
            text = r.text

            self._write_cache(path, text)
        except (requests.ConnectionError, requests.Timeout):
            text = self._read_cache(path)

        return agate.Table.from_csv(six.StringIO(text), column_types=tester, row_names=row_names)
