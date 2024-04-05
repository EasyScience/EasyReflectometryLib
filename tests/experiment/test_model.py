"""
Tests for Model class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'


import unittest
from unittest.mock import MagicMock

import numpy as np
import pytest
from numpy.testing import assert_equal

from EasyReflectometry.calculators import CalculatorFactory
from EasyReflectometry.calculators.wrapper_base import constant_resolution_function
from EasyReflectometry.calculators.wrapper_base import linear_spline_resolution_function
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.sample import Layer
from EasyReflectometry.sample import LayerCollection
from EasyReflectometry.sample import Material
from EasyReflectometry.sample import Multilayer
from EasyReflectometry.sample import RepeatingMultilayer
from EasyReflectometry.sample import Sample
from EasyReflectometry.sample import SurfactantLayer


class TestModel(unittest.TestCase):
    def test_default(self):
        p = Model.default()
        assert_equal(p.name, 'EasyModel')
        assert_equal(p.interface, None)
        assert_equal(p.sample.name, 'EasySample')
        assert_equal(p.scale.display_name, 'scale')
        assert_equal(str(p.scale.unit), 'dimensionless')
        assert_equal(p.scale.value.value.magnitude, 1.0)
        assert_equal(p.scale.min, 0.0)
        assert_equal(p.scale.max, np.Inf)
        assert_equal(p.scale.fixed, True)
        assert_equal(p.background.display_name, 'background')
        assert_equal(str(p.background.unit), 'dimensionless')
        assert_equal(p.background.value.value.magnitude, 1.0e-8)
        assert_equal(p.background.min, 0.0)
        assert_equal(p.background.max, np.Inf)
        assert_equal(p.background.fixed, True)
        assert p._resolution_function(1) == 5.0
        assert p._resolution_function(100) == 5.0

    def test_from_pars(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, o2, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel')
        assert_equal(mod.name, 'newModel')
        assert_equal(mod.interface, None)
        assert_equal(mod.sample.name, 'myModel')
        assert_equal(mod.scale.display_name, 'scale')
        assert_equal(str(mod.scale.unit), 'dimensionless')
        assert_equal(mod.scale.value.value.magnitude, 2.0)
        assert_equal(mod.scale.min, 0.0)
        assert_equal(mod.scale.max, np.Inf)
        assert_equal(mod.scale.fixed, True)
        assert_equal(mod.background.display_name, 'background')
        assert_equal(str(mod.background.unit), 'dimensionless')
        assert_equal(mod.background.value.value.magnitude, 1.0e-5)
        assert_equal(mod.background.min, 0.0)
        assert_equal(mod.background.max, np.Inf)
        assert_equal(mod.background.fixed, True)
        assert mod._resolution_function(1) == 2.0
        assert mod._resolution_function(100) == 2.0

    def test_add_item(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        surfactant = SurfactantLayer.default()
        multilayer = Multilayer.default()
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel')
        assert_equal(len(mod.sample), 1)
        mod.add_item(o2)
        assert_equal(len(mod.sample), 2)
        assert_equal(mod.sample[1].name, 'oneLayerItem2')
        assert_equal(issubclass(mod.sample[1].__class__, RepeatingMultilayer), True)
        mod.add_item(surfactant)
        assert_equal(len(mod.sample), 3)
        mod.add_item(multilayer)
        assert_equal(len(mod.sample), 4)

    def test_add_item_exception(self):
        # When
        mod = Model.default()

        # Then Expect
        with pytest.raises(ValueError):
            mod.add_item('not an assembly')

    def test_add_item_with_interface_refnx(self):
        interface = CalculatorFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    def test_add_item_with_interface_refl1d(self):
        interface = CalculatorFactory()
        interface.switch('refl1d')
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    # def test_add_item_with_interface_bornagain(self):
    #     interface = CalculatorFactory()
    #     interface.switch('BornAgain')
    #     m1 = Material.from_pars(6.908, 0.278, 'Boron')
    #     m2 = Material.from_pars(0.487, 0.000, 'Potassium')
    #     l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
    #     l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
    #     ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
    #     ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
    #     o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
    #     o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
    #     d = Sample.from_pars(o1, name='myModel')
    #     mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
    #     assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
    #     mod.add_item(o2)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
    #     assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    def test_duplicate_item(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel')
        assert_equal(len(mod.sample), 1)
        mod.add_item(o2)
        assert_equal(len(mod.sample), 2)
        mod.duplicate_item(1)
        assert_equal(len(mod.sample), 3)
        assert_equal(mod.sample[2].name, 'oneLayerItem2 duplicate')
        assert_equal(issubclass(mod.sample[2].__class__, RepeatingMultilayer), True)

    def test_duplicate_item_with_interface_refnx(self):
        interface = CalculatorFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        mod.duplicate_item(1)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 3)

    def test_duplicate_item_with_interface_refl1d(self):
        interface = CalculatorFactory()
        interface.switch('refl1d')
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        mod.duplicate_item(1)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 3)

    # def test_duplicate_item_with_interface_bornagain(self):
    #     interface = CalculatorFactory()
    #     interface.switch('BornAgain')
    #     m1 = Material.from_pars(6.908, 0.278, 'Boron')
    #     m2 = Material.from_pars(0.487, 0.000, 'Potassium')
    #     l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
    #     l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
    #     ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
    #     ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
    #     o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
    #     o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
    #     d = Sample.from_pars(o1, name='myModel')
    #     mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
    #     mod.add_item(o2)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
    #     mod.duplicate_item(1)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 3)

    def test_remove_item(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel')
        assert_equal(len(mod.sample), 1)
        mod.add_item(o2)
        assert_equal(len(mod.sample), 2)
        mod.remove_item(0)
        assert_equal(len(mod.sample), 1)

    def test_remove_item_with_interface_refnx(self):
        interface = CalculatorFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.remove_item(0)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    def test_remove_item_with_interface_refl1d(self):
        interface = CalculatorFactory()
        interface.switch('refl1d')
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection.from_pars(l1, l2, name='twoLayer1')
        ls2 = LayerCollection.from_pars(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Sample.from_pars(o1, name='myModel')
        resolution_function = constant_resolution_function(2.0)
        mod = Model.from_pars(d, 2, 1e-5, resolution_function, 'newModel', interface=interface)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
        mod.remove_item(0)
        assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
        assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    # def test_remove_item_with_interface_bornagain(self):
    #     interface = CalculatorFactory()
    #     interface.switch('BornAgain')
    #     m1 = Material.from_pars(6.908, 0.278, 'Boron')
    #     m2 = Material.from_pars(0.487, 0.000, 'Potassium')
    #     l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
    #     l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
    #     ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
    #     ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
    #     o1 = RepeatingMultilayer.from_pars(ls1, 2.0, 'twoLayerItem1')
    #     o2 = RepeatingMultilayer.from_pars(ls2, 1.0, 'oneLayerItem2')
    #     d = Sample.from_pars(o1, name='myModel')
    #     mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
    #     assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
    #     mod.add_item(o2)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 2)
    #     assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)
    #     mod.remove_item(0)
    #     assert_equal(len(mod.interface()._wrapper.storage['item']), 1)
    #     assert_equal(len(mod.interface()._wrapper.storage['layer']), 2)

    def test_uid(self):
        p = Model.default()
        assert_equal(p.uid, p._borg.map.convert_id_to_key(p))

    def test_set_resolution_function(self):
        mock_resolution_function = MagicMock()
        model = Model.default()
        model.set_resolution_function(mock_resolution_function)
        assert model._resolution_function == mock_resolution_function

    def test_repr(self):
        model = Model.default()

        assert (
            model.__repr__()
            == 'EasyModel:\n  scale: 1.0\n  background: 1.0e-08\n  resolution: 5.0 %\n  sample:\n    EasySample:\n    - EasyMultilayer:\n        EasyLayers:\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n    - EasyMultilayer:\n        EasyLayers:\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n'  # noqa: E501
        )

    def test_repr_resolution_function(self):
        resolution_function = linear_spline_resolution_function([0, 10], [0, 10])
        model = Model.default()
        model.set_resolution_function(resolution_function)
        assert (
            model.__repr__()
            == 'EasyModel:\n  scale: 1.0\n  background: 1.0e-08\n  resolution: function of Q\n  sample:\n    EasySample:\n    - EasyMultilayer:\n        EasyLayers:\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n    - EasyMultilayer:\n        EasyLayers:\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n        - EasyLayer:\n            material:\n              EasyMaterial:\n                sld: 4.186e-6 1 / angstrom ** 2\n                isld: 0.000e-6 1 / angstrom ** 2\n            thickness: 10.000 angstrom\n            roughness: 3.300 angstrom\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        resolution_function = linear_spline_resolution_function([0, 10], [0, 10])
        interface = CalculatorFactory()
        model = Model.default(interface)
        model.set_resolution_function(resolution_function)
        surfactant = SurfactantLayer.default()
        model.add_item(surfactant)
        multilayer = Multilayer.default()
        model.add_item(multilayer)
        repeating = RepeatingMultilayer.default()
        model.add_item(repeating)
        src_dict = model.as_dict()
        model_from_dict = Model.from_dict(src_dict)
        assert model.as_data_dict() == model_from_dict.as_data_dict()
        assert model._resolution_function(5.5) == model_from_dict._resolution_function(5.5)
