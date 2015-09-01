import os
import unittest
import hashlib
from romanesco.plugins.gaia import PACKAGE_DIR


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.join(PACKAGE_DIR, "tests", "data")
        self.expected_dir = os.path.join(self.data_dir, "expected_output")
        # Should also make sure we're using the configured tmp dir
        # instead of just assuming that it is 'tmp'

    def tearDown(self):
        pass

    def assertFileEquals(self, in_file, out_file):
        with open(in_file, "rb") as source:
            with open(out_file, "rb") as dest:
                self.assertEquals(
                    hashlib.md5(source.read()).hexdigest(),
                    hashlib.md5(dest.read()).hexdigest())

    def assertShapefileEquals(self, in_file, out_file):
        shape_extensions = [".cpg", ".dbf", ".prj", ".shp", ".shx"]

        if in_file[-4:] in shape_extensions:
            in_file = in_file[:-4]

        if out_file[-4:] in shape_extensions:
            out_file = out_file[:-4]

        for ext in shape_extensions:
            self.assertFileEquals(in_file + ext,  out_file + ext)
