from unittest.mock import MagicMock

from easyreflectometry.sample.collections.base_collection import BaseCollection
from easyreflectometry.sample.elements.layers.layer import Layer


class TestBaseCollection:
    def test_constructor(self):
        # When
        elem_1 = Layer(name='layer_1')
        elem_2 = Layer(name='layer_2')
        mock_interface = MagicMock()

        # Then
        p = BaseCollection('name', mock_interface, elem_1, elem_2)

        # Expect
        p._interface = mock_interface
        len(p) == 2

    def test_names(self):
        # When
        elem_1 = Layer(name='layer_1')
        elem_2 = Layer(name='layer_2')
        mock_interface = MagicMock()

        # Then
        p = BaseCollection('name', mock_interface, elem_1, elem_2)

        # Expect
        assert p.names == ['layer_1', 'layer_2']

    def test_dict_repr(self):
        # When
        elem = Layer(name='layer')
        mock_interface = MagicMock()

        # Then
        p = BaseCollection('name', mock_interface, elem)

        # Expect
        assert p._dict_repr == {
            'name': [
                {
                    'layer': {
                        'material': {'EasyMaterial': {'isld': '0.000e-6 1/Å^2', 'sld': '4.186e-6 1/Å^2'}},
                        'roughness': '3.300 Å',
                        'thickness': '10.000 Å',
                    }
                }
            ]
        }

    def test_as_dict(self):
        # When
        elem = Layer(name='layer')
        mock_interface = MagicMock()

        # Then
        p = BaseCollection('name', mock_interface, elem)

        # Expect
        assert p.as_dict()['name'] == 'name'
        assert len(p.as_dict()['data']) == 1
        assert p.as_dict()['data'][0]['name'] == 'layer'
