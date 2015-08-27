from __future__ import print_function
import os
import shutil
import fiona
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXPECTED_DIR = os.path.join(BASE_DIR, "expected_output")

INPUT_FILES = ["points.shp", "points.geojson"]

if __name__ == "__main__":
    for f in INPUT_FILES:
        df = gpd.read_file(os.path.join(BASE_DIR, f))

        for driver, mode in fiona.supported_drivers.items():
            print( "Starting {}..".format(driver), end='')

            # BNA driver for some reason causes a segfault
            if mode in ["rw", "raw"] and driver != "BNA":
                path = os.path.join(EXPECTED_DIR, f, driver)

                # Make the directory
                try:
                    os.makedirs(path)
                except OSError:
                    pass

                try:
                    # Delete the output if it exists
                    if os.path.exists(os.path.join(path, "output")):
                        try:
                            os.remove(os.path.join(path, "output"))
                        # Error,  output was probably a directory not a file
                        except OSError:
                            shutil.rmtree(os.path.join(path, "output"), ignore_errors=True)

                    # Convert and save the output
                    df.to_file(os.path.join(path, "output"), driver=driver)
                    print("Done")

                except ValueError:
                    print("Done (Error)")
                    shutil.rmtree(path, ignore_errors=True)
            else:
                print("Done (Skipping)")
