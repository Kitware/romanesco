import os
import romanesco
import unittest


class TestGeo(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "gaia", "tests", "data")

    def test_fiona_to_geodataframe(self):
        fiona_data = {"format": "fiona", "data": os.path.join(self.data_dir, "points.shp")}
        print fiona_data
        geodf_data = romanesco.convert("geo", fiona_data, {"format": "geodataframe"})
        print geodf_data
        fiona_data_2 = romanesco.convert("geo", geodf_data, {"format": "fiona"})
        print fiona_data_2
        geodf_data_2 = romanesco.convert("geo", fiona_data, {"format": "geodataframe"})
        print geodf_data_2

    def test_custom_conversion(self):
        fiona_data = {"format": "fiona", "data": os.path.join(self.data_dir, "points.shp")}
        geopandas_converter = {
            "inputs": [{"type": "geo", "format": "geodataframe", "name": "input"}, {"type": "string", "format": "text", "name": "driver"}, {"type": "string", "format": "text", "name": "file"}],
            "outputs": [{"type": "geo", "format": "fiona", "name": "output"}],
            "script": "input.to_file(file, driver=driver)\noutput = file",
            "mode": "python"
        }
        output = romanesco.run(geopandas_converter, {
            "input": fiona_data,
            "file": {"format": "text", "data": "file.json"},
            "driver": {"format": "text", "data": "GeoJSON"}
        })
        # With some syntactic sugar, the line above could become:
        # geopandas_converter.run(input="points.shp", file="file.json", driver="GeoJSON")

        print output
