__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Item class module
"""

import unittest

from numpy.testing import assert_equal
from numpy.testing import assert_raises

from EasyReflectometry.calculators.factory import CalculatorFactory
from EasyReflectometry.sample.assemblies.multilayer import Multilayer
from EasyReflectometry.sample.elements.layers.layer import Layer
from EasyReflectometry.sample.elements.layer_collection import LayerCollection
from EasyReflectometry.sample.elements.materials.material import Material


class TestMultilayer(unittest.TestCase):

    def test_default(self):
        p = Multilayer.default()
        assert_equal(p.name, 'EasyMultilayer')
        assert_equal(p._type, 'Multi-layer')
        assert_equal(p.interface, None)
        assert_equal(len(p.layers), 2)
        assert_equal(p.layers.name, 'EasyLayers')

    def test_from_pars(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        l = LayerCollection.from_pars(p, q, name='twoLayer')
        o = Multilayer.from_pars(l, 'twoLayerItem')
        assert_equal(o.name, 'twoLayerItem')
        assert_equal(o._type, 'Multi-layer')
        assert_equal(o.interface, None)
        assert_equal(o.layers.name, 'twoLayer')

    def test_from_pars_layer(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        o = Multilayer.from_pars(p, 'twoLayerItem')
        assert_equal(o.name, 'twoLayerItem')
        assert_equal(o.interface, None)
        assert_equal(o.layers.name, 'thinBoron')

    def test_from_pars_layer_list(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 15.0, 2.0, 'layerPotassium')
        o = Multilayer.from_pars([p, q], 'twoLayerItem')
        assert_equal(o.name, 'twoLayerItem')
        assert_equal(o.interface, None)
        assert_equal(o.layers.name, 'thinBoron/layerPotassium')

    def test_add_layer(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        o = Multilayer.from_pars(p, 'twoLayerItem')
        assert_equal(len(o.layers), 1)
        o.add_layer(q)
        assert_equal(len(o.layers), 2)
        assert_equal(o.layers[1].name, 'thickPotassium')

    def test_add_layer_with_interface_refnx(self):
        interface = CalculatorFactory()
        interface.switch('refnx')
        m = Material.from_pars(6.908, -0.278, 'Boron', interface=interface)
        k = Material.from_pars(0.487, 0.000, 'Potassium', interface=interface)
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron', interface=interface)
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium', interface=interface)
        o = Multilayer.from_pars(p, 'twoLayerItem', interface=interface)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 1)
        o.add_layer(q)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 2)
        assert_equal(
            o.interface()._wrapper.storage['item'][o.uid].components[1].thick.value,
            50.)

    def test_duplicate_layer(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        o = Multilayer.from_pars(p, 'twoLayerItem')
        assert_equal(len(o.layers), 1)
        o.add_layer(q)
        assert_equal(len(o.layers), 2)
        o.duplicate_layer(1)
        assert_equal(len(o.layers), 3)
        assert_equal(o.layers[1].name, 'thickPotassium')
        assert_equal(o.layers[2].name, 'thickPotassium duplicate')

    def test_duplicate_layer_with_interface_refnx(self):
        interface = CalculatorFactory()
        interface.switch('refnx')
        m = Material.from_pars(6.908, -0.278, 'Boron', interface=interface)
        k = Material.from_pars(0.487, 0.000, 'Potassium', interface=interface)
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron', interface=interface)
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium', interface=interface)
        o = Multilayer.from_pars(p, 'twoLayerItem', interface=interface)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 1)
        o.add_layer(q)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 2)
        assert_equal(
            o.interface()._wrapper.storage['item'][o.uid].components[1].thick.value,
            50.)
        o.duplicate_layer(1)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 3)
        assert_equal(
            o.interface()._wrapper.storage['item'][o.uid].components[2].thick.value,
            50.)
        assert_raises(
            AssertionError, assert_equal,
            o.interface()._wrapper.storage['item'][o.uid].components[1].name,
            o.interface()._wrapper.storage['item'][o.uid].components[2].name)

    def test_remove_layer(self):
        m = Material.from_pars(6.908, -0.278, 'Boron')
        k = Material.from_pars(0.487, 0.000, 'Potassium')
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron')
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium')
        o = Multilayer.from_pars(p, 'twoLayerItem')
        assert_equal(len(o.layers), 1)
        o.add_layer(q)
        assert_equal(len(o.layers), 2)
        assert_equal(o.layers[1].name, 'thickPotassium')
        o.remove_layer(1)
        assert_equal(len(o.layers), 1)
        assert_equal(o.layers[0].name, 'thinBoron')

    def test_remove_layer_with_interface_refnx(self):
        interface = CalculatorFactory()
        interface.switch('refnx')
        m = Material.from_pars(6.908, -0.278, 'Boron', interface=interface)
        k = Material.from_pars(0.487, 0.000, 'Potassium', interface=interface)
        p = Layer.from_pars(m, 5.0, 2.0, 'thinBoron', interface=interface)
        q = Layer.from_pars(k, 50.0, 1.0, 'thickPotassium', interface=interface)
        o = Multilayer.from_pars(p, name='twoLayerItem', interface=interface)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 1)
        o.add_layer(q)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 2)
        assert_equal(o.layers[1].name, 'thickPotassium')
        o.remove_layer(1)
        assert_equal(len(o.interface()._wrapper.storage['item'][o.uid].components), 1)
        assert_equal(o.layers[0].name, 'thinBoron')

    def test_repr(self):
        p = Multilayer.default()
        assert p.__repr__(
        ) == 'EasyMultilayer:\n  EasyLayers:\n  - EasyLayer:\n      material:\n        EasyMaterial:\n          sld: 4.186e-6 1 / angstrom ** 2\n          isld: 0.000e-6 1 / angstrom ** 2\n      thickness: 10.000 angstrom\n      roughness: 3.300 angstrom\n  - EasyLayer:\n      material:\n        EasyMaterial:\n          sld: 4.186e-6 1 / angstrom ** 2\n          isld: 0.000e-6 1 / angstrom ** 2\n      thickness: 10.000 angstrom\n      roughness: 3.300 angstrom\n'

    def test_dict_round_trip(self):
        p = Multilayer.default()
        q = Multilayer.from_dict(p.as_dict())
        assert p.as_data_dict() == q.as_data_dict()