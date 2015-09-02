import geopandas
import tempfile

output = tempfile.mktemp()
input.to_file(output, driver="GeoJSON")
