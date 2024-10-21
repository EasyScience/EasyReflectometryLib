import datetime
import json
import os
from pathlib import Path
from typing import List
from typing import Optional
from typing import Union

import numpy as np
from easyscience import global_object
from easyscience.fitting import AvailableMinimizers

from easyreflectometry.calculators import CalculatorFactory
from easyreflectometry.data import DataSet1D
from easyreflectometry.model import Model
from easyreflectometry.model import ModelCollection
from easyreflectometry.model import PercentageFhwm
from easyreflectometry.sample import Layer
from easyreflectometry.sample import MaterialCollection
from easyreflectometry.sample import Multilayer
from easyreflectometry.sample import Sample
from easyreflectometry.sample.collections.base_collection import BaseCollection

Q_MIN = 0.001
Q_MAX = 0.3
Q_ELEMENTS = 500

EXPERIMENTAL_DATA = [
    DataSet1D(
        name='Example Data 0',
        x=np.linspace(Q_MIN, Q_MAX, Q_ELEMENTS),
        y=3 * np.linspace(Q_MIN, Q_MAX, Q_ELEMENTS),
        ye=0.1 * np.linspace(Q_MIN, Q_MAX, Q_ELEMENTS),
    )
]


class Project:
    def __init__(self):
        self._info = self._default_info()
        self._path_project_parent = Path(os.path.expanduser('~'))
        self._models = ModelCollection(populate_if_none=False, unique_name='project_models')
        self._materials = MaterialCollection(populate_if_none=False, unique_name='project_materials')
        self._calculator = CalculatorFactory()
        self._minimizer = AvailableMinimizers.LMFit_leastsq
        self._experiments: List[DataSet1D] = None
        self._colors = None
        self._report = None

        # Project flags
        self._created = False
        self._with_experiments = False

    def reset(self):
        del self._models
        del self._materials
        global_object.map._clear()

        self._models = ModelCollection(populate_if_none=False, unique_name='project_models')
        self._materials = MaterialCollection(populate_if_none=False, unique_name='project_materials')

        self._info = self._default_info()
        self._path_project_parent = Path(os.path.expanduser('~'))
        self._calculator = CalculatorFactory()
        self._minimizer = AvailableMinimizers.LMFit_leastsq
        self._experiments = None
        self._colors = None
        self._report = None

        # Project flags
        self._created = False
        self._with_experiments = False

    @property
    def created(self) -> bool:
        return self._created

    @property
    def path(self):
        return self._path_project_parent / self._info['name']

    def set_path_project_parent(self, path: Union[Path, str]):
        self._path_project_parent = Path(path)

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
    def path_json(self):
        return self.path / 'project.json'

    def sld_data_for_model_at_index(self, index: int = 0) -> DataSet1D:
        self.models[index].interface = self._calculator
        sld = self.models[index].interface().sld_profile(self._models[index].unique_name)
        return DataSet1D(
            name=f'SLD for Model {index}',
            x=sld[0],
            y=sld[1],
        )

    def sample_data_for_model_at_index(self, index: int = 0, q_range: Optional[np.array] = None) -> DataSet1D:
        original_resolution_function = self.models[index].resolution_function
        self.models[index].resolution_function = PercentageFhwm(0)
        reflectivity_data = self.model_data_for_model_at_index(index, q_range)
        self.models[index].resolution_function = original_resolution_function

        return reflectivity_data

    def model_data_for_model_at_index(self, index: int = 0, q_range: Optional[np.array] = None) -> DataSet1D:
        if q_range is None:
            q_range = np.linspace(Q_MIN, Q_MAX, Q_ELEMENTS)
        self.models[index].interface = self._calculator
        reflectivity = self.models[index].interface().reflectity_profile(q_range, self._models[index].unique_name)
        return DataSet1D(
            name=f'Reflectivity for Model {index}',
            x=q_range,
            y=reflectivity,
        )

    def experimental_data_for_model_at_index(self, index: int = 0) -> DataSet1D:
        return EXPERIMENTAL_DATA[index]

    def default_model(self):
        self._replace_collection(MaterialCollection(), self._materials)

        layers = [
            Layer(material=self._materials[0], thickness=0.0, roughness=0.0, name='Vacuum Layer', interface=self._calculator),
            Layer(material=self._materials[1], thickness=100.0, roughness=3.0, name='Multi-layer', interface=self._calculator),
            Layer(material=self._materials[2], thickness=0.0, roughness=1.2, name='Si Layer', interface=self._calculator),
        ]
        assemblies = [
            Multilayer(layers[0], name='Superphase', interface=self._calculator),
            Multilayer(layers[1], name='Multi-layer', interface=self._calculator),
            Multilayer(layers[2], name='Subphase', interface=self._calculator),
        ]
        sample = Sample(*assemblies, interface=self._calculator)
        sample[0].layers[0].thickness.enabled = False
        sample[0].layers[0].roughness.enabled = False
        sample[-1].layers[-1].thickness.enabled = False
        model = Model(sample=sample, interface=self._calculator)
        self._replace_collection([model], self._models)

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

    def _default_info(self):
        return dict(
            name='Example Project',
            short_description='reflectometry, 1D',
            samples='None',
            experiments='None',
            modified=datetime.datetime.now().strftime('%d.%m.%Y %H:%M'),
        )

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
            os.makedirs(self.path / 'experiments')
            self._created = True
            self._timestamp_modification()
        else:
            print(f'ERROR: Directory {self.path} already exists')

    def save_as_json(self, overwrite=False):
        if self.path_json.exists() and overwrite:
            print(f'File already exists {self.path_json}. Overwriting...')
            self.path_json.unlink()
        try:
            project_json = json.dumps(self.as_dict(include_materials_not_in_model=True), indent=4)
            self.path_json.parent.mkdir(exist_ok=True, parents=True)
            with open(self.path_json, mode='x') as file:
                file.write(project_json)
        except Exception as exception:
            print(exception)

    def load_from_json(self, path: Optional[Union[Path, str]] = None):
        path = Path(path)
        if path is None:
            path = self.path_json
        if path.exists():
            with open(path, 'r') as file:
                project_dict = json.load(file)
                self.reset()
                self.from_dict(project_dict)
            self._path_project_parent = path.parents[1]
            self._created = True
        else:
            print(f'ERROR: File {path} does not exist')

    def as_dict(self, include_materials_not_in_model=False):
        project_dict = {}
        project_dict['info'] = self._info
        project_dict['with_experiments'] = self._with_experiments
        if self._models is not None:
            project_dict['models'] = self._models.as_dict(skip=['interface'])
        if include_materials_not_in_model:
            self._as_dict_add_materials_not_in_model_dict(project_dict)
        if self._with_experiments:
            self._as_dict_add_experiments(project_dict)
        if self._minimizer is not None:
            project_dict['minimizer'] = self._minimizer.name
        if self._calculator is not None:
            project_dict['calculator'] = self._calculator.current_interface_name
        if self._colors is not None:
            project_dict['colors'] = self._colors
        return project_dict

    def _as_dict_add_materials_not_in_model_dict(self, project_dict: dict):
        materials_not_in_model = []
        for material in self._materials:
            if material not in self._get_materials_in_models():
                materials_not_in_model.append(material)
        if len(materials_not_in_model) > 0:
            project_dict['materials_not_in_model'] = MaterialCollection(materials_not_in_model).as_dict(skip=['interface'])

    def _as_dict_add_experiments(self, project_dict: dict):
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

    def from_dict(self, project_dict: dict):
        keys = list(project_dict.keys())
        self._info = project_dict['info']
        self._with_experiments = project_dict['with_experiments']
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
            self._experiments = self._from_dict_extract_experiments(project_dict)
        else:
            self._experiments = None
        if 'calculator' in keys:
            self._calculator.switch(project_dict['calculator'])

    def _from_dict_extract_experiments(self, project_dict: dict):
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

    def _timestamp_modification(self):
        self._info['modified'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
