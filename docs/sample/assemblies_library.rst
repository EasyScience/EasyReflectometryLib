Assemblies
==========

:py:mod:`EasyReflectometry` is designed to be used with a broad range of different assemblies.
These assemblies offer flexibility for the user and enable more powerful analysis by making chemical and pysical constraints available with limited code. 
In this page, we will document the assemblies that are available with simple examples of the constructors that exist.
Full API documentation is also available for the :py:mod:`EasyReflectometry.sample.assemblies` module.

:py:class:`Multilayer`
----------------------

This assembly should be used for a series of layers that, for whatever reason, should be thought of as a single object. 
For example, in the `simple fitting tutorial`_ this assembly type is used to combine the silicon and silicon dioxide layer that as formed into a single object. 
All of the separate layers in these objects will be fitted individually, i.e. there is no constraints present, however, there is some cognative benefit to grouping layers together. 

To create a :py:class:`Multilayer` object, we use the following construction.

.. code-block:: python 

    from EasyReflectometry.sample import Layer
    from EasyReflectometry.sample import Material
    from EasyReflectometry.sample import Multilayer

    si = Material.from_pars(2.07, 0, 'Si')
    sio2 = Material.from_pars(3.47, 0, 'SiO2')
    si_layer = Layer.from_pars(si, 0, 0, 'Si layer')
    sio2_layer = Layer.from_pars(sio2, 30, 3, 'SiO2 layer')

    subphase = Multilayer.from_pars(
        layers=[si_layer, sio2_layer], 
        name='Si/SiO2 subphase'
    )

This will create a :py:class:`Multilayer` object named :code:`subphase` which we can use in some :py:class:`Structure` for our analysis. 

:py:class:`RepeatingMultilayer`
-------------------------------

The :py:class:`RepeatingMultilayer` assembly type is an extension of the :py:class:`Multilayer` for the analysis of systems with a multilayer that has some number of repeats. 
This assembly type imposes some constraints, specifically that all of the repeats have the exact same structure (i.e. thicknesses, roughnesses, and scattering length densities), 
which brings with it some computational saving as the reflectometry coefficients only needs to be calculated once for this structure and propagated for the correct number of repeats. 
There is a `tutorial`_ that discusses the utilisation of this assembly type for a nickel-titanium multilayer system. 

The creation of a :py:class:`RepeatingMultilayer` object is very similar to that for the :py:class:`Multilayer`, with the addition of a number of repetitions. 

.. code-block:: python 

    from EasyReflectometry.sample import Layer
    from EasyReflectometry.sample import Material
    from EasyReflectometry.sample import RepeatingMultilayer

    ti = Material.from_pars(-1.9493, 0, 'Ti')
    ni = Material.from_pars(9.4245, 0, 'Ni')
    ti_layer = Layer.from_pars(ti, 40, 0, 'Ti Layer')
    ni_layer = Layer.from_pars(ni, 70, 0, 'Ni Layer')

    ni_ti = RepeatingMultilayer.from_pars(
        layers=[ti_layer, ni_layer], 
        repetitions=10, 
        name='Ni/Ti Multilayer'
    )

The number of repeats is a parameter that can be varied in the optimisation process, however given this is a value that depends on the synthesis of the sample this is unlikely to be necessary.

:py:class:`SurfactantLayer`
---------------------------

The :py:class:`SurfactantLayer` assembly type allows for the creating of a model to describe a monolayer of surfactant at some interface. 
Using this assembly, we can define our surfactant in terms of the chemistry of the head and tail groups and be confident that the constraints are present to ensure the number density if kept constant. 
The `surfactant monolayer tutorial`_ looks in detail at the definition of the scattering length density in the :py:class:`SurfactantLayer`. 
However, it is founded on the chemical formula for the head and tail group and the area per molecule that these groups occupy. 

The creation of a :py:class:`SurfactantLayer` object takes a large number arguments that are shown below. 

.. code-block:: python
   
    from EasyReflectometry.sample import Layer
    from EasyReflectometry.sample import Material
    from EasyReflectometry.sample import SurfactantLayer

    subphase = Material.from_pars(6.36, 0.0, 'D2O')
    superphase = Material.from_pars(0.0, 0.0, 'Air')
    
    head_formula = 'C10H18NO8P'
    tail_formula = 'C30D64'
    head_thickness = 10.0
    tail_thickness = 16.0
    head_solvent_surface_coverage = 0.2
    tail_solvent_surface_coverage = 0.0
    area_per_molecule = 48
    roughness = 3.3

    dppc = SurfactantLayer.from_pars(
        tail_layer_molecular_formula=tail_formula,
        tail_layer_thicness=tail_thickness,
        tail_layer_solvent=superphase,
        tail_layer_solvent_surface_coverage=tail_solvent_surface_coverage, 
        tail_layer_area_per_molecule=area_per_molecule,
        tail_layer_roughness=roughness,
        head_layer_molecular_formula=head_formula,
        head_layer_thickness=head_thickness,
        head_layer_solvent=subphase,
        head_layer_solvent_surface_coverage=head_solvent_surface_coverage, 
        head_layer_area_per_molecule=area_per_molecule,
        head_layer_roughness=roughness
    )
    
On creation, the area per molecule and roughness above both the head and tail layers can be constrained to be the same. 
These constraints can be addded by setting :code:`dppc.constrain_apm = True` or :code:`dppc.conformal_roughness = True`. 
Furthermore, as shown in the `surfactant monolayer tutorial`_ the conformal roughness can be defined by that of the subphase. 

The use of the :py:class:`SurfactantLayer` in multiple contrast data analysis is shown in a `multiple contrast tutorial`_. 


.. _`simple fitting tutorial`: ../tutorials/simple_fitting.html
.. _`tutorial`: ../tutorials/repeating.html
.. _`surfactant monolayer tutorial`: ../tutorials/monolayer.html
.. _`multiple contrast tutorial`: ../tutorials/multi_contrast.html