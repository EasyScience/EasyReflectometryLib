__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest

import numpy as np
from numpy.testing import (
    assert_almost_equal,
    assert_equal,
)

from EasyReflectometry.interfaces.refnx import Refnx
from EasyReflectometry.sample.material import Material


class TestRefnx(unittest.TestCase):

    def test_init(self):
        p = Refnx()
        assert_equal(list(p.calculator.storage.keys()),
                     ['material', 'layer', 'item', 'model'])
        assert_equal(p._material_link['sld'], 'real')
        assert_equal(p._material_link['isld'], 'imag')
        assert_equal(p._layer_link['thickness'], 'thick')
        assert_equal(p._layer_link['roughness'], 'rough')
        assert_equal(p._item_link['repetitions'], 'repeats')
        assert_equal(p._model_link['scale'], 'scale')
        assert_equal(p._model_link['background'], 'bkg')
        assert_equal(p._model_link['resolution'], 'dq')
        assert_equal(p.name, 'refnx')

    def test_fit_func(self):
        p = Refnx()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', real=0.000, imag=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', real=2.000, imag=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', real=4.000, imag=0.000)
        p.calculator.create_model('MyModel')
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thick=10, rough=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', rough=1.0)
        p.calculator.create_item('Item')
        p.calculator.add_layer_to_item('Layer1', 'Item')
        p.calculator.add_layer_to_item('Layer2', 'Item')
        p.calculator.add_layer_to_item('Layer3', 'Item')
        p.calculator.add_item('Item', 'MyModel')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            9.99956517e-01, 2.16286891e-03, 1.14086254e-04, 1.93031759e-05,
            4.94188894e-06, 1.54191953e-06, 5.45592112e-07, 2.26619392e-07,
            1.26726993e-07, 1.01842852e-07
        ]
        assert_almost_equal(p.fit_func(q, 'MyModel'), expected)

    def test_calculate2(self):
        p = Refnx()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', real=0.000, imag=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', real=2.000, imag=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', real=4.000, imag=0.000)
        p.calculator.create_model('MyModel')
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thick=10, rough=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', rough=1.0)
        p.calculator.create_item('Item1')
        p.calculator.add_layer_to_item('Layer1', 'Item1')
        p.calculator.create_item('Item2')
        p.calculator.add_layer_to_item('Layer2', 'Item2')
        p.calculator.add_layer_to_item('Layer1', 'Item2')
        p.calculator.create_item('Item3')
        p.calculator.add_layer_to_item('Layer3', 'Item3')
        p.calculator.add_item('Item1', 'MyModel')
        p.calculator.add_item('Item2', 'MyModel')
        p.calculator.add_item('Item3', 'MyModel')
        p.calculator.update_item('Item2', repeats=10)
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            9.9995652e-01, 1.7096697e-05, 1.2253047e-04, 2.4026928e-06, 6.7117546e-06,
            8.3209877e-07, 1.1512901e-06, 4.1468151e-07, 3.4981523e-07, 2.5424356e-07
        ]
        assert_almost_equal(p.fit_func(q, 'MyModel'), expected)

    def test_sld_profile(self):
        p = Refnx()
        p.calculator.create_material('Material1')
        p.calculator.update_material('Material1', real=0.000, imag=0.000)
        p.calculator.create_material('Material2')
        p.calculator.update_material('Material2', real=2.000, imag=0.000)
        p.calculator.create_material('Material3')
        p.calculator.update_material('Material3', real=4.000, imag=0.000)
        p.calculator.create_model('MyModel')
        p.calculator.create_layer('Layer1')
        p.calculator.assign_material_to_layer('Material1', 'Layer1')
        p.calculator.create_layer('Layer2')
        p.calculator.assign_material_to_layer('Material2', 'Layer2')
        p.calculator.update_layer('Layer2', thick=10, rough=1.0)
        p.calculator.create_layer('Layer3')
        p.calculator.assign_material_to_layer('Material3', 'Layer3')
        p.calculator.update_layer('Layer3', rough=1.0)
        p.calculator.create_item('Item')
        p.calculator.add_layer_to_item('Layer1', 'Item')
        p.calculator.add_layer_to_item('Layer2', 'Item')
        p.calculator.add_layer_to_item('Layer3', 'Item')
        p.calculator.add_item('Item', 'MyModel')
        assert_almost_equal(p.sld_profile('MyModel')[1][0], 0)
        assert_almost_equal(p.sld_profile('MyModel')[1][-1], 4)
