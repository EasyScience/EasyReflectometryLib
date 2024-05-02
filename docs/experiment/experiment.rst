Experiment
==========

The main component of an experiment in :py:mod:`EasyReflectometry` is the `model`. 
This is a description of the `sample` and the environment in which the experiment is performed. 
The `Model` is used to calculate the reflectivity of the `sample` at a given set of angles (`q` values).
The `resolution_functions` are used to account for non-ideal effects in the instrument.


:py:class:`Model`
-----------------

A `Model` instance contains a `sample` and variables describing experimental settings.
To be able to compute reflectivities it is also necessary to have a `calculator` (interface).

.. code-block:: python 

   from EasyReflectometry.calculators import CalculatorFactory
   from EasyReflectometry.experiment import Model
   from EasyReflectometry.sample import Sample

   default_sample = Sample()
   m = Model(
      sample=default_sample,
      scale=1.0,
      background=1e-6
   )

   interface = CalculatorFactory()
   model.interface = interface

This will create a :py:class:`Model` instance with the `default_sample` and the environment variables `scale` factor set to 1.0 and a `background` of 1e-6.
Following the `interface` is set to the default calculator.


:py:mod:`resolution_functions`
------------------------------
A resolution function enables the `EasyReflectometry` model to account for various non ideal effects that might be present in the experimental setup.
When determining reflectivity the resolution function defines the smearing to apply.
For a given Q point such smearing is applied by determining an average of the neighboring Q point weigthed by a normal distribution, 
which has a Q point dependent Full Width at the Half Maximum (FWHM) that again is defined by the resolution function.

:py:func:`percentage_fhwm_resolution_function`
Often we rely on a resolution function that has a simple functional dependecy of the Q point.
By this is understood that the applied smearing in an Q point has a FWHM that is given as a percentage of the value of the Q point.

.. code-block:: python 

   from EasyReflectometry.experiment import Model
   from EasyReflectometry.experiment import percentage_fhwm_resolution_function

   resolution_function = percentage_fhwm_resolution_function(1)

   m = Model(
      resolution_function=resolution_function
   )

This will create a :py:class:`Model` instance where a resolution function is defined that has a FWHM that is 1% of the Q point value.


:py:func:`linear_spline_resolution_function`
Alternatively the FWHM value might be determined and declared directly for each measured Q point.
When this is the case the provided Q points and the corresponding FWHM values can be used to declare a linear spline function
and thereby enable a determination of the reflectivity at an arbitrary point within the provided range of discrete Q points.

.. code-block:: python 

   from EasyReflectometry.experiment import Model
   from EasyReflectometry.experiment import linear_spline_resolution_function

   m = Model()

   resolution_function = linear_spline_resolution_function(
      q_points=[0.01, 0.2, 0.31],
      fwhm_values=[0.001, 0.043, 0.026]
   )

   m.resolution_function = resolution_function

This will create a :py:class:`Model` instance where a resolution function is defined that has a FWHM that is determined from a linear interpolation.
In the present case the provided data points are (`[0.01, 0.2, 0.31]`) and the corresponding function values are (`[0.001, 0.043, 0.026]`).
