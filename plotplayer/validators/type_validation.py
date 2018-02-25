"""Simple type validation methods"""

from matplotlib.figure import Figure

INSTANCE_MESSAGE = "{} must be an instance of {}"
CALLABLE_MESSAGE = "{} must be a callable object"

def assert_is_figure(value, variable_name):
    """Asserts that a value is a Matplotlib Figure"""
    assert isinstance(value, Figure), INSTANCE_MESSAGE.format(variable_name, str(Figure))

def assert_is_int(value, variable_name):
    """Asserts that a value is an integer"""
    assert isinstance(value, int), INSTANCE_MESSAGE.format(variable_name, str(int))

def assert_is_callable(value, variable_name):
    """Asserts that a value is a callable function"""
    assert callable(value), CALLABLE_MESSAGE.format(variable_name)
