import os
import romanesco
from romanesco.utils import tmpdir
from base import BaseTest


class TestGaia(BaseTest):
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
