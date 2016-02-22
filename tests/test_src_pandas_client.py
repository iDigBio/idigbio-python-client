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

    def test_search_records_limit_10007(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_records(limit=10007)
        self.assertIsInstance(df,pandas.DataFrame)
        self.assertEqual(len(df),10007)

    def test_count_media(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.count_media()
        self.assertIsInstance(df,int)

    def test_count_records(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.count_records()
        self.assertIsInstance(df,int)

    # TODO
    # def test_datehist(self):
    #     # i_db_api_pandas = iDbApiPandas(env, debug)
    #     # self.assertEqual(expected, i_db_api_pandas.datehist(**kwargs))
    #     assert False # TODO: implement your test here

    # def test_stats(self):
    #     # i_db_api_pandas = iDbApiPandas(env, debug)
    #     # self.assertEqual(expected, i_db_api_pandas.stats(t, **kwags))
    #     assert False # TODO: implement your test here

    def test_top_media(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_media()
        self.assertIsInstance(df,pandas.DataFrame)

    def test_top_records(self):
        api = iDbApiPandas()
        self.assertIsNotNone(api)
        df = api.search_media()
        self.assertIsInstance(df,pandas.DataFrame)

if __name__ == '__main__':
    unittest.main()
