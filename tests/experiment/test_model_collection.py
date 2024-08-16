import pytest
from easyreflectometry.experiment.model import Model
from easyreflectometry.experiment.model_collection import ModelCollection
from easyscience import global_object


class TestModelCollection:
    def test_default(self):
        # When Then
        collection = ModelCollection()

        # Expect
        assert collection.name == 'EasyModels'
        assert collection.interface is None
        assert len(collection) == 2
        assert collection[0].name == 'EasyModel'
        assert collection[1].name == 'EasyModel'

    def test_from_pars(self):
        # When
        model_1 = Model(name='Model1')
        model_2 = Model(name='Model2')
        model_3 = Model(name='Model3')

        # Then
        collection = ModelCollection(model_1, model_2, model_3)

        # Expect
        assert collection.name == 'EasyModels'
        assert collection.interface is None
        assert len(collection) == 3
        assert collection[0].name == 'Model1'
        assert collection[1].name == 'Model2'
        assert collection[2].name == 'Model3'

    def test_add_model(self):
        # When
        model_1 = Model(name='Model1')
        model_2 = Model(name='Model2')

        # Then
        collection = ModelCollection(model_1)
        collection.add_model(model_2)

        # Expect
        assert len(collection) == 2
        assert collection[0].name == 'Model1'
        assert collection[1].name == 'Model2'

    def test_delete_model(self):
        # When
        model_1 = Model(name='Model1')
        model_2 = Model(name='Model2')

        # Then
        collection = ModelCollection(model_1, model_2)
        collection.remove_model(0)

        # Expect
        assert len(collection) == 1
        assert collection[0].name == 'Model2'

    def test_as_dict(self):
        # When
        model_1 = Model(name='Model1')
        collection = ModelCollection(model_1)

        # Then
        dict_repr = collection.as_dict()

        # Expect
        assert dict_repr['data'][0]['resolution_function'] == {'smearing': 'PercentageFhwm', 'constant': 5.0}

    def test_dict_round_trip(self):
        # When
        global_object.map._clear()
        model_1 = Model(name='Model1')
        model_2 = Model(name='Model2')
        model_3 = Model(name='Model3')
        collection = ModelCollection(model_1, model_2, model_3)
        collection_dict = collection.as_dict()
        global_object.map._clear()

        # Then
        collection_from_dict = ModelCollection.from_dict(collection_dict)

        # Expect
        # We have to skip the resolution_function, interface and unique_name as some are generated on the fly
        assert collection.as_data_dict(
            skip=['resolution_function', 'interface', 'unique_name']
        ) == collection_from_dict.as_data_dict(skip=['resolution_function', 'interface', 'unique_name'])
        assert collection[0]._resolution_function.smearing(5.5) == collection_from_dict[0]._resolution_function.smearing(5.5)
