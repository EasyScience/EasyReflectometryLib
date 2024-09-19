"""
Tests for Sample class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

from unittest.mock import MagicMock

import pytest
from easyscience import global_object
from numpy.testing import assert_equal

from easyreflectometry.sample import Layer
from easyreflectometry.sample import LayerCollection
from easyreflectometry.sample import Material
from easyreflectometry.sample import Multilayer
from easyreflectometry.sample import RepeatingMultilayer
from easyreflectometry.sample import Sample
from easyreflectometry.sample import SurfactantLayer


class TestSample:
    def test_default(self):
        # When Then
        p = Sample()

        # Expect
        assert_equal(p.name, 'EasySample')
        assert_equal(p.interface, None)
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')

    def test_add_assembly(self):
        # When
        p = Sample()
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()
        surfactant = SurfactantLayer()

        # Then
        p.add_assembly(surfactant)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, 'EasySurfactantLayer')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    # Problems with parameterized tests START
    def test_duplicate_assembly_multilayer(self):
        # When
        assembly_to_duplicate = Multilayer()
        p = Sample()
        p.add_assembly(assembly_to_duplicate)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.duplicate_assembly(2)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, assembly_to_duplicate.name)
        assert_equal(p[3].name, assembly_to_duplicate.name + ' duplicate')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    def test_duplicate_assembly_repeating_multilayer(self):
        # When
        assembly_to_duplicate = RepeatingMultilayer()
        p = Sample()
        p.add_assembly(assembly_to_duplicate)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.duplicate_assembly(2)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, assembly_to_duplicate.name)
        assert_equal(p[3].name, assembly_to_duplicate.name + ' duplicate')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    def test_duplicate_assembly_surfactant(self):
        # When
        assembly_to_duplicate = SurfactantLayer()
        p = Sample()
        p.add_assembly(assembly_to_duplicate)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.duplicate_assembly(2)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, assembly_to_duplicate.name)
        assert_equal(p[3].name, assembly_to_duplicate.name + ' duplicate')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    # Problems with parameterized tests END

    def test_move_assembly_up(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.add_assembly(surfactant)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.move_assembly_up(2)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, surfactant.name)
        assert_equal(p[2].name, 'EasyMultilayer')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    def test_move_assembly_up_index_0(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.add_assembly(surfactant)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.move_assembly_up(0)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, surfactant.name)
        p._enable_changes_to_outermost_layers.assert_not_called()
        p._disable_changes_to_outermost_layers.assert_not_called()

    def test_move_assembly_down(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.add_assembly(surfactant)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.move_assembly_down(1)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, surfactant.name)
        assert_equal(p[2].name, 'EasyMultilayer')
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    def test_move_assembly_down_index_2(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.add_assembly(surfactant)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.move_assembly_down(2)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, 'EasyMultilayer')
        assert_equal(p[2].name, surfactant.name)
        p._enable_changes_to_outermost_layers.assert_not_called()
        p._disable_changes_to_outermost_layers.assert_not_called()

    def test_remove_assembly(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.add_assembly(surfactant)
        p._enable_changes_to_outermost_layers = MagicMock()
        p._disable_changes_to_outermost_layers = MagicMock()

        # Then
        p.remove_assembly(1)

        # Expect
        assert_equal(p[0].name, 'EasyMultilayer')
        assert_equal(p[1].name, surfactant.name)
        p._enable_changes_to_outermost_layers.assert_called_once_with()
        p._disable_changes_to_outermost_layers.assert_called_once_with()

    def test_subphase(self):
        # When
        p = Sample()
        layer = Multilayer(Layer(name='new layer'))
        p.add_assembly(layer)

        # Then
        layer = p.subphase

        # Expect
        assert_equal(layer.name, 'new layer')

    def test_superphase(self):
        # When
        p = Sample()
        layer = Multilayer(Layer(name='new layer'))
        p.add_assembly(layer)
        p.move_assembly_up(2)
        p.move_assembly_up(1)

        # Then
        layer = p.superphase

        # Expect
        assert_equal(layer.name, 'new layer')

    def test_enable_changes_to_outermost_layers(self):
        # When
        p = Sample()
        p.superphase.thickness.enabled = False
        p.superphase.roughness.enabled = False
        p.subphase.thickness.enabled = False

        # Then
        p._enable_changes_to_outermost_layers()

        # Expect
        assert_equal(p.superphase.thickness.enabled, True)
        assert_equal(p.superphase.roughness.enabled, True)
        assert_equal(p.subphase.thickness.enabled, True)

    def test_disable_changes_to_outermost_layers(self):
        # When
        p = Sample()
        p.superphase.thickness.enabled = True
        p.superphase.roughness.enabled = True
        p.subphase.thickness.enabled = True

        # Then
        p._disable_changes_to_outermost_layers()

        # Expect
        assert_equal(p.superphase.thickness.enabled, False)
        assert_equal(p.superphase.roughness.enabled, False)
        assert_equal(p.subphase.thickness.enabled, False)

    def test_from_pars(self):
        # When
        m1 = Material(6.908, -0.278, 'Boron')
        m2 = Material(0.487, 0.000, 'Potassium')
        l1 = Layer(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = LayerCollection(l1, l2, name='twoLayer1')
        ls2 = LayerCollection(l2, l1, name='twoLayer2')
        o1 = RepeatingMultilayer(ls1, 2.0, 'twoLayerItem1')
        o2 = RepeatingMultilayer(ls2, 1.0, 'oneLayerItem2')

        # Then
        d = Sample(o1, o2, name='myModel')

        # Expect
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'twoLayerItem1')
        assert_equal(d[1].name, 'oneLayerItem2')

    def test_from_pars_layers(self):
        # When
        m1 = Material(6.908, -0.278, 'Boron')
        m2 = Material(0.487, 0.000, 'Potassium')
        l1 = Layer(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer(m2, 50.0, 1.0, 'thickPotassium')

        # Then
        d = Sample(l1, l2, name='myModel')

        # Expect
        assert_equal(d.name, 'myModel')
        assert_equal(d.interface, None)
        assert_equal(d[0].name, 'thinBoron')
        assert_equal(d[1].name, 'thickPotassium')

    def test_from_pars_error(self):
        m1 = Material(6.908, -0.278, 'Boron')

        with pytest.raises(ValueError):
            _ = Sample(m1, name='myModel')

    def test_repr(self):
        p = Sample()
        assert (
            p.__repr__()
            == 'EasySample:\n- EasyMultilayer:\n    EasyLayerCollection:\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1/Å^2\n            isld: 0.000e-6 1/Å^2\n        thickness: 10.000 Å\n        roughness: 3.300 Å\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1/Å^2\n            isld: 0.000e-6 1/Å^2\n        thickness: 10.000 Å\n        roughness: 3.300 Å\n- EasyMultilayer:\n    EasyLayerCollection:\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1/Å^2\n            isld: 0.000e-6 1/Å^2\n        thickness: 10.000 Å\n        roughness: 3.300 Å\n    - EasyLayer:\n        material:\n          EasyMaterial:\n            sld: 4.186e-6 1/Å^2\n            isld: 0.000e-6 1/Å^2\n        thickness: 10.000 Å\n        roughness: 3.300 Å\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        p = Sample()
        surfactant = SurfactantLayer()
        p.append(surfactant)
        multilayer = Multilayer()
        p.append(multilayer)
        repeating = RepeatingMultilayer()
        p.append(repeating)
        p_dict = p.as_dict()
        global_object.map._clear()

        # Then
        q = Sample.from_dict(p_dict)

        # Expect
        assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())
