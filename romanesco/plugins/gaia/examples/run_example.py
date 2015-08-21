import sys
import romanesco
sys.path.append("..")

from classes import AnalysisStaticParser
from pprint import pprint

print("### Content of test_analysis.py:\n")
with open("test_analysis.py", "r") as fh:
    print(fh.read())


# Parse test_analysis.py
spec = AnalysisStaticParser("test_analysis.py", "python").parse()

# Print the spec
print("\n\n### Spec generated from static analysis:\n")
pprint(spec)


# Run romanesco against the spec
outputs = romanesco.run(
    spec,
    inputs={
        "a": {"format": "csv", "data": 'a,b,c\n1,2,3'},
        "b": {"format": "csv", "data": 'a,b,c\n4,5,6'}
    },
    outputs={
        "c": {"format": "csv"}
    },
    debug=True)

print("\n\n### Output of romanesco.run() with above spec:\n")
pprint(outputs)

# An actual romanesco script taken from the NEX minerva demo
# which has been converted
# parser = AnalysisStaticParser("mean_contour.py", "spark.python")
# pprint(parser.parse())
