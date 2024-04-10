from copy import deepcopy
from numbers import Number
from typing import Union

from easyCore.Objects.ObjectClasses import Parameter


def get_as_parameter(value: Union[Parameter, Number, None], name, default_dict: dict[str, str]) -> Parameter:
    # Should leave the passed dictionary unchanged
    local_dict = deepcopy(default_dict)
    if value is None:
        return Parameter(name, **local_dict[name])
    elif isinstance(value, Number):
        del local_dict[name]['value']
        return Parameter(name, value, **local_dict[name])
    elif not isinstance(value, Parameter):
        raise ValueError(f'{name} must be a Parameter, a number, or None.')
    return value
