"""
Tests for LayerCollection class.
"""

__author__ = 'github.com/arm61'
__version__ = '0.0.1'

import unittest

from easyreflectometry.sample.elements.materials.material import Material
from easyreflectometry.sample.elements.materials.material_collection import MaterialCollection
from easyscience import global_object


class TestMaterialCollection(unittest.TestCase):
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

    def test_empty_list(self):
        p = MaterialCollection([])
        assert p.name == 'EasyMaterials'
        assert p.interface is None
        assert len(p) == 0

    def test_dict_repr(self):
        p = MaterialCollection()
        assert p._dict_repr == {
            'EasyMaterials': [
                {'EasyMaterial': {'isld': '0.000e-6 1/Å^2', 'sld': '4.186e-6 1/Å^2'}},
                {'EasyMaterial': {'isld': '0.000e-6 1/Å^2', 'sld': '4.186e-6 1/Å^2'}},
            ]
        }

    def test_repr(self):
        p = MaterialCollection()
        p.__repr__()
        assert (
            p.__repr__()
            == 'EasyMaterials:\n- EasyMaterial:\n    sld: 4.186e-6 1/Å^2\n    isld: 0.000e-6 1/Å^2\n- EasyMaterial:\n    sld: 4.186e-6 1/Å^2\n    isld: 0.000e-6 1/Å^2\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = MaterialCollection()
        p.insert(0, m)
        p.append(k)
        p_dict = p.as_dict()
        global_object.map._clear()

        # Then
        q = MaterialCollection.from_dict(p_dict)

        # Expect
        assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())
