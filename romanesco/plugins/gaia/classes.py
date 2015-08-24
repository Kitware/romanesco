import sys
import ast
import os
from romanesco.format import validators


class RomanescoTypeConverter(object):

    types = {}

    def __new__(cls, value, **kwargs):

        if cls.is_valid(value, **kwargs):
            return cls.convert(value, **kwargs)
        else:
            raise Exception("Invalid Romanesco Type")

    @classmethod
    def is_valid(cls, value, **kwargs):
        # Currently we don't actually validate anything
        return True

    @classmethod
    def convert(cls, value, **kwargs):
        # Currently we don't actually convert anything
        # Would have to resolve the format of value before
        # converting it to the format in kwargs
        return value

# Define the Output converter
Output = type("Output", (RomanescoTypeConverter,), {})

module = sys.modules[__name__]

for key, val in validators.items():
    if not hasattr(module, key.title()):
        setattr(module,
                str(key.title()),
                type(str(key.title()), (RomanescoTypeConverter, ), {}))

        RomanescoTypeConverter.types[key.title()] = getattr(module, key.title())


class AnalysisStaticParser(ast.NodeVisitor):

    def __init__(self, filepath, mode, name=None, *args, **kwargs):
        super(AnalysisStaticParser, self).__init__(*args, **kwargs)

        if name is None:
            name = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, "r") as fh:
            script = fh.read()

        self.tree = ast.parse(script)

        # Internally maintain inputs and outputs as dicts
        # with type name as keys and parsed type dicts as
        # values.  This ensure we never have duplicate inputs
        # and defines our duplicate input policy,  last
        # declaration wins
        self.analysis = {
            "name": name,
            "mode": mode,
            "script": script,
            "inputs": {},
            "outputs": {}
        }

    def parse(self):
        self.visit(self.tree)
        self.analysis['inputs'] = self.analysis['inputs'].values()
        self.analysis['outputs'] = self.analysis['outputs'].values()
        return self.analysis

    # Parse out the actual ast information
    def get_value(self, node):
        try:
            # Strings and Bytes
            return node.s
        except AttributeError:
            # Numbers
            return node.n
        except AttributeError:
            # Named constaints (True, False, None)
            return node.value
        except AttributeError as e:
            raise e

    def parse_type(self, node):
        ret = {}

        # Must have args
        # Args must be length 1
        # args[0] must have id
        ret["name"] = node.args[0].id

        # Must be callable
        # Must have func
        # Func must have id
        # id must be in romanesco_types
        ret["type"] = node.func.id.lower()

        # Must have keywords argument
        for keyword in node.keywords:
            # Must have 'arg'
            # 'arg' must be in valid keywords
            # keyword must have value
            ret[keyword.arg] = self.get_value(keyword.value)

            # Should do static analysis here
            # i.e., require 'format' to be a keyword arg
            return (ret['name'], ret)

    def parse_output(self, node):
        ret = {}
        # must have targets
        # targets must be length 1 (does not support multiple assignments)
        # target[0] must have id
        ret['name'] = node.targets[0].id

        # Node must have value
        # Value must have keywords
        for keyword in node.value.keywords:
            # Must have 'arg'
            # 'arg' must be in valid keywords
            # keyword must have value
            ret[keyword.arg] = self.get_value(keyword.value)

        # Should do static analysis here
        # i.e., require 'format' to be a keyword arg
        return (ret['name'], ret)

    def is_type(self, node):
        try:
            return node.func.id in RomanescoTypeConverter.types.keys()
        except AttributeError:
            return False

    def is_output(self, node):
        try:
            return node.value.func.id == "Output"
        except AttributeError:
            return False

    # Look for ast.Assign objects whos RVALUEs are Output ast.Call objects
    def visit_Assign(self, node):
        if self.is_output(node):
            _name, _output = self.parse_output(node)
            self.analysis['outputs'][_name] = _output

        self.generic_visit(node)

    # Look for ast.Call objects that match romanesco_types
    def visit_Call(self, node):
        if self.is_type(node):
            _name, _input = self.parse_type(node)
            self.analysis['inputs'][_name] = _input

        self.generic_visit(node)
