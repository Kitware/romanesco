import os
import romanesco
from romanesco.specs import Port, PortList
from romanesco.plugins.gaia import PACKAGE_DIR as GAIA_DIR

from pprint import pprint


class GeopandasReader(object):
    __inputs__ = PortList([Port(name="path",
                                type="string",
                                format="text",
                                validate=False),
                          Port(name="driver",
                               type="string",
                               format="text",
                               validate=False)])
    __outputs__ = PortList([Port(name="output",
                                 type="geo",
                                 format="dataframe")])

    def __init__(self, *args, **kwargs):
        self.inputs = {}

        for pos, port in enumerate(self.__inputs__):
            self.inputs[port.name] = dict(port.items() + [("data", args[pos])])

    @property
    def script(self):
        return """import geopandas as gpd\noutput = gpd.read_file(path, driver=driver)"""

    def parse(self):
        return {
            "inputs": self.__inputs__.values(),
            "outputs": self.__outputs__.values(),
            "script": self.script,
            "mode": "python"}

    def run(self):
        raw = romanesco.run(self.parse(), inputs=self.inputs)
        ret = []

        for pos, port in enumerate(self.__outputs__):
            try:
                ret.append(raw[port.name]['data'])
            except KeyError:
                # Error here?
                pass

        return ret[0] if len(ret) == 1 else tuple(ret)

if __name__ == "__main__":
    c = GeopandasReader(os.path.join(GAIA_DIR, "tests", "data", "points.shp"),
                        "ESRI Shapefile")

    pprint(c.run())
