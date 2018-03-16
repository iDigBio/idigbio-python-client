import unittest
import os
import sys

from idigbio.json_client import iDbApiJson, ImagesDisabledException

try:
    import mock as mock_module
except ImportError:
    try:
        import unittest.mock as mock_module
    except ImportError:
        mock_module = None

if mock_module:
    Mock = mock_module.Mock
    MagicMock = mock_module.MagicMock
    patch = mock_module.patch

class TestIDbApiJson(unittest.TestCase):
    def test___init__(self):
        api = iDbApiJson()
        self.assertIsNotNone(api.s)

    def test___del__(self):
        api = iDbApiJson()
        del api

    def test_create_map(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)

    def test_search_media(self):
        api = iDbApiJson()
        r = api.search_media()
        self.assertIsNotNone(r)

    def test_search_records(self):
        api = iDbApiJson()
        r = api.search_records()
        self.assertIsNotNone(r)

    def test_view(self):
        api = iDbApiJson()
        r = api.view("records","56c351b5-30c0-4529-a57f-60c451cc5876")
        self.assertIsNotNone(r)

    def test_count_media(self):
        api = iDbApiJson()
        r = api.count_media()
        self.assertIsNotNone(r)
        self.assertIsInstance(r,int)
        self.assertNotEqual(r,0)

    def test_count_media_null(self):
        api = iDbApiJson()
        r = api.count_media(mq={"version": -1})
        self.assertIsNotNone(r)
        self.assertIsInstance(r,int)
        self.assertEqual(r,0)

    def test_count_records(self):
        api = iDbApiJson()
        r = api.count_records()
        self.assertIsNotNone(r)
        self.assertIsInstance(r,int)
        self.assertNotEqual(r,0)

    def test_count_records_null(self):
        api = iDbApiJson()
        r = api.count_records(rq={"version": -1})
        self.assertIsNotNone(r)
        self.assertIsInstance(r,int)
        self.assertEqual(r,0)

    def test_count_recordsets(self):
        api = iDbApiJson()
        r = api.count_recordsets()
        self.assertIsNotNone(r)
        self.assertIsInstance(r,int)
        self.assertNotEqual(r,0)

    def test_datehist(self):
        api = iDbApiJson()
        r = api.datehist(
            rq={"scientificname": "puma concolor"},
            top_fields=["institutioncode"],
            min_date="2005-01-01")
        self.assertIsNotNone(r)

    def test_stats_api(self):
        api = iDbApiJson()
        r = api.stats("api", min_date="2005-01-01")
        self.assertIsNotNone(r)

    def test_stats_digest(self):
        api = iDbApiJson()
        r = api.stats("digest", min_date="2005-01-01")
        self.assertIsNotNone(r)

    def test_stats_search(self):
        api = iDbApiJson()
        r = api.stats("search", min_date="2005-01-01")
        self.assertIsNotNone(r)

    def test_top_media(self):
        api = iDbApiJson()
        r = api.top_media()
        self.assertIsNotNone(r)

    def test_top_records(self):
        api = iDbApiJson()
        r = api.top_records()
        self.assertIsNotNone(r)

    def test_upload(self):
        if mock_module is None:
            self.skipTest('mock library not installed')
        api = iDbApiJson(user="foo", password="bar")
        api._api_post = Mock()
        api.upload('testreference', __file__)
        args, kwargs = api._api_post.call_args
        self.assertIn("/v2/media", args)
        self.assertIn('files', kwargs)
        self.assertIn('params', kwargs)
        self.assertIn('etag', kwargs['params'])
        self.assertIsNotNone(kwargs['params']['etag'])

if __name__ == '__main__':
    unittest.main()
