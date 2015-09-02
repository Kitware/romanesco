import os
import romanesco
from romanesco.specs import Port, PortList
from romanesco.plugins.gaia import PACKAGE_DIR as GAIA_DIR


class Task(object):
    __inputs__ = PortList()
    __outputs__ = PortList()

    def __init__(self, *args, **kwargs):
        self.inputs = {}
        self.mode = kwargs.get("mode", "python")

        for pos, port in enumerate(self.__inputs__):
            self.inputs[port.name] = dict(port.items() + [("data", args[pos])])

    @property
    def script(self):
        raise Exception("Must be implemented in subclass!")

    def parse(self):
        return {
            "inputs": self.__inputs__.values(),
            "outputs": self.__outputs__.values(),
            "script": self.script,
            "mode": self.mode}

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


class GeopandasReader(Task):
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

    @property
    def script(self):
        return """import geopandas as gpd\noutput = gpd.read_file(path, driver=driver)"""


class GeopandasWriter(Task):
    __inputs__ = PortList([
        Port(name="df",
             type="geo",
             format="dataframe",
             validate=False),
        Port(name="path",
             type="string",
             format="text",
             validate=False),
        Port(name="driver",
             type="string",
             format="text",
             validate=False)])
    __outputs__ = PortList([Port(name="output",
                                 type="boolean",
                                 format="boolean")])

    @property
    def script(self):
        return """
import geopandas as gpd
try:
   df.to_file(path, driver=driver)
   output = True
except Exception:
   output = False
"""


if __name__ == "__main__":
    r = GeopandasReader(os.path.join(GAIA_DIR, "tests", "data", "points.shp"),
                        "ESRI Shapefile")

    df = r.run()

    w = GeopandasWriter(df,
                        "/tmp/tmp/points.shp",
                        "ESRI Shapefile")

    w.run()
