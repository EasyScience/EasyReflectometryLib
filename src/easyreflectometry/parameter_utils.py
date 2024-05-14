from copy import deepcopy
from numbers import Number
from typing import Union

from easyscience.Objects.ObjectClasses import Parameter


def get_as_parameter(name: str, value: Union[Parameter, Number, None], default_dict: dict) -> Parameter:
    """
    This function creates a parameter for the variable `name`.  A parameter has a value and metadata.
    If the value already is a parameter, it is returned.
    If the value is a number, a parameter is created with this value and metadata from the dictionary.
    If the value is None, a parameter is created with the default value and metadata from the dictionary.

    param value: The value to use for the parameter.  If None, the default value in the dictionary is used.
    param name: The name of the parameter
    param default_dict: Dictionary with entry for `name` containing the default value and metadata for the parameter
    """
    # Ensure we got the dictionary for the parameter with the given name
    # Should leave the passed dictionary unchanged
    if name not in default_dict:
        parameter_dict = deepcopy(default_dict)
    else:
        parameter_dict = deepcopy(default_dict[name])

    if value is None:
        # Create a default parameter using both value and metadata from dictionary
        return Parameter(name, **parameter_dict)
    elif isinstance(value, Number):
        # Create a parameter using provided value and metadata from dictionary
        del parameter_dict['value']
        return Parameter(name, value, **parameter_dict)
    elif not isinstance(value, Parameter):
        raise ValueError(f'{name} must be a Parameter, a number, or None.')
    return value
