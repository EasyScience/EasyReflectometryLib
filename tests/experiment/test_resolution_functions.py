import numpy as np
from easyreflectometry.experiment.resolution_functions import linear_spline_resolution_function
from easyreflectometry.experiment.resolution_functions import percentage_fhwm_resolution_function


def test_percentage_fhwm_resolution_function():
    resolution_function = percentage_fhwm_resolution_function(5)
    assert np.all(resolution_function([0, 2.5]) == [5, 5])
    assert resolution_function([-100]) == 5
    assert resolution_function([100]) == 5


def test_linear_spline_resolution_function():
    resolution_function = linear_spline_resolution_function([0, 10], [5, 10])
    assert np.all(resolution_function([0, 2.5]) == [5, 6.25])
    assert resolution_function([-100]) == 5
    assert resolution_function([100]) == 10
