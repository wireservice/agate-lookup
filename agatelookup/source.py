#!/usr/bin/env python

import agate
import agateremote
import requests
import yaml

agateremote.patch()

def default_table_url_func(root, keys, value, version=None):
    """
    Default function for converting lookup table data into a table URL.
    """
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    url = '%s/%s/%s' % (root, keys, value)

    if version:
        url += '.%s' % version

    url += '.csv'

    return url

def default_metadata_url_func(root, keys, value, version=None):
    """
    Default method of converting lookup table data into a metadata file url.
    """
    if isinstance(keys, (list, tuple)):
        keys = '/'.join(keys)

    url = '%s/%s/%s' % (root, keys, value)

    if version:
        url += '.%s' % version

    url += '.csv.yml'

    return url

def make_type_tester(meta):
    """
    Uses parsed lookup table metadata to create a :class:`.agate.TypeTester`
    that will always use correct types for the table columns. (And avoid
    the overhead of type inference.)
    """
    force = {}

    for k, v in meta['columns'].items():
        force[k] = getattr(agate, v)()

    return agate.TypeTester(force=force)

class Source(object):
    """
    A reference to an archive of lookup tables. This is a remote location with
    lookup table and metadata files at a known path structure.

    :param root:
        The root URL to prefix all data and metadata paths.
    :param table_url_func:
        A function that takes table metadata and returns an absolute URL to
        that table's data file. See :func:`default_table_url_func`.
    :param metadata_url_func:
        A function that takes table metadata and returns an absolute URL to
        that table's data file. See :func:`default_metadata_url_func`.
    :param callback:
        A function that translates the remote data table into an agate table.
        Typically this is :meth:`.agate.Table.from_csv`, but it could also be
        :meth:`.agate.Table.from_json` or a method provided by an extension.
    """
    def __init__(self, root='http://wireservice.github.io/lookup', table_url_func=default_table_url_func, metadata_url_func=default_metadata_url_func, callback=agate.Table.from_csv):
        self._root = root
        self._table_url_func = table_url_func
        self._metadata_url_func = metadata_url_func
        self._callback = callback

    def get_metadata(self, keys, value, version=None):
        """
        Fetches metadata related to a specific lookup table.

        See :meth:`Source.get_table` for parameter details.
        """
        url = self._metadata_url_func(self._root, keys, value, version)
        r = requests.get(url)

        try:
            data = yaml.load(r.text)
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

        url = self._table_url_func(self._root, keys, value, version)

        if agate.utils.issequence(keys):
            row_names = lambda r: tuple(r[k] for k in keys)
        else:
            row_names = keys

        return agate.Table.from_url(url, column_types=tester, row_names=row_names, callback=self._callback)
