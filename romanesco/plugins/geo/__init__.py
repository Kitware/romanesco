import os
import romanesco


def load(params):
    romanesco.format.import_converters(
        os.path.join(params['plugin_dir'], 'converters'))
