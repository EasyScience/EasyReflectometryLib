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
        summary._project_information_section = MagicMock(return_value='project result html')
        summary._sample_section = MagicMock(return_value='sample result html')
        summary._experiments_section = MagicMock(return_value='experiments results html')
        summary._refinement_section = MagicMock(return_value='refinement result html')

        # Then
        result = summary.compile_html_summary()

        # Expect
        assert 'project result html' in result
        assert 'sample result html' in result
        assert 'experiments results html' in result
        assert 'refinement result html' in result

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
        assert 'name' in html
        assert 'value' in html
        assert 'unit' in html
        assert 'error' in html

        assert 'sld' in html
        assert 'isld' in html
        assert 'thickness' in html
        assert 'background' in html

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
