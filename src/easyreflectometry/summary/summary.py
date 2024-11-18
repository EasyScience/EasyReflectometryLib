from easyscience import global_object

from easyreflectometry import Project
from easyreflectometry.utils import count_fixed_parameters
from easyreflectometry.utils import count_free_parameters
from easyreflectometry.utils import count_parameter_user_constraints

from .html_templates import HTML_DATA_COLLECTION_TEMPLATE
from .html_templates import HTML_PARAMETER_HEADER_TEMPLATE
from .html_templates import HTML_PARAMETER_TEMPLATE
from .html_templates import HTML_PROJECT_INFORMATION_TEMPLATE
from .html_templates import HTML_REFINEMENT_TEMPLATE
from .html_templates import HTML_TEMPLATE


class Summary:
    def __init__(self, project: Project):
        self._project = project

    def compile_html_summary(self):
        html = HTML_TEMPLATE
        project_information_section = self._project_information_section()
        if project_information_section == '':  # no project information
            project_information_section = '<td>No project information</td>'
        html = html.replace('project_information_section', project_information_section)

        html = html.replace('sample_section', self._sample_section())

        experiments_section = self._experiments_section()
        if experiments_section == '':  # no experiments
            experiments_section = '<td>No experiments</td>'
        html = html.replace('experiments_section', experiments_section)

        html = html.replace('refinement_section', self._refinement_section())

        return html

    def save_html_summary(self, filename: str) -> None:
        html = self.compile_html_summary()
        with open(filename, 'w') as f:
            f.write(html)

    def _project_information_section(self) -> None:
        html_project = ''
        if self._project.created:
            html_project = HTML_PROJECT_INFORMATION_TEMPLATE
            name = self._project._info['name']
            short_description = self._project._info['short_description']
            html_project = html_project.replace('project_title', f'{name}')
            html_project = html_project.replace('project_description', f'{short_description}')
            html_project = html_project.replace('num_experiments', f'{len(self._project.experiments)}')
        return html_project

    def _sample_section(self) -> None:
        html_parameters = []

        html_parameter = HTML_PARAMETER_HEADER_TEMPLATE
        html_parameter = html_parameter.replace('parameter_name', 'Name')
        html_parameter = html_parameter.replace('parameter_value', 'Value')
        html_parameter = html_parameter.replace('parameter_unit', 'Unit')
        html_parameter = html_parameter.replace('parameter_error', 'Error')
        html_parameters.append(html_parameter)

        for parameter in self._project.parameters:
            path = global_object.map.find_path(
                self._project._models[self._project.current_model_index].unique_name, parameter.unique_name
            )
            if 0 < len(path):
                name = f'{global_object.map.get_item_by_key(path[-2]).name} {global_object.map.get_item_by_key(path[-1]).name}'
            else:
                name = parameter.name
            value = parameter.value
            unit = parameter.unit
            error = parameter.error

            html_parameter = HTML_PARAMETER_TEMPLATE
            html_parameter = html_parameter.replace('parameter_name', f'{name}')
            html_parameter = html_parameter.replace('parameter_value', f'{value}')
            html_parameter = html_parameter.replace('parameter_unit', f'{unit}')
            html_parameter = html_parameter.replace('parameter_error', f'{error}')
            html_parameters.append(html_parameter)

        html_parameters_str = '\n'.join(html_parameters)

        return html_parameters_str

    def _experiments_section(self) -> None:
        html_experiments = []

        for idx, experiment in self._project.experiments.items():
            experiment_name = experiment.name
            num_data_points = len(experiment.x)
            resolution_function = self._project.models[idx].resolution_function.as_dict()['smearing']
            if resolution_function == 'PercentageFhwm':
                precentage = self._project.models[idx].resolution_function.as_dict()['constant']
                resolution_function = f'{resolution_function} {precentage}%'
            range_min = min(experiment.y)
            range_max = max(experiment.y)
            range_units = 'Å⁻¹'
            html_experiment = HTML_DATA_COLLECTION_TEMPLATE
            html_experiment = html_experiment.replace('experiment_name', f'{experiment_name}')
            html_experiment = html_experiment.replace('range_min', f'{range_min}')
            html_experiment = html_experiment.replace('range_max', f'{range_max}')
            html_experiment = html_experiment.replace('range_units', f'{range_units}')
            html_experiment = html_experiment.replace('num_data_points', f'{num_data_points}')
            html_experiment = html_experiment.replace('resolution_function', f'{resolution_function}')
            html_experiments.append(html_experiment)

        html_experiments_str = '\n'.join(html_experiments)

        return html_experiments_str

    def _refinement_section(
        self,
    ) -> None:
        html_refinement = HTML_REFINEMENT_TEMPLATE
        num_free_params = count_free_parameters(self._project)
        num_fixed_params = count_fixed_parameters(self._project)
        num_params = num_free_params + num_fixed_params
        #        goodness_of_fit = self._project.status.goodnessOfFit
        #        goodness_of_fit = goodness_of_fit.split(' → ')[-1]
        num_constraints = count_parameter_user_constraints(self._project)

        html_refinement = html_refinement.replace('calculation_engine', f'{self._project._calculator.current_interface_name}')
        html_refinement = html_refinement.replace('minimization_engine', f'{self._project.minimizer.name}')
        #        html = html.replace('goodness_of_fit', f'{goodness_of_fit}')
        html_refinement = html_refinement.replace('num_total_params', f'{num_params}')
        html_refinement = html_refinement.replace('num_free_params', f'{num_free_params}')
        html_refinement = html_refinement.replace('num_fixed_params', f'{num_fixed_params}')
        html_refinement = html_refinement.replace('num_constriants', f'{num_constraints}')
        return html_refinement
