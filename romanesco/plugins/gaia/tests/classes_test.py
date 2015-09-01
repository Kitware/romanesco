import os
from romanesco.plugins.gaia.classes import GeopandasReader
from base import BaseTest
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
