HTML_TEMPLATE = """<!DOCTYPE html>

<html>

<style>
    th, td {
        padding-right: 18px;
    }
    th {
        text-align: left;
    }
</style>

<body>

    <table>

    <tr></tr>

    <!-- Summary title -->

    <tr>
        <td><h1>Summary</h1></td>
    </tr>

    <tr></tr>

    <!-- Project -->

    project_information_section

    <!-- Phases -->

    <tr>
        <td><h3>Crystal data</h3></td>
    </tr>

    <tr></tr>

    crystal_data_section

    <!-- Experiments -->

    <tr>
        <td><h3>Data collection</h3></td>
    </tr>

    <tr></tr>

    data_collection_section

    <!-- Analysis -->

    <tr>
        <td><h3>Refinement</h3></td>
    </tr>

    <tr></tr>

    <tr>
        <td>Calculation engine</td>
        <td>calculation_engine &mdash; https://www.cryspy.fr</td>
    </tr>
    <tr>
        <td>Minimization engine</td>
        <td>minimization_engine &mdash; https://lmfit.github.io/lmfit-py</td>
    </tr>
    <tr>
        <td>Goodness-of-fit: reduced <i>&chi;</i><sup>2</sup></td>
        <td>goodness_of_fit</td>
    </tr>
    <tr>
        <td>No. of parameters: total, free, fixed</td>
        <td>num_total_params,&nbsp;&nbsp;num_free_params,&nbsp;&nbsp;num_fixed_params</td>
    </tr>
    <tr>
        <td>No. of constraints</td>
        <td>0</td>
    </tr>

    <tr></tr>

    </table>

</body>

</html>"""


HTML_PROJECT_INFORMATION_TEMPLATE = """
<tr>
    <td><h3>Project information</h3></td>
</tr>

<tr></tr>

<tr>
    <th>Title</th>
    <th>project_title</th>
</tr>
<tr>
    <td>Description</td>
    <td>project_description</td>
</tr>
<tr>
    <td>No. of experiments</td>
    <td>num_experiments</td>
</tr>

<tr></tr>
"""

HTML_CRYSTAL_DATA_TEMPLATE = """
<tr>
    <th>Phase datablock</th>
    <th>phase_name</th>
</tr>
<tr>
    <td>Crystal system, space group</td>
    <td>crystal_system,&nbsp;&nbsp;<i>name_H_M_alt</i></td>
</tr>
<tr>
    <td>Cell lengths: <i>a</i>, <i>b</i>, <i>c</i> (&#8491;)</td>
    <td>length_a,&nbsp;&nbsp;length_b,&nbsp;&nbsp;length_c</td>
</tr>
<tr>
    <td>Cell angles: <i>&#593;</i>, <i>&beta;</i>, <i>&#611;</i> (&deg;)</td>
    <td>angle_alpha,&nbsp;&nbsp;angle_beta,&nbsp;&nbsp;angle_gamma</td>
</tr>

<tr></tr>
"""

HTML_DATA_COLLECTION_TEMPLATE = """
<tr>
    <th>Experiment datablock</th>
    <th>experiment_name</th>
</tr>
<tr>
    <td>Radiation probe</td>
    <td>radiation_probe</td>
</tr>
<tr>
    <td>Radiation type</td>
    <td>radiation_type</td>
</tr>
<tr>
    <td>Measured range: min, max, inc (range_units)</td>
    <td>range_min,&nbsp;&nbsp;range_max,&nbsp;&nbsp;range_inc</td>
</tr>
<tr>
    <td>No. of data points</td>
    <td>num_data_points</td>
</tr>

<tr></tr>
"""
