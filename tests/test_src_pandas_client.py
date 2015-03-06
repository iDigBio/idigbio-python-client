import unittest
import pandas

from idigbio.pandas_client import iDbApiPandas

class TestIDbApiPandas(unittest.TestCase):
    def test___init__(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)

    def test_search_media(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_media()
        self.assertIsInstance(df,pandas.DataFrame)

    def test_search_records(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_records()
        self.assertIsInstance(df,pandas.DataFrame)

    def test_search_records_limit_10000(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_records(limit=10000)
        self.assertIsInstance(df,pandas.DataFrame)
        self.assertEquals(df.shape[0],10000)

if __name__ == '__main__':
    unittest.main()
