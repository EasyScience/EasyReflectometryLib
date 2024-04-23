"""
Tests for LayerCollection class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

from EasyReflectometry.sample.elements.materials.material import Material
from EasyReflectometry.sample.elements.materials.material_collection import MaterialCollection


class TestLayerCollection(unittest.TestCase):
    def test_default(self):
        p = MaterialCollection()
        assert p.name == 'EasyMaterials'
        assert p.interface is None
        assert len(p) == 2
        assert p[0].name == 'EasyMaterial'
        assert p[1].name == 'EasyMaterial'

    def test_from_pars(self):
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = MaterialCollection(m, k, name='thinBoron')
        assert p.name == 'thinBoron'
        assert p.interface is None
        assert len(p) == 2
        assert p[0].name == 'Boron'
        assert p[1].name == 'Potassium'

    def test_dict_repr(self):
        p = MaterialCollection()
        assert p._dict_repr == {
            'EasyMaterials': [
                {'EasyMaterial': {'isld': '0.000e-6 1 / angstrom ** 2', 'sld': '4.186e-6 1 / angstrom ** 2'}},
                {'EasyMaterial': {'isld': '0.000e-6 1 / angstrom ** 2', 'sld': '4.186e-6 1 / angstrom ** 2'}},
            ]
        }

    def test_repr(self):
        p = MaterialCollection()
        assert (
            p.__repr__()
            == 'EasyMaterials:\n- EasyMaterial:\n    sld: 4.186e-6 1 / angstrom ** 2\n    isld: 0.000e-6 1 / angstrom ** 2\n- EasyMaterial:\n    sld: 4.186e-6 1 / angstrom ** 2\n    isld: 0.000e-6 1 / angstrom ** 2\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = MaterialCollection()
        p.insert(0, m)
        p.append(k)

        # Then
        q = MaterialCollection.from_dict(p.as_dict())

        # Expect
        assert p.as_data_dict() == q.as_data_dict()
