Layers
======

Similar to a range of different `materials`_, there are a few different ways that a layer can be defined in :py:mod:`EasyReflectometry`.

:py:class:`Layer`
-----------------

The :py:class:`Layer` is the simplest possible type of layer, taking a :py:class:`Material` and two floats associated with the thickness and upper (that is closer to the source of the incident radiation) roughness. 
So we construct a :py:class:`Layer` as follows for a 100 Å thick layer of boron with a roughness of 10 Å. 

.. code-block:: python

    from EasyReflectometry.sample import Material
    from EasyReflectometry.sample import Layer

    b = Material.from_pars(
        sld=6.908,
        isld=-0.278,
        'Boron'
    )
    boron_layer = Layer.from_pars(
        material=b,
        thickness=100, 
        roughness=10,
        name='Boron Layer'
    )

This type of layer is used extensively in the `tutorials`_

:py:class:`LayerApm`
--------------------

The :py:class:`LayerApm` layer type is the fundation of the :py:class:`SurfactantLayer` assemblies type (further information on this can be found in the `assemblies library`_).
The purpose of the :py:class:`LayerApm` is to allow a layer to be defined in terms of the chemical formula of the material and the area per molecule of the layer. 
The area per molecule is a common description of surface density in the surfactant monolayer and bilayer community. 

We can construct a 10 Å thick :py:class:`LayerApm` of phosphatidylcholine, with an area per molecule of 48 Å squared and a roughness of 3 Å that has 20 % solvent surface coverage with D2O using the following.

.. code-block:: python

    from EasyReflectometry.sample import Material
    from EasyReflectometry.sample import LayerApm

    d2o = Material.from_pars(6.36, 0, 'D2O')

    pc_formula = 'C10H18NO8P'
    pc = LayerApm.from_pars(
        chemical_formula=pc_formula, 
        thickness=10, 
        solvent=d2o, 
        solvation=.2,
        area_per_molecule=48, 
        roughness=3,
        name='PC Layer'
    )

It is expected that the typical user will not interface directly with the :py:class:`LayerApm` assembly type, but instead the :py:class:`SurfactantLayer` `assemblies library`_ will be used instead. 

.. _`materials`: ./material_library.html
.. _`tutorials`: ../tutorials/tutorials.html
.. _`assemblies library`: ./assemblies_library.html