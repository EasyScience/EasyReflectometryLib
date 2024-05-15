import numpy as np
from easyreflectometry.experiment.resolution_functions import DEFAULT_RESOLUTION_FWHM_PERCENTAGE
from easyreflectometry.experiment.resolution_functions import LinearSpline
from easyreflectometry.experiment.resolution_functions import PercentageFhwm

# from easyreflectometry.experiment.resolution_functions import linear_spline_resolution_function
# from easyreflectometry.experiment.resolution_functions import percentage_fhwm_resolution_function


# def test_percentage_fhwm_resolution_function():
#     # When Then
#     resolution_function = percentage_fhwm_resolution_function(5)

#     # Expect
#     assert np.all(resolution_function([0, 2.5]) == [5, 5])
#     assert resolution_function([-100]) == 5
#     assert resolution_function([100]) == 5


# def test_linear_spline_resolution_function():
#     # When Then
#     resolution_function = linear_spline_resolution_function([0, 10], [5, 10])

#     # Expect
#     assert np.all(resolution_function([0, 2.5]) == [5, 6.25])
#     assert resolution_function([-100]) == 5
#     assert resolution_function([100]) == 10


# def test_percentage_fhwm_resolution():
#     # When
#     resolution_function = PercentageFhwm(1.0)

#     # Then Expect
#     assert np.all(resolution_function.smearing([0, 2.5]) == [1.0, 1.0])
#     assert resolution_function.smearing([-100]) == 1.0
#     assert resolution_function.smearing([100]) == 1.0


def test_percentage_fhwm_resolution_as_dict():
    # When
    resolution_function = PercentageFhwm(1.0)

    # Then Expect
    resolution_function.as_dict() == {'smearing': 'PercentageFhwm', 'constant': 1.0}


def test_percentage_fhwm_resolution_none():
    # When
    resolution_function = PercentageFhwm()

    # Then Expect
    assert np.all(
        resolution_function.smearing([0, 2.5]) == [DEFAULT_RESOLUTION_FWHM_PERCENTAGE, DEFAULT_RESOLUTION_FWHM_PERCENTAGE]
    )
    assert resolution_function.smearing([-100]) == DEFAULT_RESOLUTION_FWHM_PERCENTAGE
    assert resolution_function.smearing([100]) == DEFAULT_RESOLUTION_FWHM_PERCENTAGE


def test_linear_spline_resolution():
    # When
    resolution_function = LinearSpline(q_data_points=[0, 10], fwhm_values=[5, 10])

    # Then Expect
    assert np.all(resolution_function.smearing([0, 2.5]) == [5, 6.25])
    assert resolution_function.smearing([-100]) == 5
    assert resolution_function.smearing([100]) == 10


def test_linear_spline_resolution_as_dict():
    # When
    resolution_function = LinearSpline(q_data_points=[0, 10], fwhm_values=[5, 10])

    # Then Expect
    resolution_function.as_dict() == {'smearing': 'LinearSpline', 'q_data_points': [0, 10], 'fwhm_values': [5, 10]}
