Layers
======

Similar to a range of different `materials`_, there are a few different ways that a layer can be defined in :py:mod:`EasyReflectometry`.

:py:class:`Layer`
-----------------

The :py:class:`Layer` is the simplest possible type of layer, taking a :py:class:`Material` and two floats associated with the thickness and upper (that is closer to the source of the incident radiation) roughness. 
So we construct a :py:class:`Layer` as follows for a 100 Å thick layer of boron with a roughness of 10 Å. 

.. code-block:: python

    from EasyReflectometry.sample import Material, Layer

    b = Material.from_pars(6.908, -0.278, 'Boron')
    boron_layer = Layer.from_pars(b, 100, 10, 'Boron Layer')

This type of layer is used extensively in the `tutorials`_

:py:class:`LayerApm`
--------------------

The :py:class:`LayerApm` layer type is the fundation of the :py:class:`SurfactantLayer` item type (further information on this can be foundin the `item library`_).
The purpose of the :py:class:`LayerApm` is to allow a layer to be defined in terms of the chemical formula of the material and the area per molecule of the layer. 
The area per molecule is a common description of surface density in the surfactant monolayer and bilayer community. 

We can construct a 10 Å thick :py:class:`LayerApm` of phosphatidylcholine, with an area per molecule of 48 Å squared and a roughness of 3 Å that has 20 % solvation with D2O using the following.

.. code-block:: python

    from EasyReflectometry.sample import Material, LayerApm

    d2o = Material.from_pars(6.36, 0, 'D2O')

    pc_formula = 'C10H18NO8P'
    pc = LayerApm.from_pars(pc_formula, 10, d2o, 0.2, 48, 3, name='PC Layer')

It is expected that the typical user will not interface directly with the :py:class:`LayerApm` item type, but instead the :py:class:`SurfactantLayer` `item type`_ will be used instead. 

.. _`materials`: ./material_library.html
.. _`tutorials`: ./tutorials.html
.. _`item library`: ./item_library.html