import datetime
import json
import os
from pathlib import Path

from easyscience.fitting import AvailableMinimizers

from easyreflectometry.model import ModelCollection
from easyreflectometry.sample import MaterialCollection


class Project:
    def __init__(self):
        self._info = self._defalt_info()
        self._current_path = Path(os.path.expanduser('~'))
        self._models: ModelCollection = None
        self._materials: MaterialCollection = None
        self._calculator = None
        self._minimizer: AvailableMinimizers = None
        self._experiments = None
        self._report = None

        # Project flags
        self._project_created = False
        self._project_with_experiments = False

    def _defalt_info(self):
        return dict(
            name='Example Project',
            short_description='reflectometry, 1D',
            samples='None',
            experiments='None',
            modified=datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        )

    def create_project_dir(self):
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
            os.makedirs(self.project_path / 'experiments')
            with open(self.project_json, 'w') as file:
                project_dict = self._prepare_project_dict()
                file.write(json.dumps(project_dict, indent=4))
        else:
            print(f'ERROR: Directory {self.project_path} already exists')

    @property
    def project_path(self):
        return self._current_path / self._info['name']

    @property
    def project_json(self):
        return self.project_path / 'project.json'

    def _construct_project_dict(self, include_materials_not_in_model=False):
        project_dict = {}
        project_dict['models'] = self._models.as_dict(skip=['interface'])

        project_dict['no_experiments'] = self._no_experiments
        project_dict['project_info'] = self._info

        project_dict['calculator'] = [self._calculator.current_interface_name]

        project_dict['minimizer'] = self._minimizer.name

        if include_materials_not_in_model:
            self._add_materials_not_in_model_dict(project_dict)

        if self._project_with_experiments:
            self._add_experiments_to_dict(project_dict)

        project_dict['colors'] = self.parent._model_proxy._colors

    def _add_materials_not_in_model_dict(self, project_json: dict):
        materials_in_model = []
        for model in self._models:
            for assembly in model.sample:
                for layer in assembly.layers:
                    materials_in_model.append(layer.material)
        materials_not_in_model = []
        for material in self._materials:
            if material not in materials_in_model:
                materials_not_in_model.append(material)
        project_json['materials_not_in_model'] = MaterialCollection(materials_not_in_model).as_dict(skip=['interface'])

    def _add_experiments_to_dict(self, project_json: dict):
        project_json['experiments'] = []
        project_json['experiments_models'] = []
        project_json['experiments_names'] = []
        for experiment in self._experiments:
            if self._experiments[0].xe is not None:
                project_json['experiments'].append([experiment.x, experiment.y, experiment.ye, experiment.xe])
            else:
                project_json['experiments'].append([experiment.x, experiment.y, experiment.ye])
            project_json['experiments_models'].append(experiment.model.name)
            project_json['experiments_names'].append(experiment.name)

    def _extract_project_dict(self, project_dict):
        self._models = ModelCollection.from_dict(project_dict['models'])
        self._info = project_dict['project_info']
        self._calculator = project_dict['calculator']
        self._minimizer = AvailableMinimizers[project_dict['minimizer']]
        self._project_with_experiments = project_dict['no_experiments']
        if self._project_with_experiments:
            self._experiments = self._extract_experiments_from_dict(project_dict)
        self._materials = MaterialCollection.from_dict(project_dict['materials'])

    def _extracy_experiments_from_dict(self, project_json: dict):
        project_json['experiments'] = []
        project_json['experiments_models'] = []
        project_json['experiments_names'] = []
        for experiment in self._experiments:
            if self._experiments[0].xe is not None:
                project_json['experiments'].append([experiment.x, experiment.y, experiment.ye, experiment.xe])
            else:
                project_json['experiments'].append([experiment.x, experiment.y, experiment.ye])
            project_json['experiments_models'].append(experiment.model.name)
            project_json['experiments_names'].append(experiment.name)
