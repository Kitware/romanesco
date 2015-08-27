import os
import romanesco
from . import executor
import geopandas
import fiona
from romanesco.format import conv_graph, Validator
from classes import AnalysisStaticParser

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_handler(spec, **kwargs):
    path = spec.get("path", None)
    if path is not None:
        df = geopandas.GeoDataFrame.from_file(
            os.path.join(__path__[0], path),
            driver=spec.get("format", None))

    return df


def push_handler(data, spec, **kwargs):
    path = spec.get("path", None)
    format = spec.get("format", None)
    if path is not None and path is not None:
        data.to_file(path, driver=format)


def load_geopandas_validators():
    # Geopandas formats are the same strings as the fiona/GDAL drivers
    task_path = os.path.join(PACKAGE_DIR,
                             "converters",
                             "geopandas_validator_task.py")

    for driver in fiona.supported_drivers.keys():
        analysis = AnalysisStaticParser(task_path, mode="gaia").parse()

        analysis['inputs'][0]['format'] = driver
        analysis['name'] = "validate_{}".format(driver)

        analysis['write_script'] = True

        in_type = "geo"

        conv_graph.add_node(Validator(in_type, driver), {
            "validator": analysis
        })


def add_geopandas_converter(in_format, out_format):
    script = 'output = Output(Geo(input, format="{}"),type="geo", format="{}")'
    conv_graph.add_edge(
        Validator("geo", in_format),
        Validator("geo", out_format),
        AnalysisStaticParser(script.format(in_format, out_format),
                             mode="gaia",
                             name="{}_to_{}".format(in_format, out_format))
        .parse())

def load_geopandas_converters():    
    for in_driver in fiona.supported_drivers.keys():
        for out_driver, mode in fiona.supported_drivers.items():
            
            if mode in ["rw", "raw"]:
                add_geopandas_converter(in_driver, out_driver)        


def load(params):
    romanesco.register_executor('gaia', executor.run)

    load_geopandas_validators()
    load_geopandas_converters()

    romanesco.io.register_fetch_handler('gaia', fetch_handler)
    romanesco.io.register_push_handler('gaia', push_handler)
