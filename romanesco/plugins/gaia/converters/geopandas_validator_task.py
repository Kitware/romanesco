from romanesco.plugins.gaia.classes import Geo, Output
import geopandas
# Intentionally leave off format from Geo(), this
# will be added by the gaia import_validators() function
output = Output(isinstance(Geo(input), geopandas.GeoDataFrame),
                type="boolean",
                format="boolean")
