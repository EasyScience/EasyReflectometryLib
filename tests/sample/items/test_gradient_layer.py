import unittest

import pytest
from numpy.testing import assert_almost_equal

from EasyReflectometry.sample.item import GradientLayer
from EasyReflectometry.sample.items.gradient_layer import _linear_gradient
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.material import Material
from easyCore.Objects.ObjectClasses import Parameter


class TestGradientLayer(unittest.TestCase):
    def test_init(self):
        # When
        init = Material.from_pars(10.0, -10.0, 'Material_1')
        final = Material.from_pars(0.0, 0.0, 'Material_2')

        # Then
        result = GradientLayer(
            initial_material=init,
            final_material=final,
            thickness=1.0,
            roughness=2.0,
            discretisation_elements=10,
            name='Test',
            interface=None
        )
    
        # Expect
        assert len(result.layers) == 10 
        assert result.name, 'Test'
        assert result.type, 'Gradient-layer'
        assert result.interface is None
        assert result.thickness == 1.0
        assert result.layers.name == '0/1/2/3/4/5/6/7/8/9'
        assert result.layers[0].material.sld.raw_value == 10.0
        assert result.layers[5].material.sld.raw_value == 5.0
        assert result.layers[0].thickness.raw_value == 0.1
        assert result.layers[5].material.isld.raw_value == -5.0
        assert result.layers[9].material.isld.raw_value == -1.0

    def test_default(self):
        # When Then
        result = GradientLayer.default()
        
        # Expect
        assert result.name == 'Air-Deuterium'
        assert result.type, 'Gradient-layer'
        assert result.interface is None
        assert len(result.layers) == 10
        assert  result.layers.name == '0/1/2/3/4/5/6/7/8/9'

    def test_from_pars(self):
        # When
        init = Material.from_pars(6.908, -0.278, 'Boron')
        final = Material.from_pars(0.487, 0.000, 'Potassium')
        
        # Then
        result = GradientLayer.from_pars(
            initial_material=init,
            final_material=final,
            thickness=10.0,
            roughness=1.0,
            discretisation_elements=5,
            name='gradientItem'
        )

        # Expect
        assert result.name, 'gradientItem'
        assert result.type, 'Gradient-layer'
        assert result.interface is None
        assert len(result.layers) == 5
        assert result.layers.name == '0/1/2/3/4'

    def test_add_layer(self):
        # When
        gradient_layer = GradientLayer.default()

        # Then Expect
        with pytest.raises(NotImplementedError, match=r".* add .*"):
            gradient_layer.add_layer(Layer.default())

    def test_duplicate_layer(self):
        # When
        gradient_layer = GradientLayer.default()

        # Then Expect
        with pytest.raises(NotImplementedError, match=r".* duplicate .*"):
            gradient_layer.duplicate_layer(1)

    def test_remove_layer(self):
        # When
        gradient_layer = GradientLayer.default()

        # Then Expect
        with pytest.raises(NotImplementedError, match=r".* remove .*"):
            gradient_layer.remove_layer(1)

    def test_repr(self):
        # When Then
        result = GradientLayer.default()

        # Expect
        expected_str = "type: Gradient-layer\nthickness: 2.0\ndiscretisation_elements: 10\ninitial_layer:\n  '0':\n    material:\n      EasyMaterial:\n        sld: 0.000e-6 1 / angstrom ** 2\n        isld: 0.000e-6 1 / angstrom ** 2\n    thickness: 0.200 angstrom\n    roughness: 0.000 angstrom\nfinal_layer:\n  '9':\n    material:\n      EasyMaterial:\n        sld: 5.724e-6 1 / angstrom ** 2\n        isld: 0.000e-6 1 / angstrom ** 2\n    thickness: 0.200 angstrom\n    roughness: 0.000 angstrom\n"
        assert result.__repr__() == expected_str

    def test_dict_round_trip(self):
        # When
        default = GradientLayer.default()

        # Then
        result = GradientLayer.from_dict(default.as_dict())
        
        # Expect
        assert result.as_data_dict() == default.as_data_dict()
        assert len(default.layers) == len(result.layers)
        # Just one layer of the generated layers is checked
        assert default.layers[5].__repr__() == result.layers[5].__repr__()


def test_linear_gradient_increasing():
    # When Then
    result = _linear_gradient(init_value=1.5, final_value=2.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([1.5, 1.6, 1.7, 1.8, 1.9, 2. , 2.1, 2.2, 2.3, 2.4, 2.5], result)


def test_linear_gradient_decreasing():
    # When Then
    result = _linear_gradient(init_value=2.5, final_value=1.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([2.5, 2.4, 2.3, 2.2, 2.1, 2. , 1.9, 1.8, 1.7, 1.6, 1.5], result)


def test_linear_gradient_same():
    # When Then
    result = _linear_gradient(init_value=2.5, final_value=2.5, discretisation_elements=10)

    # Expect
    assert_almost_equal([2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5], result)
