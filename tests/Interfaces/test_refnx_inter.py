__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Refnx class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Interfaces.refnx import Refnx
from easyReflectometryLib.Sample.material import Material


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
