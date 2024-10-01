"""
Tests for LayerCollection class.
"""

from easyscience import global_object

from easyreflectometry.sample.collections.material_collection import MaterialCollection
from easyreflectometry.sample.elements.materials.material import Material


class TestMaterialCollection:
    def test_default(self):
        p = MaterialCollection()
        assert p.name == 'EasyMaterials'
        assert p.interface is None
        assert len(p) == 3
        assert p[0].name == 'Air'
        assert p[1].name == 'D2O'
        assert p[2].name == 'Si'

    def test_dont_populate(self):
        p = MaterialCollection(populate_if_none=False)
        assert p.name == 'EasyMaterials'
        assert p.interface is None
        assert len(p) == 0

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
                {'Air': {'isld': '0.000e-6 1/Å^2', 'sld': '0.000e-6 1/Å^2'}},
                {'D2O': {'isld': '0.000e-6 1/Å^2', 'sld': '6.335e-6 1/Å^2'}},
                {'Si': {'isld': '0.000e-6 1/Å^2', 'sld': '2.074e-6 1/Å^2'}},
            ]
        }

    def test_repr(self):
        p = MaterialCollection()
        p.__repr__()
        assert (
            p.__repr__()
            == 'EasyMaterials:\n- Air:\n    sld: 0.000e-6 1/Å^2\n    isld: 0.000e-6 1/Å^2\n- D2O:\n    sld: 6.335e-6 1/Å^2\n    isld: 0.000e-6 1/Å^2\n- Si:\n    sld: 2.074e-6 1/Å^2\n    isld: 0.000e-6 1/Å^2\n'  # noqa: E501
        )

    def test_dict_round_trip(self):
        # When
        m = Material(6.908, -0.278, 'Boron')
        k = Material(0.487, 0.000, 'Potassium')
        p = MaterialCollection()
        p.insert(0, m)
        p.add_material(k)
        p_dict = p.as_dict()
        global_object.map._clear()

        # Then
        q = MaterialCollection.from_dict(p_dict)

        # Expect
        assert sorted(p.as_data_dict()) == sorted(q.as_data_dict())

    def test_add_material(self):
        # Given
        p = MaterialCollection()
        m = Material(6.908, -0.278, 'Boron')

        # When
        p.add_material(m)

        # Then
        assert p[3] == m

    def test_duplicate_material(self):
        # Given
        p = MaterialCollection()
        m = Material(6.908, -0.278, 'Boron')
        p.add_material(m)

        # When
        p.duplicate_material(3)

        # Then
        assert p[4].name == 'Boron duplicate'

    def test_move_material_up(self):
        # Given
        p = MaterialCollection()
        k = Material(0.487, 0.000, 'Bottom')
        p.add_material(k)

        # When
        p.move_material_up(3)

        # Then
        assert p[2].name == 'Bottom'
        assert p[3].name == 'Si'

    def test_move_material_up_to_top_and_further(self):
        # Given
        p = MaterialCollection()
        m = Material(0.487, 0.000, 'Bottom')
        p.add_material(m)

        # When
        p.move_material_up(3)
        p.move_material_up(2)
        p.move_material_up(1)
        p.move_material_up(0)

        # Then
        assert p[0].name == 'Bottom'
        assert p[3].name == 'Si'

    def test_move_material_down(self):
        # Given
        p = MaterialCollection()
        m = Material(0.487, 0.000, 'Bottom')
        p.add_material(m)

        # When
        p.move_material_down(2)

        # Then
        assert p[2].name == 'Bottom'
        assert p[3].name == 'Si'

    def test_move_material_down_to_bottom_and_further(self):
        # Given
        p = MaterialCollection()
        k = Material(0.487, 0.000, 'Middle')
        m = Material(0.487, 0.000, 'Bottom')
        p.add_material(k)
        p.add_material(m)

        # When
        p.move_material_down(3)
        p.move_material_down(4)

        # Then
        assert p[0].name == 'Air'
        assert p[3].name == 'Bottom'
        assert p[4].name == 'Middle'

    def test_remove_material(self):
        # Given
        p = MaterialCollection()
        m = Material(0.487, 0.000, 'Bottom')
        p.add_material(m)

        # When
        p.remove_material(1)

        # Then
        assert len(p) == 3
        assert p[0].name == 'Air'
        assert p[2].name == 'Bottom'
