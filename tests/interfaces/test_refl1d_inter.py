__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from EasyReflectometry.interfaces.refl1d import Refl1d
from EasyReflectometry.sample.material import Material


class TestRefl1d(unittest.TestCase):

    def test_init(self):
        p = Refl1d()
        assert_equal(list(p.calculator.storage.keys()),
                     ['material', 'layer', 'item', 'model'])
        assert_equal(p._material_link['sld'], 'rho')
        assert_equal(p._material_link['isld'], 'irho')
        assert_equal(p._layer_link['thickness'], 'thickness')
        assert_equal(p._layer_link['roughness'], 'interface')
        assert_equal(p._item_link['repetitions'], 'repeat')
        assert_equal(p._model_link['scale'], 'scale')
        assert_equal(p._model_link['background'], 'bkg')
        assert_equal(p._model_link['resolution'], 'dq')
        assert_equal(p.name, 'refl1d')

    def test_fit_func(self):
        p = Refl1d()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', rho=0.000, irho=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', rho=2.000, irho=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', rho=4.000, irho=0.000)
        p.calculator.create_model()
        p.calculator.update_model('model', bkg=1e-7, dq=5.0)
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thickness=10, interface=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', interface=1.0)
        p.calculator.create_item('Item')
        p.calculator.add_layer_to_item('Layer1', 'Item')
        p.calculator.add_layer_to_item('Layer2', 'Item')
        p.calculator.add_layer_to_item('Layer3', 'Item')
        p.calculator.add_item('Item')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            1.0000001e+00, 2.1749216e-03, 1.1433942e-04, 1.9337269e-05, 4.9503970e-06,
            1.5447182e-06, 5.4663919e-07, 2.2701724e-07, 1.2687053e-07, 1.0188127e-07
        ]
        assert_almost_equal(p.fit_func(q), expected)

    def test_calculate2(self):
        p = Refl1d()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', rho=0.000, irho=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', rho=2.000, irho=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', rho=4.000, irho=0.000)
        p.calculator.create_model()
        p.calculator.update_model('model', bkg=1e-7, dq=5.0)
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thickness=10, interface=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', interface=1.0)
        p.calculator.create_item('Item1')
        p.calculator.add_layer_to_item('Layer1', 'Item1')
        p.calculator.create_item('Item2')
        p.calculator.add_layer_to_item('Layer2', 'Item2')
        p.calculator.add_layer_to_item('Layer1', 'Item2')
        p.calculator.create_item('Item3')
        p.calculator.add_layer_to_item('Layer3', 'Item3')
        p.calculator.add_item('Item1')
        p.calculator.add_item('Item2')
        p.calculator.add_item('Item3')
        p.calculator.update_item('Item2', repeat=10)
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            1.0000001e+00, 1.8923350e-05, 1.2274125e-04, 2.4073165e-06, 6.7232911e-06,
            8.3051185e-07, 1.1546344e-06, 4.1351306e-07, 3.5132221e-07, 2.5347996e-07
        ]
        assert_almost_equal(p.fit_func(q), expected)

    def test_sld_profile(self):
        p = Refl1d()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', rho=0.000, irho=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', rho=2.000, irho=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', rho=4.000, irho=0.000)
        p.calculator.create_model()
        p.calculator.update_model('model', bkg=1e-7, dq=5.0)
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thickness=10, interface=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', interface=1.0)
        p.calculator.create_item('Item')
        p.calculator.add_layer_to_item('Layer1', 'Item')
        p.calculator.add_layer_to_item('Layer2', 'Item')
        p.calculator.add_layer_to_item('Layer3', 'Item')
        p.calculator.add_item('Item')
        assert_almost_equal(p.sld_profile()[1][0], 0)
        assert_almost_equal(p.sld_profile()[1][-1], 4)
