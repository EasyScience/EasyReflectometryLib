__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Calculators.refnx import Refnx
from refnx import reflect


class TestRefnx(unittest.TestCase):
    def test_init(self):
        p = Refnx()
        assert_equal(list(p.storage.keys()), ['material', 'layer', 'item', 'model'])
        assert_equal(issubclass(p.storage['material'].__class__, dict), True)

    def test_reset_storage(self):
        p = Refnx()
        p.storage['material']['a'] = 1
        assert_equal(p.storage['material']['a'], 1)
        p.reset_storage()
        assert_equal(p.storage['material'], {})

    def test_create_material(self):
        p = Refnx()
        p.create_material('Si')
        assert_equal(list(p.storage['material'].keys()), ['Si'])
        assert_almost_equal(p.storage['material']['Si'].real.value, 0.0)
        assert_almost_equal(p.storage['material']['Si'].imag.value, 0.0)
        assert_equal(p.storage['material']['Si'].name, 'Si')

    def test_update_material(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.storage['material']['B'].real.value, 6.908)
        assert_almost_equal(p.storage['material']['B'].imag.value, -0.278)

    def test_get_material_value(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.get_material_value('B', 'real'), 6.908)
        assert_almost_equal(p.get_material_value('B', 'imag'), -0.278)

    def test_create_layer(self):
        p = Refnx()
        p.create_layer('Si')
        assert_equal(list(p.storage['layer'].keys()), ['Si'])
        assert_almost_equal(p.storage['layer']['Si'].thick.value, 0)
        assert_almost_equal(p.storage['layer']['Si'].rough.value, 0)
        assert_almost_equal(p.storage['layer']['Si'].sld.real.value, 0)
        assert_almost_equal(p.storage['layer']['Si'].sld.imag.value, 0)

    def test_update_layer(self):
        p = Refnx()
        p.create_layer('Si')
        p.update_layer('Si', thick=10, rough=5)
        assert_almost_equal(p.storage['layer']['Si'].thick.value, 10)
        assert_almost_equal(p.storage['layer']['Si'].rough.value, 5)

    def test_get_layer_value(self):
        p = Refnx()
        p.create_layer('Si')
        p.update_layer('Si', thick=10, rough=5)
        assert_almost_equal(p.get_layer_value('Si', 'thick'), 10)
        assert_almost_equal(p.get_layer_value('Si', 'rough'), 5)

    def test_create_item(self):
        p = Refnx()
        p.create_item('SiNi')
        assert_equal(list(p.storage['item'].keys()), ['SiNi'])
        assert_almost_equal(p.storage['item']['SiNi'].repeats.value, 1)

    def test_update_item(self):
        p = Refnx()
        p.create_item('SiNi')
        p.update_item('SiNi', repeats=10)
        assert_almost_equal(p.storage['item']['SiNi'].repeats.value, 10)
    
    def test_get_item_value(self):
        p = Refnx()
        p.create_item('SiNi')
        p.update_item('SiNi', repeats=10)
        assert_almost_equal(p.get_item_value('SiNi', 'repeats'), 10)

    def test_create_model(self):
        p = Refnx()
        p.create_model()
        assert_equal(isinstance(p.storage['model'], reflect.ReflectModel), True)

    def test_update_model(self):
        p = Refnx()
        p.create_model()
        p.update_model('model', scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.storage['model'].scale.value, 2)
        assert_almost_equal(p.storage['model'].bkg.value, 1e-3)
        assert_almost_equal(p.storage['model'].dq.value, 2.0)

    def test_get_model_value(self):
        p = Refnx()
        p.create_model()
        p.update_model('model', scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.get_model_value('model', 'scale'), 2)
        assert_almost_equal(p.get_model_value('model', 'bkg'), 1e-3)
        assert_almost_equal(p.get_model_value('model', 'dq'), 2.0)

    def test_assign_material_to_layer(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        assert_almost_equal(p.storage['layer']['B_layer'].sld.real.value, 6.908)
        assert_almost_equal(p.storage['layer']['B_layer'].sld.imag.value, -0.278)

    def test_add_layer_to_item(self): 
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        assert_equal(len(p.storage['item']['B_item']), 0)
        p.add_layer_to_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item']), 1)
        assert_equal(p.storage['item']['B_item'][0].name, 'B_layer')

    def test_add_item(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        p.create_model()
        assert_equal(len(p.storage['model'].structure.components), 0)
        p.add_item('B_item')
        assert_equal(len(p.storage['model'].structure.components), 1)
        assert_equal(p.storage['model'].structure.components[0].name, 'B_item')

    def test_remove_layer_from_item(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item']), 1)
        p.remove_layer_from_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item']), 0)

    def test_remove_item(self):
        p = Refnx()
        p.create_material('B')
        p.update_material('B', real=6.908, imag=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        p.create_model()
        p.add_item('B_item')
        assert_equal(len(p.storage['model'].structure.components), 1)
        p.remove_item('B_item')
        assert_equal(len(p.storage['model'].structure.components), 0)

    def test_calculate(self):
        p = Refnx()
        p.create_material('Material1')
        p.update_material('Material1', real=0.000, imag=0.000)
        p.create_material('Material2')
        p.update_material('Material2', real=2.000, imag=0.000)
        p.create_material('Material3')
        p.update_material('Material3', real=4.000, imag=0.000)
        p.create_model()
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thick=10, rough=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', rough=1.0)
        p.create_item('Item')
        p.add_layer_to_item('Layer1', 'Item')
        p.add_layer_to_item('Layer2', 'Item')
        p.add_layer_to_item('Layer3', 'Item')
        p.add_item('Item')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            9.99956517e-01, 2.16286891e-03, 1.14086254e-04, 1.93031759e-05,
            4.94188894e-06, 1.54191953e-06, 5.45592112e-07, 2.26619392e-07,
            1.26726993e-07, 1.01842852e-07
        ]
        assert_almost_equal(p.calculate(q), expected)

    def test_calculate2(self):
        p = Refnx()
        p.create_material('Material1')
        p.update_material('Material1', real=0.000, imag=0.000)
        p.create_material('Material2')
        p.update_material('Material2', real=2.000, imag=0.000)
        p.create_material('Material3')
        p.update_material('Material3', real=4.000, imag=0.000)
        p.create_model()
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thick=10, rough=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', rough=1.0)
        p.create_item('Item1')
        p.add_layer_to_item('Layer1', 'Item1')
        p.create_item('Item2')
        p.add_layer_to_item('Layer2', 'Item2')
        p.add_layer_to_item('Layer1', 'Item2')
        p.create_item('Item3')
        p.add_layer_to_item('Layer3', 'Item3')
        p.add_item('Item1')
        p.add_item('Item2')
        p.add_item('Item3')
        p.update_item('Item2', repeats=10)
        q = np.linspace(0.001, 0.3, 10)
        expected = [9.9995652e-01, 1.7096697e-05, 1.2253047e-04, 2.4026928e-06,
                  6.7117546e-06, 8.3209877e-07, 1.1512901e-06, 4.1468151e-07,
                  3.4981523e-07, 2.5424356e-07]
        assert_almost_equal(p.calculate(q), expected)
        assert_almost_equal(p.calculate(q), expected)

    def test_sld_profile(self):
        p = Refnx()
        p.create_material('Material1')
        p.update_material('Material1', real=0.000, imag=0.000)
        p.create_material('Material2')
        p.update_material('Material2', real=2.000, imag=0.000)
        p.create_material('Material3')
        p.update_material('Material3', real=4.000, imag=0.000)
        p.create_model()
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thick=10, rough=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', rough=1.0)
        p.create_item('Item')
        p.add_layer_to_item('Layer1', 'Item')
        p.add_layer_to_item('Layer2', 'Item')
        p.add_layer_to_item('Layer3', 'Item')
        p.add_item('Item')
        assert_almost_equal(p.sld_profile()[1][0], 0)
        assert_almost_equal(p.sld_profile()[1][-1], 4)
