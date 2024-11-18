import os
from unittest.mock import MagicMock

import pytest
from easyscience import global_object

import easyreflectometry
from easyreflectometry import Project
from easyreflectometry.summary import Summary

PATH_STATIC = os.path.join(os.path.dirname(easyreflectometry.__file__), '..', '..', 'tests', '_static')


class TestSummary:
    @pytest.fixture
    def project(self) -> Project:
        global_object.map._clear()
        project = Project()
        project.default_model()
        return project

    def test_constructor(self, project: Project) -> None:
        # When Then
        result = Summary(project)

        # Expect
        assert result._project == project

    def test_compile_html_summary(self, project: Project) -> None:
        # When
        project._created = True
        summary = Summary(project)
        summary._project_information_section = MagicMock(return_value='project result')
        summary._sample_section = MagicMock(return_value='sample result')
        summary._experiments_section = MagicMock(return_value='_experiments results')
        summary._refinement_section = MagicMock(return_value='refinement result')

        # Then
        result = summary.compile_html_summary()

        # Expect
        assert (
            result
            == '<!DOCTYPE html>\n\n<html>\n\n<style>\n    th, td {\n        padding-right: 18px;\n    }\n    th {\n        text-align: left;\n    }\n</style>\n\n<body>\n\n    <table>\n\n    <tr></tr>\n\n    <!-- Summary title -->\n\n    <tr>\n        <td><h1>Summary</h1></td>\n    </tr>\n\n    <tr></tr>\n\n    <!-- Project -->\n\n    project result\n\n    <!-- Phases -->\n\n    <tr>\n        <td><h3>Crystal data</h3></td>\n    </tr>\n\n    <tr></tr>\n\n    crystal_data_section\n\n    <!-- Experiments -->\n\n    <tr>\n        <td><h3>Experiments</h3></td>\n    </tr>\n\n    <tr></tr>\n\n    _experiments results\n\n    <!-- Analysis -->\n\n    refinement result\n\n    </table>\n\n</body>\n\n</html>'
        )

    def test_project_information_section(self, project: Project) -> None:
        # When
        project._created = True
        summary = Summary(project)

        # Then
        html = summary._project_information_section()

        # Expect
        assert (
            html
            == '\n<tr>\n    <td><h3>Project information</h3></td>\n</tr>\n\n<tr></tr>\n\n<tr>\n    <th>Title</th>\n    <th>ExampleProject</th>\n</tr>\n<tr>\n    <td>Description</td>\n    <td>Reflectometry, 1D</td>\n</tr>\n<tr>\n    <td>No. of experiments</td>\n    <td>0</td>\n</tr>\n\n<tr></tr>\n'
        )

    def test_sample_section(self, project: Project) -> None:
        # When
        project._created = True
        summary = Summary(project)

        # Then
        html = summary._sample_section()

        # Expect
        assert (
            html
            == '\n<tr>\n    <th>sld 0.0 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>isld 0.0 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>sld 6.335 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>isld 0.0 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>sld 2.074 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>isld 0.0 1/Å^2 0.0</th>\n</tr>\n\n\n<tr>\n    <th>thickness 0.0 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>roughness 0.0 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>thickness 100.0 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>roughness 3.0 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>thickness 0.0 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>roughness 1.2 Å 0.0</th>\n</tr>\n\n\n<tr>\n    <th>scale 1.0 dimensionless 0.0</th>\n</tr>\n\n\n<tr>\n    <th>background 1e-08 dimensionless 0.0</th>\n</tr>\n'
        )

    def test_experiments_section(self, project: Project) -> None:
        # When
        project._created = True
        fpath = os.path.join(PATH_STATIC, 'example.ort')
        project.load_experiment_for_model_at_index(fpath)
        summary = Summary(project)

        # Then
        html = summary._experiments_section()

        # Expect
        assert (
            html
            == '\n<tr>\n    <th>Experiment datablock</th>\n    <th>Experiment for Model 0</th>\n</tr>\n<tr>\n    <td>Radiation probe</td>\n    <td>radiation_probe</td>\n</tr>\n<tr>\n    <td>Radiation type</td>\n    <td>radiation_type</td>\n</tr>\n<tr>\n    <td>Measured range: min, max, inc (Å⁻¹)</td>\n    <td>9.26972e-08,&nbsp;&nbsp;1.1171,&nbsp;&nbsp;range_inc</td>\n</tr>\n<tr>\n    <td>No. of data points</td>\n    <td>408</td>\n</tr>\n\n<tr></tr>\n'
        )

    def test_refinement_section(self, project: Project) -> None:
        # When
        project._created = True
        summary = Summary(project)

        # Then
        html = summary._refinement_section()

        # Expect
        assert (
            html
            == '\n<tr>\n    <td><h3>Refinement</h3></td>\n</tr>\n\n<tr></tr>\n\n<tr>\n    <td>Calculation engine</td>\n    <td>refnx</td>\n</tr>\n<tr>\n    <td>Minimization engine</td>\n    <td>LMFit_leastsq</td>\n</tr>\n<tr>\n    <td>Goodness-of-fit: reduced <i>&chi;</i><sup>2</sup></td>\n    <td>goodness_of_fit</td>\n</tr>\n<tr>\n    <td>No. of parameters: total, free, fixed</td>\n    <td>14, 0, 14</td>\n</tr>\n<tr>\n    <td>No. of constraints</td>\n    <td>num_constriants</td>\n</tr>\n\n<tr></tr>\n'
        )
