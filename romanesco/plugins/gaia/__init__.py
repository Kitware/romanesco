import os
import romanesco
from . import executor
import geopandas
import fiona

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



def load(params):
    romanesco.register_executor('gaia', executor.run)

    #converters_dir = os.path.join(params['plugin_dir'], 'converters')
    #romanesco.format.import_converters([
    #    os.path.join(converters_dir, 'geopandas')
    #])

    romanesco.io.register_fetch_handler('gaia', fetch_handler)
    romanesco.io.register_push_handler('gaia', push_handler)
