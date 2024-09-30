import datetime
import os
from pathlib import Path

from easyscience import global_object
from easyscience.fitting import AvailableMinimizers

from easyreflectometry.model import Model
from easyreflectometry.model import ModelCollection
from easyreflectometry.project import Project
from easyreflectometry.sample import Material
from easyreflectometry.sample import MaterialCollection


class TestProject:
    def test_constructor(self):
        # When Then
        project = Project()

        # Expect
        assert project._info == {
            'name': 'Example Project',
            'short_description': 'reflectometry, 1D',
            'samples': 'None',
            'experiments': 'None',
            'modified': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        }
        assert project._project_path == Path(os.path.expanduser('~'))
        assert len(project._materials) == 0
        assert len(project._models) == 0
        assert project._calculator is None
        assert project._minimizer is None
        assert project._experiments is None
        assert project._report is None
        assert project._project_created is False
        assert project._project_with_experiments is False

    def test_reset(self):
        # When
        project = Project()
        project._info['name'] = 'Test Project'
        project._materials.append(Material())
        project._models.append(Model())
        project._calculator = 'calculator'
        project._minimizer = 'minimizer'
        project._experiments = 'experiments'
        project._report = 'report'
        project._project_created = True
        project._project_with_experiments = True
        project._project_path = 'project_path'

        # Then
        project.reset()

        # Expect
        assert project._info == {
            'name': 'Example Project',
            'short_description': 'reflectometry, 1D',
            'samples': 'None',
            'experiments': 'None',
            'modified': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        }
        assert project._models.unique_name == 'project_models'
        assert len(project._models) == 0
        assert project._materials.unique_name == 'project_materials'
        assert len(project._materials) == 0

        assert project._project_path == Path(os.path.expanduser('~'))
        assert project._calculator is None
        assert project._minimizer is None
        assert project._experiments is None
        assert project._report is None
        assert project._project_created is False
        assert project._project_with_experiments is False
        assert global_object.map.vertices() == ['project_models', 'project_materials']

    def test_models(self):
        # When
        project = Project()
        models = ModelCollection(Model())
        material = Material()
        project._materials.append(material)

        # Then
        project.models = models

        # Expect
        project_models_dict = project.models.as_dict(skip=['interface'])
        models_dict = models.as_dict(skip=['interface'])
        models_dict['unique_name'] = 'project_models'
        assert project_models_dict == models_dict

        assert len(project._materials) == 3
        assert project._materials[0] == material
        assert project._materials[1] == models[0].sample[0].layers[0].material
        assert project._materials[2] == models[0].sample[1].layers[0].material

    def test_default_model(self):
        # When
        global_object.map._clear()
        project = Project()

        # Then
        project.default_model()

        # Expect
        assert len(project._models) == 1
        assert project._models[0].unique_name == 'Model_0'
        assert len(project._models.data[0].sample) == 3
        assert len(project._materials) == 3

    def test_minimizer(self):
        # When
        project = Project()

        # Then
        project.minimizer = 'minimizer'

        # Expect
        assert project.minimizer == 'minimizer'

    def test_experiments(self):
        # When
        project = Project()

        # Then
        project.experiments = 'experiments'

        # Expect
        assert project.experiments == 'experiments'

    # def test_path_project(self):
    #     # When
    #     project = Project()
    #     project._info['name'] = 'Test Project'

    #     # Then Expect
    #     assert project.path_project == Path(os.path.expanduser('~')) / 'Test Project'

    def test_path_json(self, tmp_path):
        # When
        project = Project()
        project.project_path = tmp_path
        #        project._info['name'] = 'Test Project'

        # Then Expect
        assert project.path_json == Path(tmp_path) / 'project.json'

    def test_add_material(self):
        # When
        project = Project()
        material = Material()

        # Then
        project.add_material(material)

        # Expect
        assert len(project._materials) == 1
        assert project._materials[0] == material

    def test_remove_material(self):
        # When
        project = Project()
        material = Material()
        project.add_material(material)

        # Then
        project.remove_material(0)

        # Expect
        assert len(project._materials) == 0

    def test_remove_material_in_model(self):
        # When
        project = Project()
        model = Model()
        models = ModelCollection(model)
        project.models = models

        # Then
        project.remove_material(0)

        # Expect
        assert len(project._materials) == 2

    def test_default_info(self):
        # When
        project = Project()

        # Then
        info = project._defalt_info()

        # Expect
        assert info == {
            'name': 'Example Project',
            'short_description': 'reflectometry, 1D',
            'samples': 'None',
            'experiments': 'None',
            'modified': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        }

    def test_as_dict(self):
        # When
        project = Project()

        # Then
        project_dict = project.as_dict()

        # Expect
        keys = list(project_dict.keys())
        keys.sort()
        assert keys == [
            'info',
            'models',
            'project_created',
            'project_with_experiments',
        ]
        assert project_dict['info'] == {
            'name': 'Example Project',
            'short_description': 'reflectometry, 1D',
            'samples': 'None',
            'experiments': 'None',
            'modified': datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        }
        assert project_dict['models']['data'] == []
        assert project_dict['project_created'] is False
        assert project_dict['project_with_experiments'] is False

    def test_as_dict_models(self):
        # When
        project = Project()
        models = ModelCollection(Model())
        project.models = models

        # Then
        project_dict = project.as_dict()

        # Expect
        models_dict = models.as_dict(skip=['interface'])
        models_dict['unique_name'] = 'project_models'
        assert project_dict['models'] == models_dict

    def test_as_dict_materials_not_in_model(self):
        # When
        project = Project()
        models = ModelCollection(Model())
        project.models = models
        material = Material()
        project.add_material(material)

        # Then
        project_dict = project.as_dict(include_materials_not_in_model=True)

        # Expect
        assert project_dict['materials_not_in_model']['data'][0] == material.as_dict(skip=['interface'])

    def test_as_dict_minimizer(self):
        # When
        project = Project()
        minimizer = AvailableMinimizers.LMFit
        project.minimizer = minimizer

        # Then
        project_dict = project.as_dict()

        # Expect
        assert project_dict['minimizer'] == 'LMFit'

    def test_replace_collection(self):
        # When
        project = Project()
        material = Material()
        project._materials.append(material)
        new_material = Material()

        # Then
        project._replace_collection(MaterialCollection(new_material), project._materials)

        # Expect
        assert project._materials[0] == new_material
        assert project._materials.unique_name == 'project_materials'

    def test_get_materials_in_models(self):
        # When
        models = ModelCollection(Model())
        project = Project()
        project.models = models
        material = Material(6.908, -0.278, 'Boron')
        project.add_material(material)

        # Then
        materials = project._get_materials_in_models()

        # Expect
        assert len(materials) == 2
        assert materials[0] == models[0].sample[0].layers[0].material
        assert materials[1] == models[0].sample[1].layers[0].material

    def test_dict_round_trip(self):
        # When
        global_object.map._clear()
        project = Project()
        models = ModelCollection(Model())
        project.models = models
        material = Material(6.908, -0.278, 'Boron')
        project.add_material(material)
        minimizer = AvailableMinimizers.LMFit
        project.minimizer = minimizer
        project_dict = project.as_dict(include_materials_not_in_model=True)
        project_materials_dict = project._materials.as_dict()

        del material
        global_object.map._clear()

        # Then
        new_project = Project()
        new_project.from_dict(project_dict)
        new_project_dict = new_project.as_dict(include_materials_not_in_model=True)
        new_project_materials_dict = new_project._materials.as_dict()

        # Expect
        keys = list(project_dict.keys())
        for key in keys:
            assert project_dict[key] == new_project_dict[key]
        assert project_materials_dict == new_project_materials_dict

    def test_save_project(self, tmp_path):
        # When
        global_object.map._clear()
        project = Project()
        project.current_path = tmp_path
        project._models.append(Model())
        project._info['name'] = 'Test Project'
        project.save_project_json(overwrite=True)

        # Then
        project_path = project.path_json

        # Expect
        assert project_path.exists()

    def test_load_project(self, tmp_path):
        # When
        global_object.map._clear()
        project = Project()
        project.current_path = tmp_path
        project._models.append(Model())
        project._info['name'] = 'Test Project'
        project.save_project_json()
        project_dict = project.as_dict()

        global_object.map._clear()
        new_project = Project()
        new_project.current_path = tmp_path

        # Then
        new_project.load_project_json(new_project._project_path / 'project.json')
        # Do it twice to ensure that potential global objects don't collide
        new_project.load_project_json(new_project._project_path / 'project.json')

        # Expect
        assert len(new_project._models) == 1
        assert new_project._info['name'] == 'Test Project'
        assert new_project.as_dict() == project_dict
