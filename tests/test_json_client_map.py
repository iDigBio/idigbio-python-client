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

    def test_save_map_from_bounding_box(self):
        api = iDbApiJson()
        # rectangular bounding box around Gainesville, FL
        bbox = {"type": "geo_bounding_box",
                "bottom_right": {"lat": 29.642979999999998, "lon": -82.00},
                "top_left": {"lat": 29.66298, "lon": -82.35315800000001}}
        m = api.create_map(rq={"geopoint": bbox})
        m.save_map_image("test_bounded_map", None, bbox=bbox)
        self.assertTrue(os.path.exists("test_bounded_map.png"))
        os.unlink("test_bounded_map.png")


if __name__ == '__main__':
    unittest.main()
