import unittest
import os
import sys

from idigbio.json_client import iDbApiJson, ImagesDisabledException

class TestIDigBioMap(unittest.TestCase):
    def test___init__(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m._short_code)

    def test_definition(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.definition())

    def test_json_tile(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.json_tile(1,0,0))

    def test_png_tile(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.png_tile(1,0,0))

    def test_png_tile_disabled(self):
        api = iDbApiJson()
        m = api.create_map(disable_images=True)
        self.assertIsNotNone(m)
        with self.assertRaises(ImagesDisabledException):
            m.png_tile(1,0,0)

    def test_points(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.points(0,0,1))

    def test_save_map_image(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        m.save_map_image("test_map",1)
        self.assertTrue(os.path.exists("test_map.png"))
        os.unlink("test_map.png")

    def test_save_map_image_disabled(self):
        api = iDbApiJson()
        m = api.create_map(disable_images=True)
        self.assertIsNotNone(m)
        with self.assertRaises(ImagesDisabledException):
            m.save_map_image("test_map",1)
        self.assertFalse(os.path.exists("test_map.png"))

    def test_utf8grid_tile(self):
        api = iDbApiJson()
        m = api.create_map()
        self.assertIsNotNone(m)
        self.assertIsNotNone(m.utf8grid_tile(1,0,0))

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
        r = api.view("records","bc5510a4-4cc5-4731-a023-8827fdf58e61")
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

    def test_datehist(self):
        api = iDbApiJson()
        r = api.datehist()
        self.assertIsNotNone(r)

    def test_stats_api(self):
        api = iDbApiJson()
        r = api.stats("api")
        self.assertIsNotNone(r)

    def test_stats_digest(self):
        api = iDbApiJson()
        r = api.stats("digest")
        self.assertIsNotNone(r)

    def test_stats_search(self):
        api = iDbApiJson()
        r = api.stats("search")
        self.assertIsNotNone(r)

    def test_top_media(self):
        api = iDbApiJson()
        r = api.top_media()
        self.assertIsNotNone(r)

    def test_top_records(self):
        api = iDbApiJson()
        r = api.top_records()
        self.assertIsNotNone(r)

if __name__ == '__main__':
    unittest.main()
