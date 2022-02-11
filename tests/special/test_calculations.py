__author__ = 'github.com/arm61'

import unittest

from numpy.testing import assert_almost_equal

from EasyReflectometry.special.calculations import weighted_average_sld


class TestMaterialMixture(unittest.TestCase):

    def test_weighted_average_sld(self):
        a = weighted_average_sld(1, 2, 0.5)
        assert_almost_equal(a, 1.5)
