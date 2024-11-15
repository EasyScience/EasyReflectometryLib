import pytest

from easyreflectometry import Project
from easyreflectometry.summary import Summary
from easyreflectometry.summary.html_templates import HTML_TEMPLATE


class TestSummary:
    @pytest.fixture
    def project(self) -> Project:
        project = Project()
        project.default_model()
        return project

    def test_constructor(self, project: Project) -> None:
        # When Then
        result = Summary(project)

        # Expect
        assert result._project == project

    # def test_compile_html_summary(self, project: Project) -> None:
    #     # When
    #     summary = Summary(project)

    #     # Then
    #     result = summary.compile_html_summary()

    #     # Expect
    #     assert result is not None

    def test_set_project_information_section(self, project: Project) -> None:
        # When
        project._created = True
        summary = Summary(project)
        html = 'project_information_section'

        # Then
        html = summary._set_project_information_section(html)

        # Expect
        assert (
            html
            == '\n<tr>\n    <td><h3>Project information</h3></td>\n</tr>\n\n<tr></tr>\n\n<tr>\n    <th>Title</th>\n    <th>Example Project</th>\n</tr>\n<tr>\n    <td>Description</td>\n    <td>reflectometry, 1D</td>\n</tr>\n<tr>\n    <td>No. of experiments</td>\n    <td>0</td>\n</tr>\n\n<tr></tr>\n'
        )
