import agate

import agatelookup


class TestSource(agate.AgateTestCase):
    def setUp(self):
        self.source = agatelookup.Source()

    def test_get_metadata(self):
        meta = self.source.get_metadata('usps', 'state')

        self.assertIn('Census Bureau', meta['sources'][0])

    def test_get_table(self):
        table = self.source.get_table('usps', 'state')

        self.assertColumnNames(table, ['usps', 'state'])
        self.assertColumnTypes(table, [agate.Text, agate.Text])
        self.assertSequenceEqual(table.row_names[:2], ['AL', 'AK'])

    def test_get_table_multiple_keys(self):
        table = self.source.get_table(['year', 'month'], 'cpi.sa')
        print(table)

        self.assertColumnNames(table, ['year', 'month', 'cpi'])
        self.assertColumnTypes(table, [agate.Text, agate.Text, agate.Number])
        self.assertSequenceEqual(table.row_names[:2], [('1947', '1'), ('1947', '2')])
