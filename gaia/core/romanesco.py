"""This module contains components integrating romanesco with gaia."""

from __future__ import absolute_import
# from romanesco import io
from gaia.core import Task

# Use a python type to romanesco data format definition dict?


class RomanescoTask(Task):

    """A task using Romanesco io API's for port data handling.

    This class is meant to be an abstraction for a general execution
    mode in Romanesco.  It only handles the io components, subclasses
    should implement specific execution steps in :py:func:`.run`.
    """

#    def get_input_data(self, name='0'):
#        """Return the data from the named input port."""
#        port = self.get_input(name)
#        return io.fetch(port.spec)

#    def run(self, *arg, **kw):
#        """Run the superclass method and push outputs through romanesco.
#
#        This method should be called **after** you update the output
#        cache (self._output_data).
#        """
#        super(RomanescoTask, self).run(*arg, **kw)
#        for port in self.outputs:
#            data = self.get_output_data(port)
#            io.push(data, self.outputs[port].spec)

#    @classmethod
#    def make_input_port(cls, spec):
#        port = Task.make_input_port(object)  # should specialize
#        port.spec = {'format': 'number', 'data': None}
#
#    @classmethod
#    def make_output_port(cls, spec):
#        port = Task.make_output_port(object)
#        port.spec = {'format': 'number', 'data': None}


class PythonTask(RomanescoTask):

    """A romanesco task that executes a python script."""

    script = ''  # the script source is a class attribute

    def run(self, *arg, **kw):
        """Execute the python script."""
        # get runtime variables from input ports
        env = {}
        for port in self.inputs:
            env[port] = self.get_input_data(port)

        # execute the script in the environment
        exec(self.script, env)

        # set output ports
        for port in self.outputs:
            self._output_data[port] = env.get(port)

        # finish with superclass method
        super(PythonTask, self).run(*arg, **kw)


def get_task(spec):
    """Generate a new task from a spec object.

    :param dict spec: A romanesco task specification
    :rtype: A subclass of :py:gaia.core.Task

    The returned class is a Task subclass that implements the given
    Romanesco specification.  This task can be inserted into a pipeline
    just like any other.

    Example:
    >>> Add = get_task({
    ...     'name': 'Add',
    ...     'inputs': [
    ...         {'name': 'a', 'type': 'number'},
    ...         {'name': 'b', 'type': 'number'}
    ...     ],
    ...     'outputs': [
    ...         {'name': 'c', 'type': 'number'}
    ...     ],
    ...     'script': 'c = a + b',
    ...     'mode': 'python'
    ... })
    >>> Multiply = get_task({
    ...     'name': 'Multiply',
    ...     'inputs': [
    ...         {'name': 'a', 'type': 'number'},
    ...         {'name': 'b', 'type': 'number'}
    ...     ],
    ...     'outputs': [
    ...         {'name': 'c', 'type': 'number'}
    ...     ],
    ...     'script': 'c = a * b',
    ...     'mode': 'python'
    ... })
    >>> a1 = Add().set_input(a=1, b=2)
    >>> a2 = Add().set_input(a=3, b=4)
    >>> m = Multiply().set_input(a=a1.get_output('c'), b=a2.get_output('c'))
    >>> m.get_output_data('c')
    21
    """
    if spec.get('mode') != 'python':  # only implement python for now
        raise Exception('Unhandled execution mode in task spec')

    input_ports = {}
    for input_spec in spec.get('inputs', []):
        input_ports[input_spec['name']] = RomanescoTask.make_input_port(object)

    output_ports = {}
    for output_spec in spec.get('outputs', []):
        output_ports[output_spec['name']] = RomanescoTask.make_output_port(object)

    script = spec['script']
    name = spec['name']

    attrs = {
        'input_ports': input_ports,
        'output_ports': output_ports,
        'script': script
    }
    return type(name, (PythonTask,), attrs)


__all__ = ('get_task',)
