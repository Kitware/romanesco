import romanesco
import os
from romanesco.plugins.gaia import PACKAGE_DIR
from romanesco.utils import tmpdir
import unittest
import hashlib

class TestGaia(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(PACKAGE_DIR, "tests", "data")
        self.expected_dir = os.path.join(self.data_dir, "expected_output")
        # Should also make sure we're using the configured tmp dir
        # instead of just assuming that it is 'tmp'

    def tearDown(self):
        pass

    def assertFileEquals(self, in_file, out_file):
        with open(in_file, "rb") as source:
            with open(out_file, "rb") as dest:
                self.assertEquals(
                    hashlib.md5(source.read()).hexdigest(),
                    hashlib.md5(dest.read()).hexdigest())

    def assertShapefileEquals(self, in_file, out_file):
        for ext in [".cpg", ".dbf", ".prj", ".shp", ".shx"]:
            self.assertFileEquals(in_file + ext,  out_file + ext)

    def test_fetch_push_shapefile(self):
        # import pudb; pu.db

        with tmpdir(cleanup=True) as tmp_dir:
            romanesco.run(
                {"inputs": [{"name": "input",
                             "type": "geo",
                             "format": "ESRI Shapefile"}],
                 "outputs": [{"name": "out",
                              "type": "geo",
                              "format": "ESRI Shapefile"}],
                 "script": "out = input",
                 "mode": "gaia"},
                inputs={"input":
                        {"path": os.path.join(self.data_dir, "points.shp"),
                         "mode": "gaia",
                         "format": "ESRI Shapefile"}},
                outputs={"out":
                         {"path": os.path.join(tmp_dir, "points.shp"),
                          "mode": "gaia",
                          "format": "ESRI Shapefile"}})

            self.assertShapefileEquals(
                os.path.join(self.data_dir, "points"),
                os.path.join(tmp_dir, "points"))


    def test_shape_to_geojson(self):
        # import pudb; pu.db

        with tmpdir(cleanup=True) as tmp_dir:
            romanesco.run(
                {"inputs": [{"name": "dataframe",
                             "type": "geo",
                             "format": "ESRI Shapefile"}],
                 "outputs": [{"name": "dataframe",
                              "type": "geo",
                              "format": "GeoJSON"}],
                 "script": "",
                 "mode": "gaia"},
                inputs={"dataframe":
                        {"path": os.path.join(self.data_dir, "points.shp"),
                         "mode": "gaia",
                         "format": "ESRI Shapefile"}},
                outputs={"dataframe":
                         {"path": os.path.join(tmp_dir, "points.geojson"),
                          "mode": "gaia",
                          "format": "GeoJSON"}})

            self.assertFileEquals(
                os.path.join(tmp_dir, "points.geojson"),
                os.path.join(self.expected_dir,
                             "points.shp",
                             "GeoJSON",
                             "output"))

    def test_geojson_to_shape(self):
        # import pudb; pu.db

        with tmpdir(cleanup=True) as tmp_dir:
            romanesco.run(
                {"inputs": [{"name": "dataframe",
                             "type": "geo",
                             "format": "GeoJSON"}],
                 "outputs": [{"name": "dataframe",
                              "type": "geo",
                              "format": "ESRI Shapefile"}],
                 "script": "",
                 "mode": "gaia"},
                inputs={"dataframe":
                        {"path": os.path.join(self.data_dir, "points.geojson"),
                         "mode": "gaia",
                         "format": "GeoJSON"}},
                outputs={"dataframe":
                         {"path": os.path.join(tmp_dir, "points.shp"),
                          "mode": "gaia",
                          "format": "ESRI Shapefile"}})

            self.assertShapefileEquals(
                os.path.join(tmp_dir, "points"),
                os.path.join(self.expected_dir,
                             "points.geojson",
                             "ESRI Shapefile",
                             "output",   # First output is the folder
                             "output"))  # Second is the filename wo/extension
