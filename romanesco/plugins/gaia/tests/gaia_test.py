import romanesco
import unittest


class TestGaia(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetch_shapefile(self):
        import pudb; pu.db
        romanesco.run(
            {"inputs": [{"name": "input",
                         "type": "geo",
                         "format": "dataframe"}],
             "outputs": [{"name": "out",
                          "type": "geo",
                          "format": "dataframe"}],
             "script": "out = input",
             "mode": "gaia"},
            inputs={"input":
                    {"path": "tests/data/shapefile.shp",
                     "mode": "gaia",
                     "format": "ESRI Shapefile"}},
            outputs={"out":
                     {"path": "tests/tmp/shapefile.shp",
                      "mode": "gaia",
                      "format": "ESRI Shapefile"}})
