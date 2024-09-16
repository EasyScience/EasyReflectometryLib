"""
Tests exercising the methods of the topmost classes for nested structure.
To ensure that the parameters are relayed.
"""

from copy import copy

from numpy.testing import assert_almost_equal

from easyreflectometry.calculators import CalculatorFactory
from easyreflectometry.experiment import LinearSpline
from easyreflectometry.experiment import Model
from easyreflectometry.sample import Multilayer
from easyreflectometry.sample import RepeatingMultilayer
from easyreflectometry.sample import SurfactantLayer


def test_dict_skip_unique_name():
    # When
    resolution_function = LinearSpline([0, 10], [0, 10])
    model = Model(interface=CalculatorFactory())
    model.resolution_function = resolution_function
    for additional_layer in [SurfactantLayer(), Multilayer(), RepeatingMultilayer()]:
        model.add_item(additional_layer)

    # Then
    dict_no_unique_name = model.as_dict(skip=['unique_name'])

    # Expect
    assert 'unique_name' not in dict_no_unique_name


def test_copy():
    # When
    resolution_function = LinearSpline([0, 10], [0, 10])
    model = Model(interface=CalculatorFactory())
    model.resolution_function = resolution_function
    for additional_layer in [SurfactantLayer(), Multilayer(), RepeatingMultilayer()]:
        model.add_item(additional_layer)

    # Then
    model_copy = copy(model)

    # Expect
    assert sorted(model.as_data_dict()) == sorted(model_copy.as_data_dict())
    assert model._resolution_function.smearing(5.5) == model_copy._resolution_function.smearing(5.5)
    assert model.interface().name == model_copy.interface().name
    assert_almost_equal(
        model.interface().fit_func([0.3], model.unique_name),
        model_copy.interface().fit_func([0.3], model_copy.unique_name),
    )
    assert model.unique_name != model_copy.unique_name
    assert model.name == model_copy.name
    assert model.as_data_dict(skip=['interface', 'unique_name', 'resolution_function']) == model_copy.as_data_dict(
        skip=['interface', 'unique_name', 'resolution_function']
    )
