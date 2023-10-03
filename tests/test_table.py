from unittest.mock import patch

import agate
import requests

import agatelookup  # noqa: F401


class TestLookup(agate.AgateTestCase):
    def setUp(self):
        self._source = agatelookup.Source(cache=False)

    def test_lookup(self):
        rows = (
            ('WA',),
            ('VA',),
            ('TX',)
        )

        column_names = ['usps']
        column_types = [agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        result = table.lookup('usps', 'state', source=self._source)

        self.assertColumnNames(result, ['usps', 'state'])
        self.assertColumnTypes(result, [agate.Text, agate.Text])

        self.assertSequenceEqual(result.rows[1].values(), ['VA', 'Virginia'])

    def test_lookup_key(self):
        rows = (
            ('WA',),
            ('VA',),
            ('TX',)
        )

        column_names = ['postal']
        column_types = [agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        result = table.lookup('postal', 'state', lookup_key='usps', source=self._source)

        self.assertColumnNames(result, ['postal', 'state'])
        self.assertColumnTypes(result, [agate.Text, agate.Text])

        self.assertSequenceEqual(result.rows[1].values(), ['VA', 'Virginia'])

    def test_lookup_version(self):
        rows = (
            ('1111',),
            ('313320',),
            ('522310',)
        )

        column_names = ['naics']
        column_types = [agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        result = table.lookup('naics', 'description', version='2012', source=self._source)

        self.assertColumnNames(result, ['naics', 'description'])
        self.assertColumnTypes(result, [agate.Text, agate.Text])

        self.assertSequenceEqual(result.rows[1].values(), ['313320', 'Fabric Coating Mills'])

    def test_lookup_multiple_keys(self):
        rows = (
            ('AZ', '1985'),
            ('WY', '2014'),
            ('SC', '1994')
        )

        column_names = ['usps', 'year']
        column_types = [agate.Text(), agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        result = table.lookup(['usps', 'year'], 'population', source=self._source)

        self.assertColumnNames(result, ['usps', 'year', 'population'])
        self.assertColumnTypes(result, [agate.Text, agate.Text, agate.Number])

        self.assertSequenceEqual(result.rows[1].values(), ['WY', '2014', 584153])

    def test_lookup_no_match(self):
        rows = (
            ('WA',),
            ('VA',),
            ('FA',)
        )

        column_names = ['usps']
        column_types = [agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        result = table.lookup('usps', 'state', source=self._source)

        self.assertColumnNames(result, ['usps', 'state'])
        self.assertColumnTypes(result, [agate.Text, agate.Text])

        self.assertSequenceEqual(result.rows[2].values(), ['FA', None])

    def test_lookup_require_match(self):
        rows = (
            ('WA',),
            ('VA',),
            ('FA',)
        )

        column_names = ['usps']
        column_types = [agate.Text()]

        table = agate.Table(rows, column_names, column_types)

        with self.assertRaises(ValueError):
            table.lookup('usps', 'state', require_match=True, source=self._source)

    def test_from_lookup(self):
        table = agate.Table.from_lookup('usps', 'state')

        self.assertColumnNames(table, ['usps', 'state'])
        self.assertColumnTypes(table, [agate.Text, agate.Text])
        self.assertSequenceEqual(table.rows[1].values(), ['AK', 'Alaska'])

    def test_connection_fails(self):
        with patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = requests.ConnectionError

            with self.assertRaises(RuntimeError):
                agate.Table.from_lookup('usps', 'state', source=self._source)

    def test_cache(self):
        source = agatelookup.Source(cache='examples')

        with patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = requests.ConnectionError

            table = agate.Table.from_lookup('usps', 'state', source=source)

        self.assertColumnNames(table, ['usps', 'state'])
