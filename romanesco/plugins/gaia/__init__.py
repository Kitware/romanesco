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


def push_handler(spec, **kwargs):
    path = spec.get("path", None)
    if path is not None:
        df = geopandas.GeoDataFrame.to_file(
            os.path.join(__path__[0], path),
            driver=spec.get("format", None))


def import_validators():
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



def load(params):
    romanesco.register_executor('gaia', executor.run)

    import_validators()

    #converters_dir = os.path.join(params['plugin_dir'], 'converters')
    #romanesco.format.import_converters([
    #    os.path.join(converters_dir, 'geopandas')
    #])

    romanesco.io.register_fetch_handler('gaia', fetch_handler)
    romanesco.io.register_push_handler('gaia', push_handler)
