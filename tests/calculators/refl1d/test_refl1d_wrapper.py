__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refl1d class module
"""

import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from EasyReflectometry.calculators.refl1d.wrapper import Refl1dWrapper


class TestRefl1d(unittest.TestCase):

    def test_init(self):
        p = Refl1dWrapper()
        assert_equal(list(p.storage.keys()), ['material', 'layer', 'item', 'model'])
        assert_equal(issubclass(p.storage['material'].__class__, dict), True)

    def test_reset_storage(self):
        p = Refl1dWrapper()
        p.storage['material']['a'] = 1
        assert_equal(p.storage['material']['a'], 1)
        p.reset_storage()
        assert_equal(p.storage['material'], {})

    def test_create_material(self):
        p = Refl1dWrapper()
        p.create_material('Si')
        assert_equal(list(p.storage['material'].keys()), ['Si'])
        assert_almost_equal(p.storage['material']['Si'].rho.value, 0.0)
        assert_almost_equal(p.storage['material']['Si'].irho.value, 0.0)
        assert_equal(p.storage['material']['Si'].name, 'Si')

    def test_update_material(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.storage['material']['B'].rho.value, 6.908)
        assert_almost_equal(p.storage['material']['B'].irho.value, -0.278)

    def test_get_material_value(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        assert_equal(list(p.storage['material'].keys()), ['B'])
        assert_almost_equal(p.get_material_value('B', 'rho'), 6.908)
        assert_almost_equal(p.get_material_value('B', 'irho'), -0.278)

    def test_create_layer(self):
        p = Refl1dWrapper()
        p.create_layer('Si')
        assert_equal(list(p.storage['layer'].keys()), ['Si'])
        assert_almost_equal(p.storage['layer']['Si'].thickness.value, 0)
        assert_almost_equal(p.storage['layer']['Si'].interface.value, 0)
        # assert_almost_equal(p.storage['layer']['Si'].material.rho.value, 0)
        # assert_almost_equal(p.storage['layer']['Si'].material.irho.value, 0)

    def test_update_layer(self):
        p = Refl1dWrapper()
        p.create_layer('Si')
        p.update_layer('Si', thickness=10, interface=5)
        assert_almost_equal(p.storage['layer']['Si'].thickness.value, 10)
        assert_almost_equal(p.storage['layer']['Si'].interface.value, 5)

    def test_get_layer_value(self):
        p = Refl1dWrapper()
        p.create_layer('Si')
        p.update_layer('Si', thickness=10, interface=5)
        assert_almost_equal(p.get_layer_value('Si', 'thickness'), 10)
        assert_almost_equal(p.get_layer_value('Si', 'interface'), 5)

    def test_create_item(self):
        p = Refl1dWrapper()
        p.create_item('SiNi')
        assert_equal(list(p.storage['item'].keys()), ['SiNi'])
        assert_almost_equal(p.storage['item']['SiNi'].repeat.value, 1)

    def test_update_item(self):
        p = Refl1dWrapper()
        p.create_item('SiNi')
        p.update_item('SiNi', repeat=10)
        assert_almost_equal(p.storage['item']['SiNi'].repeat.value, 10)

    def test_get_item_value(self):
        p = Refl1dWrapper()
        p.create_item('SiNi')
        p.update_item('SiNi', repeat=10)
        assert_almost_equal(p.get_item_value('SiNi', 'repeat'), 10)

    def test_create_model(self):
        p = Refl1dWrapper()
        p.create_model('MyModel')
        assert_equal(p.storage['model']['MyModel'], {'scale': 1, 'bkg': 0, 'dq': 0, 'items': []})

    def test_update_model(self):
        p = Refl1dWrapper()
        p.create_model('MyModel')
        p.update_model('MyModel', scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.storage['model']['MyModel']['scale'], 2)
        assert_almost_equal(p.storage['model']['MyModel']['bkg'], 1e-3)
        assert_almost_equal(p.storage['model']['MyModel']['dq'], 2.0)

    def test_get_model_value(self):
        p = Refl1dWrapper()
        p.create_model('MyModel')
        p.update_model('MyModel', scale=2, bkg=1e-3, dq=2.0)
        assert_almost_equal(p.get_model_value('MyModel', 'scale'), 2)
        assert_almost_equal(p.get_model_value('MyModel', 'bkg'), 1e-3)
        assert_almost_equal(p.get_model_value('MyModel', 'dq'), 2.0)

    def test_assign_material_to_layer(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        assert_almost_equal(p.storage['layer']['B_layer'].material.rho.value, 6.908)
        assert_almost_equal(p.storage['layer']['B_layer'].material.irho.value, -0.278)

    def test_add_layer_to_item(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        assert_equal(len(p.storage['item']['B_item'].stack), 0)
        p.add_layer_to_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item'].stack), 1)
        assert_equal(p.storage['item']['B_item'][0].name, 'B_layer')

    def test_add_item(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        p.create_model('MyModel')
        assert_equal(len(p.storage['model']['MyModel']['items']), 0)
        p.add_item('B_item', 'MyModel')
        assert_equal(len(p.storage['model']['MyModel']['items']), 1)
        assert_equal(p.storage['model']['MyModel']['items'][0].name, 'B_item')

    def test_remove_layer_from_item(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item'].stack), 1)
        p.remove_layer_from_item('B_layer', 'B_item')
        assert_equal(len(p.storage['item']['B_item'].stack), 0)

    def test_remove_item(self):
        p = Refl1dWrapper()
        p.create_material('B')
        p.update_material('B', rho=6.908, irho=-0.278)
        p.create_layer('B_layer')
        p.assign_material_to_layer('B', 'B_layer')
        p.create_item('B_item')
        p.add_layer_to_item('B_layer', 'B_item')
        p.create_model('MyModel')
        p.add_item('B_item', 'MyModel')
        assert_equal(len(p.storage['model']['MyModel']['items']), 1)
        p.remove_item('B_item', 'MyModel')
        assert_equal(len(p.storage['model']['MyModel']['items']), 0)

    def test_calculate(self):
        p = Refl1dWrapper()
        p.create_material('Material1')
        p.update_material('Material1', rho=0.000, irho=0.000)
        p.create_material('Material2')
        p.update_material('Material2', rho=2.000, irho=0.000)
        p.create_material('Material3')
        p.update_material('Material3', rho=4.000, irho=0.000)
        p.create_model('MyModel')
        p.update_model('MyModel', bkg=1e-7, dq=5.0)
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thickness=10, interface=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', interface=1.0)
        p.create_item('Item')
        p.add_layer_to_item('Layer1', 'Item')
        p.add_layer_to_item('Layer2', 'Item')
        p.add_layer_to_item('Layer3', 'Item')
        p.add_item('Item', 'MyModel')
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            1.0000001e+00, 2.1749216e-03, 1.1433942e-04, 1.9337269e-05, 4.9503970e-06,
            1.5447182e-06, 5.4663919e-07, 2.2701724e-07, 1.2687053e-07, 1.0188127e-07
        ]
        assert_almost_equal(p.calculate(q, 'MyModel'), expected)

    def test_calculate2(self):
        p = Refl1dWrapper()
        p.create_material('Material1')
        p.update_material('Material1', rho=0.000, irho=0.000)
        p.create_material('Material2')
        p.update_material('Material2', rho=2.000, irho=0.000)
        p.create_material('Material3')
        p.update_material('Material3', rho=4.000, irho=0.000)
        p.create_model('MyModel')
        p.update_model('MyModel', bkg=1e-7, dq=5.0)
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thickness=10, interface=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', interface=1.0)
        p.create_item('Item1')
        p.add_layer_to_item('Layer1', 'Item1')
        p.create_item('Item2')
        p.add_layer_to_item('Layer2', 'Item2')
        p.add_layer_to_item('Layer1', 'Item2')
        p.create_item('Item3')
        p.add_layer_to_item('Layer3', 'Item3')
        p.add_item('Item1', 'MyModel')
        p.add_item('Item2', 'MyModel')
        p.add_item('Item3', 'MyModel')
        p.update_item('Item2', repeat=10)
        q = np.linspace(0.001, 0.3, 10)
        expected = [
            1.0000001e+00, 1.8923350e-05, 1.2274125e-04, 2.4073165e-06, 6.7232911e-06,
            8.3051185e-07, 1.1546344e-06, 4.1351306e-07, 3.5132221e-07, 2.5347996e-07
        ]
        assert_almost_equal(p.calculate(q, 'MyModel'), expected)
        assert_almost_equal(p.calculate(q, 'MyModel'), expected)

    def test_sld_profile(self):
        p = Refl1dWrapper()
        p.create_material('Material1')
        p.update_material('Material1', rho=0.000, irho=0.000)
        p.create_material('Material2')
        p.update_material('Material2', rho=2.000, irho=0.000)
        p.create_material('Material3')
        p.update_material('Material3', rho=4.000, irho=0.000)
        p.create_model('MyModel')
        p.create_layer('Layer1')
        p.assign_material_to_layer('Material1', 'Layer1')
        p.create_layer('Layer2')
        p.assign_material_to_layer('Material2', 'Layer2')
        p.update_layer('Layer2', thickness=10, interface=1.0)
        p.create_layer('Layer3')
        p.assign_material_to_layer('Material3', 'Layer3')
        p.update_layer('Layer3', interface=1.0)
        p.create_item('Item')
        p.add_layer_to_item('Layer1', 'Item')
        p.add_layer_to_item('Layer2', 'Item')
        p.add_layer_to_item('Layer3', 'Item')
        p.add_item('Item', 'MyModel')
        assert_almost_equal(p.sld_profile('MyModel')[1][0], 0)
        assert_almost_equal(p.sld_profile('MyModel')[1][-1], 4)
