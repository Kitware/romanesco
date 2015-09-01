import os
import romanesco
import geopandas as gpd
from romanesco.specs import Port, PortList
from romanesco.plugins.gaia import PACKAGE_DIR as GAIA_DIR


class GeopandasReader(object):
    __inputs__ = PortList([Port(name="path",
                                type="string",
                                format="text"),
                          Port(name="driver",
                               type="string",
                               format="text")])
    __outputs__ = PortList([Port(name="dataframe",
                                 type="geo",
                                 format="dataframe")])

    def __init__(self, *args, **kwargs):
        self.inputs = []
        self.outputs = []
        for port in self.__inputs__:
            self.inputs.append(dict(port.items() +
                                    [("data", kwargs.get(port.name, None))]))

        self.outputs = kwargs.get("outputs", [])

    @property
    def script(self):
        return """import geopandas as gpd\noutput = gdp.read_file(path, driver=driver)"""

    def parse(self):
        return {
            "inputs": self.__inputs__.values(),
            "outputs": self.__outputs__.values(),
            "script": self.script,
            "mode": "python"}

    def run(self):
        return (self.parse(), self.inputs, self.outputs)



if __name__ == "__main__":
    c = GeopandasReader(path=os.path.join(GAIA_DIR, "tests", "data", "points.shp"),
                        format="ESRI Shapefile")
    c.run()
