import datetime
import json
import os
from pathlib import Path
from typing import List

from easyscience.fitting import AvailableMinimizers

from easyreflectometry.data.data_store import DataSet1D
from easyreflectometry.model import ModelCollection
from easyreflectometry.sample import MaterialCollection
from easyreflectometry.sample.collections.base_collection import BaseCollection


class Project:
    def __init__(self):
        self._info = self._defalt_info()
        self._current_path = Path(os.path.expanduser('~'))
        self._models = ModelCollection(populate_if_none=False, unique_name='project_models')
        self._materials = MaterialCollection(populate_if_none=False, unique_name='project_materials')
        self._calculator = None
        self._minimizer: AvailableMinimizers = None
        self._experiments: List[DataSet1D] = None
        self._colors = None
        self._report = None

        # Project flags
        self._project_created = False
        self._project_with_experiments = False

    def reset(self):
        for i in range(len(self._models)):
            self._models.pop(0)
        for i in range(len(self._materials)):
            self._materials.pop(0)

        self._info = self._defalt_info()
        self._calculator = None
        self._minimizer = None
        self._experiments = None
        self._colors = None
        self._report = None

        # Project flags
        self._project_created = False
        self._project_with_experiments = False

    @property
    def models(self) -> ModelCollection:
        return self._models

    @models.setter
    def models(self, models: ModelCollection) -> None:
        self._replace_collection(models, self._models)
        self._materials.extend(self._get_materials_in_models())

    @property
    def minimizer(self) -> AvailableMinimizers:
        return self._minimizer

    @minimizer.setter
    def minimizer(self, minimizer: AvailableMinimizers) -> None:
        self._minimizer = minimizer

    @property
    def experiments(self) -> List[DataSet1D]:
        return self._experiments

    @experiments.setter
    def experiments(self, experiments: List[DataSet1D]) -> None:
        self._experiments = experiments

    @property
    def project_path(self):
        return self._current_path / self._info['name']

    @property
    def project_json(self):
        return self.project_path / 'project.json'

    def add_material(self, material: MaterialCollection) -> None:
        if material in self._materials:
            print(f'WARNING: Material {material} is already in material collection')
        else:
            self._materials.append(material)

    def remove_material(self, index: int) -> None:
        if self._materials[index] in self._get_materials_in_models():
            print(f'ERROR: Material {self._materials[index]} is used in models')
        else:
            self._materials.pop(index)

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
                project_dict = self._construct_project_dict()
                file.write(json.dumps(project_dict, indent=4))
        else:
            print(f'ERROR: Directory {self.project_path} already exists')

    def _construct_project_dict(self, include_materials_not_in_model=False):
        project_dict = {}
        project_dict['info'] = self._info
        project_dict['project_with_experiments'] = self._project_with_experiments
        project_dict['project_created'] = self._project_created
        if self._models is not None:
            project_dict['models'] = self._models.as_dict(skip=['interface'])
        if include_materials_not_in_model:
            self._add_materials_not_in_model_dict(project_dict)
        if self._project_with_experiments:
            self._add_experiments_to_dict(project_dict)
        if self._minimizer is not None:
            project_dict['minimizer'] = self._minimizer.name
        if self._calculator is not None:
            project_dict['calculator'] = [self._calculator.current_interface_name]
        if self._colors is not None:
            project_dict['colors'] = self._colors
        return project_dict

    def _add_materials_not_in_model_dict(self, project_dict: dict):
        materials_not_in_model = []
        for material in self._materials:
            if material not in self._get_materials_in_models():
                materials_not_in_model.append(material)
        if len(materials_not_in_model) > 0:
            project_dict['materials_not_in_model'] = MaterialCollection(materials_not_in_model).as_dict(skip=['interface'])

    def _add_experiments_to_dict(self, project_dict: dict):
        project_dict['experiments'] = []
        project_dict['experiments_models'] = []
        project_dict['experiments_names'] = []
        for experiment in self._experiments:
            if self._experiments[0].xe is not None:
                project_dict['experiments'].append([experiment.x, experiment.y, experiment.ye, experiment.xe])
            else:
                project_dict['experiments'].append([experiment.x, experiment.y, experiment.ye])
            project_dict['experiments_models'].append(experiment.model.name)
            project_dict['experiments_names'].append(experiment.name)

    def _extract_project_dict(self, project_dict: dict):
        keys = list(project_dict.keys())
        self._info = project_dict['info']
        self._project_with_experiments = project_dict['project_with_experiments']
        if 'models' in keys:
            self._models = None
            self._models = ModelCollection.from_dict(project_dict['models'])

        self._replace_collection(self._get_materials_in_models(), self._materials)

        if 'materials_not_in_model' in keys:
            self._materials.extend(MaterialCollection.from_dict(project_dict['materials_not_in_model']))

        if 'minimizer' in keys:
            self._minimizer = AvailableMinimizers[project_dict['minimizer']]
        else:
            self._minimizer = None
        if 'experiments' in keys:
            self._experiments = self._extract_experiments_from_dict(project_dict)
        else:
            self._experiments = None
        if 'calculator' in keys:
            self._calculator = project_dict['calculator']
        else:
            self._calculator = None

    def _extract_experiments_from_dict(self, project_dict: dict):
        self._experiments: List[DataSet1D] = []

        for i in range(len(project_dict['experiments'])):
            self._experiments.append(
                DataSet1D(
                    name=project_dict['experiments_names'][i],
                    x=project_dict['experiments'][i][0],
                    y=project_dict['experiments'][i][1],
                    ye=project_dict['experiments'][i][2],
                    xe=project_dict['experiments'][i][3],
                    model=self._models[project_dict['experiments_models'][i]],
                )
            )

    def _get_materials_in_models(self) -> MaterialCollection:
        materials_in_model = MaterialCollection(populate_if_none=False)
        for model in self._models:
            for assembly in model.sample:
                for layer in assembly.layers:
                    materials_in_model.append(layer.material)
        return materials_in_model

    def _replace_collection(self, src_collection: BaseCollection, dst_collection: BaseCollection) -> None:
        # Clear the destination collection
        for i in range(len(dst_collection)):
            dst_collection.pop(0)

        for element in src_collection:
            dst_collection.append(element)
