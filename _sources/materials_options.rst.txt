Types of material
=================

In order to support a wide range of applications (and to build complex `items`_) there are a few different types of material that can be utilised in :py:mod:`EasyReflectometry`. 
These can include constraints or enabel the user to define the material based on chemical or physical properties. 
Full API documentation for the :py:mod:`EasyReflectoemtry.sample.material` mdoule is also available, but here we will give some simple uses for them. 

:py:class:`Material`
--------------------

The simplest type of material that is available is the :py:class:`Material`.
This allows the user to define a single type of material, with a real and imaginary component to the scattering length density. 
The construction of a :py:class:`Material` is achieved as shown below. 

.. code-block:: python 

    from EasyReflectometry.sample.material import Material

    b = Material.from_pars(6.908, -0.278, 'Boron')

The above object will have the properties of :py:attr:`sld` and :py:attr:`isld`, which will have values of :code:`6.908 1 / angstrom ** 2` and :code:`-0.278 1 / angstrom ** 2` respectively. 
As is shown in the `tutorials`_, a material can be used to construct a :py:class:`Layer` from which `slab models`_ are created.

:py:class:`MaterialMixture`
---------------------------

Sometimes it is desirable to have a layer that consists of two materials in some ratio.
An example of this is shown in the `solvation tutorial`_, where a polymer film solvated with D:sub:`2`O is modelled. 
To produce a material that is described by such a mixture, there is the :py:class:`MaterialMixture` material option. 
This is constructed from two constituent materials and the fractional amount of the second in the first. 
So to produce a material that is 20 % D:sub:`2`O in a polymer, the following is used. 

.. code-block:: python

    from EasyReflectometry.sample.material import Material, MaterialMixture

    polymer = Material.from_pars(2., 0., 'Polymer')
    d2o = Material.from_pars(6.36, 0, 'D2O')

    solvated_polymer = MaterialMixture.from_pars(polymer, 
                                                 d2o, 
                                                 0.2, 
                                                 'Solvated Polymer')

For the :py:attr:`solvated_polymer` object, the :py:attr:`sld` will be :code:`2.872 1 / angstrom ** 2` (the weighted average of the two scattering length densities). 
The :py:class:`MaterialMixture` includes a constraint such that if the value of either constituent scattering length densities (both real and imaginary components) or the fraction changes, then the resulting material :py:attr:`sld` and :py:attr:`isld` will change appropriately. 

.. _`items`: ./library.html
.. _`tutorials`: ./tutorials.html
.. _`slab models`: https://www.reflectometry.org/isis_school/3_reflectometry_slab_models/the_slab_model.html
.. _`solvation tutorial`: ./solvation.html