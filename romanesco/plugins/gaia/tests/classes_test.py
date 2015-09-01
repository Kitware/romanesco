import os
from romanesco.plugins.gaia.classes import GeopandasReader, GeopandasWriter
from base import BaseTest
from romanesco.utils import tmpdir
import geopandas as gpd
import tempfile


class TestClasses(BaseTest):
    def assertDataFrameEquals(self, system, ground):
        system_path = tempfile.NamedTemporaryFile()
        ground_path = tempfile.NamedTemporaryFile()

        with open(system_path.name, "wb") as fh:
            fh.write(system.to_json())

        with open(ground_path.name, "wb") as fh:
            fh.write(ground.to_json())

        self.assertFileEquals(system_path.name, ground_path.name)

    def test_GeopandasReader(self):
        file_path = os.path.join(self.data_dir, "points.geojson")
        reader = GeopandasReader(file_path, "GeoJSON")

        system = reader.run()
        ground = gpd.read_file(file_path, driver="GeoJSON")

        self.assertDataFrameEquals(system, ground)

    def test_GeopandasWriter(self):
        ground_path = os.path.join(self.data_dir, "points.geojson")
        df = gpd.read_file(ground_path, driver="GeoJSON")

        with tmpdir(cleanup=True) as tmp_dir:
            system_path = os.path.join(tmp_dir, "points.geojson")

            writer = GeopandasWriter(df, system_path, "GeoJSON")
            writer.run()

            self.assertTrue(os.path.exists(system_path))

            self.assertFileEquals(system_path, ground_path)

    def test_GeopandasReader_to_GeopandasWriter(self):
        ground_path = os.path.join(self.data_dir, "points.shp")
        reader = GeopandasReader(ground_path, "ESRI Shapefile")

        with tmpdir(cleanup=True) as tmp_dir:
            system_path = os.path.join(tmp_dir, "points.shp")

            writer = GeopandasWriter(reader.run(), system_path, "ESRI Shapefile")
            writer.run()

            self.assertTrue(os.path.exists(system_path))

            self.assertShapefileEquals(system_path, ground_path)
