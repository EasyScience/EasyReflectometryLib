# SPDX-FileCopyrightText: 2025 EasyScience contributors <https://github.com/easyscience>
# SPDX-License-Identifier: BSD-3-Clause

"""ORSO file support: reading and writing `.ort` (text) and `.orb` (binary) files.

Reading is built on ``orsopy.fileio``.  Data columns follow the ORSO
specification: the first four columns are Qz, R, sR, sQz (fixed order); sR and
sQz default to sigma but a ``value_is: FWHM`` declaration is honoured and
converted to sigma on load.  Q values declared in ``1/nm`` are converted to the
internal ``1/angstrom`` unit.  Errors are stored as **variances** on the scipp
arrays (sigma squared), which is also the convention used by
:class:`~easyreflectometry.model.resolution_functions.Pointwise` and by project
serialization (``sQz_data_points``); any exporter must convert back to sigma.

The ORSO "simple model" language is resolved with units honoured (the language
default length unit is **nm**; internal thicknesses/roughnesses are angstrom)
and with sub-stack repetitions mapped to
:class:`~easyreflectometry.sample.assemblies.repeating_multilayer.RepeatingMultilayer`.
"""

import logging
import math
import warnings
from typing import List
from typing import Optional
from typing import Union

import numpy as np
import scipp as sc
from orsopy.fileio import Header
from orsopy.fileio import model_language
from orsopy.fileio import orso
from orsopy.fileio.base import Column
from orsopy.fileio.base import ComplexValue
from orsopy.fileio.base import ErrorColumn
from orsopy.fileio.base import Value
from orsopy.fileio.orso import Orso
from orsopy.fileio.orso import OrsoDataset

from easyreflectometry.data import DataSet1D

from .sample.assemblies.multilayer import Multilayer
from .sample.assemblies.repeating_multilayer import RepeatingMultilayer
from .sample.collections.sample import Sample
from .sample.elements.layers.layer import Layer
from .sample.elements.layers.layer_magnetism import LayerMagnetism
from .sample.elements.materials.material import Material
from .sample.elements.materials.material_density import MaterialDensity
from .sample.elements.materials.material_magnetic import MaterialMagnetic
from .special.calculations import MAGNETIC_SCATTERING_LENGTH
from .special.calculations import mass_density_from_number_density
from .special.calculations import molecular_weight

# Set up logging
logger = logging.getLogger(__name__)

# Mirrors resolution_functions.SIGMA_TO_FWHM; kept local to avoid importing the
# model package from this low-level module (data <-> model import cycle).
SIGMA_TO_FWHM = 2 * np.sqrt(2 * np.log(2))

# The mandatory first line of a text ORSO file; the discriminator for the
# ORSO-vs-plain-text decision (the file extension is not reliable).
ORSO_BANNER = 'ORSO reflectivity data file'

# Magic bytes of an HDF5 container -- how a binary ORSO (.orb, NeXus) file starts.
_HDF5_MAGIC = b'\x89HDF\r\n\x1a\n'

# Length unit -> angstrom conversion factors for model-language values.
_LENGTH_UNIT_TO_ANGSTROM = {
    None: 1.0,
    'angstrom': 1.0,
    'A': 1.0,
    'nm': 10.0,
    'um': 1.0e4,
    'mm': 1.0e7,
}

# SLD unit -> 1/angstrom^2 conversion factors.
_SLD_UNIT_TO_INV_ANGSTROM_SQUARED = {
    None: 1.0,
    '1/angstrom^2': 1.0,
    '1/nm^2': 1.0e-2,
}

# Qz column unit -> 1/angstrom conversion factors.
_Q_UNIT_TO_INV_ANGSTROM = {
    None: 1.0,
    '1/angstrom': 1.0,
    '1/nm': 0.1,
}

# Mass density unit -> g/cm^3 conversion factors.
_MASS_DENSITY_UNIT_TO_G_CM3 = {
    None: 1.0,
    'g/cm^3': 1.0,
    'g/ml': 1.0,
    'kg/m^3': 1.0e-3,
}

# Number density unit -> 1/angstrom^3 (the model-language default is 1/nm^3).
_NUMBER_DENSITY_UNIT_TO_INV_ANGSTROM3 = {
    None: 1.0e-3,
    '1/nm^3': 1.0e-3,
    '1/angstrom^3': 1.0,
    '1/cm^3': 1.0e-24,
}

# Magnetic moment unit -> Bohr magnetons (per formula unit).
_MAGNETIC_MOMENT_UNIT_TO_MUB = {
    None: 1.0,
    'muB': 1.0,
    'mu_B': 1.0,
    'bohr_magneton': 1.0,
}


def is_orso_file(fname: str) -> bool:
    """Whether *fname* is an ORSO file: text with the ORSO banner line, or HDF5 (.orb).

    Parameters
    ----------
    fname : str
        Path to the file.

    Returns
    -------
    bool
        True when the file starts with the ORSO banner or the HDF5 magic bytes.
    """
    try:
        with open(fname, 'rb') as f:
            head = f.read(128)
    except OSError:
        return False
    if head.startswith(_HDF5_MAGIC):
        return True
    try:
        first_line = head.decode('utf-8', errors='replace').splitlines()[0]
    except IndexError:
        return False
    return first_line.lstrip().startswith('#') and ORSO_BANNER in first_line


def _is_binary_orso(fname: str) -> bool:
    """Whether *fname* is a binary (HDF5 / .orb) ORSO file."""
    try:
        with open(fname, 'rb') as f:
            return f.read(8).startswith(_HDF5_MAGIC)
    except OSError:
        return False


def _load_orso_any(fname: str) -> List[OrsoDataset]:
    """Parse an ORSO file, text (`.ort`) or binary (`.orb`), into OrsoDataset objects.

    Parameters
    ----------
    fname : str
        Path to the file.

    Returns
    -------
    List[OrsoDataset]
        The parsed datasets.

    Raises
    ------
    ValueError :
        If the file cannot be parsed as ORSO (the original error is chained).
    """
    fname = str(fname)
    try:
        if _is_binary_orso(fname):
            return orso.load_nexus(fname)
        return orso.load_orso(fname)
    except Exception as e:
        raise ValueError(f'Error loading ORSO file {fname!r}: {e}') from e


def LoadOrso(orso_data):
    """Load a model and data from an ORSO file (path or pre-parsed datasets)."""

    orso_obj = _coerce_orso_object(orso_data)
    sample = load_orso_model(orso_obj)
    data = load_orso_data(orso_obj)
    return sample, data


def _coerce_orso_object(orso_input):
    """Return a parsed ORSO object list from either a path or pre-parsed input."""
    try:
        if orso_input and hasattr(orso_input[0], 'info'):
            return orso_input
    except (TypeError, IndexError):
        pass
    return _load_orso_any(orso_input)


def load_data_from_orso_file(fname: str) -> sc.DataGroup:
    """Load data from an ORSO file (`.ort` text or `.orb` binary).

    Parameters
    ----------
    fname : str
        Path to the file.

    Returns
    -------
    sc.DataGroup
        A scipp DataGroup with data, coords, and attrs.

    Raises
    ------
    ValueError :
        If the file cannot be parsed as ORSO. Parse failures are **not**
        swallowed here; falling back to plain-text loading is the caller's
        decision and only valid when the file carries no ORSO banner.
    """
    orso_data = _load_orso_any(fname)
    return load_orso_data(orso_data)


def _orso_dataset_key(o, index: int) -> Union[str, int]:
    """The name a dataset is stored under: its ``data_set`` label or its index."""
    if o.info.data_set is not None:
        return o.info.data_set
    return index


def _validate_columns(columns, dataset_label) -> None:
    """Warn when the leading four columns do not follow the ORSO layout.

    The spec fixes the order Qz, R, sR, sQz; data is read by position, so a
    file with different columns is very likely misread. The names in
    ``info.columns`` are used as validation only.
    """
    expected = ('Qz', 'R', 'R', 'Qz')
    for position, expected_name in enumerate(expected):
        if position >= len(columns):
            warnings.warn(
                f'ORSO dataset {dataset_label!r} declares only {len(columns)} columns; the specification '
                f'requires Qz, R, sR, sQz (nan-filled when unknown). Missing error columns are treated as absent.',
                UserWarning,
                stacklevel=3,
            )
            return
        column = columns[position]
        name = getattr(column, 'error_of', None) or getattr(column, 'name', None)
        # Legacy (0.1 standard) files use plain columns named 'sR'/'sQz'.
        if position >= 2 and isinstance(name, str) and name.startswith('s'):
            name = name[1:]
        if name != expected_name:
            warnings.warn(
                f'ORSO dataset {dataset_label!r} columns do not follow the specified order '
                f'(Qz, R, sR, sQz): column {position} is {name!r}. Data is read by position '
                f'and may be misinterpreted.',
                UserWarning,
                stacklevel=3,
            )
            return


def _q_unit_scale(column, dataset_label) -> float:
    """Conversion factor from the Qz column unit to the internal 1/angstrom."""
    unit = getattr(column, 'unit', None)
    try:
        return _Q_UNIT_TO_INV_ANGSTROM[unit]
    except KeyError:
        warnings.warn(
            f'ORSO dataset {dataset_label!r} declares Qz unit {unit!r}; expected 1/angstrom or 1/nm. '
            f'Values are used as-is (assumed 1/angstrom).',
            UserWarning,
            stacklevel=3,
        )
        return 1.0


def _error_column_sigma(o, position: int) -> Optional[np.ndarray]:
    """Extract an error column as sigma values, or None when the column is absent.

    Honours ``value_is: FWHM`` by converting to sigma (dividing by 2.3548...).
    """
    if o.data.ndim != 2 or o.data.shape[1] <= position:
        return None
    values = np.asarray(o.data[:, position], dtype=float)
    if position < len(o.info.columns):
        value_is = getattr(o.info.columns[position], 'value_is', None)
        if value_is == 'FWHM':
            values = values / SIGMA_TO_FWHM
    return values


def _clean_sqz(sqz: Optional[np.ndarray], dataset_label) -> Optional[np.ndarray]:
    """Apply the nan policy to the sQz column.

    All-nan (spec-valid "resolution unknown") returns None so that no q-variance
    is stored and the caller falls back to the default percentage smearing.
    Partial nan (common at the low/high-Q extremes of real reductions) is filled
    by interpolating sigma over the valid points -- otherwise a single nan would
    propagate through ``np.interp`` in ``Pointwise`` across the whole range.
    """
    if sqz is None:
        return None
    nan_mask = np.isnan(sqz)
    if not nan_mask.any():
        return sqz
    if nan_mask.all():
        return None
    warnings.warn(
        f'ORSO dataset {dataset_label!r}: {nan_mask.sum()} of {sqz.size} sQz values are nan; '
        f'they are filled by interpolating the resolution over the valid points.',
        UserWarning,
        stacklevel=3,
    )
    valid = ~nan_mask
    indices = np.arange(sqz.size)
    filled = sqz.copy()
    filled[nan_mask] = np.interp(indices[nan_mask], indices[valid], sqz[valid])
    return filled


def _clean_sr(sr: Optional[np.ndarray], dataset_label) -> Optional[np.ndarray]:
    """Apply the nan policy to the sR column.

    All-nan returns None (uncertainty unknown). Partial nan is kept as-is --
    interpolating measurement uncertainties would fabricate fit weights -- but
    is warned about, since nan weights degrade fitting.
    """
    if sr is None:
        return None
    nan_mask = np.isnan(sr)
    if nan_mask.all() and sr.size:
        return None
    if nan_mask.any():
        warnings.warn(
            f'ORSO dataset {dataset_label!r}: {nan_mask.sum()} of {sr.size} sR values are nan; '
            f'these points carry no uncertainty and will degrade fit weighting.',
            UserWarning,
            stacklevel=3,
        )
    return sr


def load_orso_data(orso_data) -> sc.DataGroup:
    """Convert parsed ORSO dataset objects into a scipp DataGroup.

    Q values are converted to 1/angstrom; sR/sQz are converted to sigma when
    declared as FWHM and stored as variances; nan-filled error columns follow
    the policy documented on the cleaning helpers.

    Parameters
    ----------
    orso_data : list
        Parsed ORSO dataset list (as returned by ``orso.load_orso``).

    Returns
    -------
    sc.DataGroup
        A scipp DataGroup with data, coords, and attrs.
    """
    data = {}
    coords = {}
    attrs = {}
    for i, o in enumerate(orso_data):
        name = _orso_dataset_key(o, i)
        _validate_columns(o.info.columns, name)

        q_scale = _q_unit_scale(o.info.columns[0], name)
        qz = np.asarray(o.data[:, 0], dtype=float) * q_scale
        reflectivity = np.asarray(o.data[:, 1], dtype=float)

        sr = _clean_sr(_error_column_sigma(o, 2), name)
        sqz = _clean_sqz(_error_column_sigma(o, 3), name)
        if sqz is not None:
            sqz = sqz * q_scale

        dims = [f'{o.info.columns[0].name}_{name}']
        coords[f'Qz_{name}'] = sc.array(
            dims=dims,
            values=qz,
            variances=np.square(sqz) if sqz is not None else None,
            unit=sc.Unit('1/angstrom'),
        )
        r_unit = getattr(o.info.columns[1], 'unit', None)
        try:
            data[f'R_{name}'] = sc.array(
                dims=dims,
                values=reflectivity,
                variances=np.square(sr) if sr is not None else None,
                unit=sc.Unit(r_unit) if r_unit is not None else None,
            )
        except TypeError:
            data[f'R_{name}'] = sc.array(
                dims=dims,
                values=reflectivity,
                variances=np.square(sr) if sr is not None else None,
            )
        attrs[f'R_{name}'] = {'orso_header': sc.scalar(Header.asdict(o.info))}
    data_group = sc.DataGroup(data=data, coords=coords, attrs=attrs)
    return data_group


# ---------------------------------------------------------------------------
# Model language -> Sample
# ---------------------------------------------------------------------------


def _length_to_angstrom(value) -> float:
    """Convert a model-language length (Value with unit, or bare number) to angstrom."""
    if value is None:
        return 0.0
    magnitude = getattr(value, 'magnitude', value)
    if magnitude is None:
        return 0.0
    unit = getattr(value, 'unit', None)
    try:
        factor = _LENGTH_UNIT_TO_ANGSTROM[unit]
    except KeyError:
        warnings.warn(
            f'Unknown ORSO length unit {unit!r}; value used as angstrom.',
            UserWarning,
            stacklevel=4,
        )
        factor = 1.0
    return float(magnitude) * factor


def load_orso_model(orso_data) -> Sample:
    """Load a model from an ORSO file and return a Sample object.

    The **original** ``sample.model`` object is resolved (keeping ``globals``,
    ``materials``, ``sub_stacks`` and ``composits``), so declared units --
    including the model-language default length unit of **nm** -- are honoured
    and converted to the internal angstrom.  Sub-stacks with repetitions map to
    :class:`RepeatingMultilayer`; density-defined materials stay density-defined
    (:class:`MaterialDensity`) instead of being flattened to a numeric SLD.

    The stack is converted to a proper Sample structure:
    - First layer -> Superphase assembly (thickness=0, roughness=0, both fixed)
    - Middle layers -> 'Loaded layer' Multilayer assembly (parameters enabled),
      with repeated sub-stacks as RepeatingMultilayer assemblies
    - Last layer -> Subphase assembly (thickness=0 fixed, roughness enabled)

    Parameters
    ----------
    orso_data : list
        Parsed ORSO dataset list (as returned by ``orso.load_orso``).

    Raises
    ------
    ValueError :
        If ORSO layers could not be resolved or fewer than 2 layers.

    Returns
    -------
    Sample
        An EasyReflectometry Sample object.
    """
    sample_model = orso_data[0].info.data_source.sample.model
    if sample_model is None:
        warnings.warn(
            'ORSO file does not contain a sample model definition. Only experimental data can be loaded from this file.',
            UserWarning,
            stacklevel=2,
        )
        return None
    if isinstance(sample_model, model_language.SampleModel):
        # Use the file's model as parsed: rebuilding it from `stack` and
        # `layers` alone (as done previously) silently dropped the
        # `materials` / `sub_stacks` / `composits` definitions, so named
        # materials could not be resolved and their SLDs read as 0.
        orso_sample = sample_model
    else:
        stack_str = sample_model.stack
        layers_dict = sample_model.layers if hasattr(sample_model, 'layers') else None
        orso_sample = model_language.SampleModel(
            stack=stack_str,
            layers=layers_dict,
            materials=getattr(sample_model, 'materials', None),
            sub_stacks=getattr(sample_model, 'sub_stacks', None),
            composits=getattr(sample_model, 'composits', None),
            globals=getattr(sample_model, 'globals', None),
        )

    # Resolve the original model (globals/materials/sub_stacks intact) at the
    # stack level: resolve_stack() keeps SubStack objects (and with them the
    # repetition counts) that resolve_to_layers()/resolve_to_blocks() flatten.
    orso_blocks = orso_sample.resolve_stack()

    # Handle case where layers are not resolved correctly
    if not orso_blocks:
        raise ValueError('Could not resolve ORSO layers.')

    # Plain layers still need their material resolved (what
    # resolve_to_layers() would have done); a failure is warned about instead
    # of silently re-resolving the whole stack a different way.
    for block in orso_blocks:
        if isinstance(block, model_language.Layer):
            _generate_layer_material(block)

    # The ambient (first) and substrate (last) entries must be plain layers;
    # flatten pathological edge sub-stacks.
    if not isinstance(orso_blocks[0], model_language.Layer):
        warnings.warn('First ORSO stack item is a sub-stack; its layers are used directly.', UserWarning, stacklevel=2)
        orso_blocks = list(orso_blocks[0].resolve_to_layers()) + orso_blocks[1:]
    if not isinstance(orso_blocks[-1], model_language.Layer):
        warnings.warn('Last ORSO stack item is a sub-stack; its layers are used directly.', UserWarning, stacklevel=2)
        orso_blocks = orso_blocks[:-1] + list(orso_blocks[-1].resolve_to_layers())

    total_layers = sum(1 if isinstance(block, model_language.Layer) else max(len(block.sequence), 1) for block in orso_blocks)
    if total_layers < 2:
        raise ValueError('ORSO stack must contain at least 2 layers (superphase and subphase).')

    logger.debug(f'Resolved blocks: {orso_blocks}')

    # Create Superphase from first layer (thickness=0, roughness=0, both fixed)
    superphase_layer = _convert_orso_layer_to_erl(orso_blocks[0])
    superphase_layer.thickness.value = 0.0
    superphase_layer.roughness.value = 0.0
    superphase_layer.thickness.fixed = True
    superphase_layer.roughness.fixed = True
    superphase = Multilayer(superphase_layer, name='Superphase')

    # Create Subphase from last layer (thickness=0 fixed, roughness enabled)
    subphase_layer = _convert_orso_layer_to_erl(orso_blocks[-1])
    subphase_layer.thickness.value = 0.0
    subphase_layer.thickness.fixed = True
    subphase_layer.roughness.fixed = False
    subphase = Multilayer(subphase_layer, name='Subphase')

    # Middle blocks: consecutive plain layers group into one Multilayer;
    # sub-stacks become their own (repeating) assemblies.
    middle_assemblies = []
    pending_layers = []

    def flush_pending():
        if pending_layers:
            middle_assemblies.append(Multilayer(list(pending_layers), name='Loaded layer'))
            pending_layers.clear()

    for block in orso_blocks[1:-1]:
        if isinstance(block, model_language.Layer):
            pending_layers.append(_convert_orso_layer_to_erl(block))
        else:
            flush_pending()
            middle_assemblies.append(_convert_orso_substack_to_erl(block))
    flush_pending()

    # Keep the historic single-group name; disambiguate multiple plain groups.
    plain_groups = [a for a in middle_assemblies if a.name == 'Loaded layer']
    if len(plain_groups) > 1:
        for k, assembly in enumerate(plain_groups):
            assembly.name = f'Loaded layer {k}'

    # Create Sample from the file
    sample_info = orso_data[0].info.data_source.sample
    sample_name = sample_info.name if sample_info.name else 'ORSO Sample'

    sample = Sample(superphase, *middle_assemblies, subphase, name=sample_name)
    return sample


def _generate_layer_material(orso_layer) -> None:
    """Resolve a model-language layer's material in place (formula -> SLD).

    This is the per-layer half of orsopy's ``resolve_to_layers()``; a failure
    is warned about (the material then imports with its declared values, or an
    SLD of 0) instead of silently re-resolving the stack a different way.
    """
    try:
        if orso_layer.material is None:
            orso_layer.generate_material()
        orso_layer.material.generate_density()
    except Exception as e:
        warnings.warn(
            f'Could not resolve material for ORSO layer {getattr(orso_layer, "original_name", None) or orso_layer!r}: {e}',
            UserWarning,
            stacklevel=3,
        )


def _convert_orso_substack_to_erl(block) -> Multilayer:
    """Convert an ORSO SubStack block into a (repeating) multilayer assembly."""
    repetitions = int(getattr(block, 'repetitions', 1) or 1)
    # SubStack.resolve_to_layers() returns layers * repetitions; resolve one
    # period by temporarily neutralizing the repetition count.
    original_repetitions = block.repetitions
    try:
        block.repetitions = 1
        period = block.resolve_to_layers()
    except Exception as e:
        warnings.warn(
            f'Could not fully resolve ORSO sub-stack ({e}); using its raw layer sequence.',
            UserWarning,
            stacklevel=3,
        )
        period = [item for item in block.sequence if isinstance(item, model_language.Layer)]
    finally:
        block.repetitions = original_repetitions
    erl_layers = [_convert_orso_layer_to_erl(orso_layer) for orso_layer in period]
    name = getattr(block, 'original_name', None) or 'Multilayer'
    if repetitions > 1 and any(layer.magnetism is not None for layer in erl_layers):
        warnings.warn(
            f'Sub-stack "{name}" repeats magnetic layers; refl1d cannot calculate magnetism inside a repeating multilayer.',
            UserWarning,
            stacklevel=3,
        )
    if repetitions > 1:
        return RepeatingMultilayer(erl_layers, repetitions=repetitions, name=name)
    return Multilayer(erl_layers, name=name)


def _convert_orso_layer_to_erl(layer):
    r"""Helper function to convert an ORSO layer to an EasyReflectometry layer."""
    material = layer.material
    # Prefer original_name for the material name, fall back to the formula; a
    # material defined only by its SLD has neither, so never leave it None.
    formula = getattr(material, 'formula', None)
    m_name = layer.original_name if layer.original_name is not None else formula
    if m_name is None:
        m_name = 'material'

    erl_material, rho_m = _convert_orso_material_to_erl(material, m_name)
    # A moment becomes layer magnetism aligned with an in-plane field (the model
    # language has no direction): coupled to a magnetic material, or a direct
    # magnetic SLD when the material has no formula.
    coupled = isinstance(erl_material, MaterialMagnetic)
    magnetism = LayerMagnetism(rho_m=rho_m) if rho_m is not None else None

    # Create and return ERL layer; lengths honour the declared unit (nm default).
    return Layer(
        material=erl_material,
        thickness=_length_to_angstrom(layer.thickness),
        roughness=_length_to_angstrom(layer.roughness),
        name=layer.original_name if layer.original_name is not None else m_name,
        magnetism=magnetism,
        rho_m_coupled=coupled,
    )


def _convert_orso_material_to_erl(material, material_name) -> tuple:
    """Convert an ORSO material to an ERL material and a magnetic SLD.

    A formula with a density (mass density, or number density converted with
    the formula's weight; the mass density wins when both are given) stays
    density-defined as :class:`MaterialDensity`, so formula and density remain
    editable. With a magnetic moment it becomes a :class:`MaterialMagnetic`,
    and an explicit SLD then overrides the formula's nuclear SLD. Without a
    usable formula the material is an SLD :class:`Material`, and a moment needs
    a number density.

    Returns
    -------
    tuple
        ``(material, rho_m)``: ``rho_m`` is a magnetic SLD in 1e-6/angstrom^2 for
        the layer to carry directly, or None (non-magnetic, or the material
        carries it).
    """
    name = material_name
    formula = getattr(material, 'formula', None) or name
    mass_density = _orso_quantity(material.mass_density, _MASS_DENSITY_UNIT_TO_G_CM3, 'mass density', name)
    number_density = _orso_quantity(material.number_density, _NUMBER_DENSITY_UNIT_TO_INV_ANGSTROM3, 'number density', name)
    moment = _orso_quantity(material.magnetic_moment, _MAGNETIC_MOMENT_UNIT_TO_MUB, 'magnetic moment', name)
    if material.relative_density not in (None, 1.0):
        warnings.warn(
            f'ORSO relative_density of "{name}" is not applied; its densities are used as given.',
            UserWarning,
            stacklevel=4,
        )

    weight = _formula_weight(formula)
    if weight is not None and number_density is not None:
        from_number_density = mass_density_from_number_density(number_density, weight)
        if mass_density is None:
            mass_density = from_number_density
        elif not math.isclose(mass_density, from_number_density, rel_tol=0.01):
            warnings.warn(
                f'ORSO mass and number density of "{name}" disagree; the mass density is used.',
                UserWarning,
                stacklevel=4,
            )

    if mass_density is not None and weight is not None and (material.sld is None or moment is not None):
        if moment is None:
            erl_material = MaterialDensity(chemical_structure=formula, density=mass_density, name=name)
        else:
            erl_material = MaterialMagnetic(chemical_structure=formula, density=mass_density, magnetic_moment=moment, name=name)
        if material.sld is not None:
            erl_material.sld_coupled = False
            erl_material.sld.value, erl_material.isld.value = _get_sld_values(material, name)
        return erl_material, None

    m_sld, m_isld = _get_sld_values(material, name)
    erl_material = Material(sld=m_sld, isld=m_isld, name=name)
    if moment is None:
        return erl_material, None
    if number_density is None:
        warnings.warn(
            f'Magnetic moment of "{name}" not imported: it needs a number density, or a mass density with a chemical formula.',
            UserWarning,
            stacklevel=4,
        )
        return erl_material, None
    return erl_material, number_density * moment * MAGNETIC_SCATTERING_LENGTH * 1e6


def _orso_quantity(value, unit_factors: dict, quantity: str, material_name) -> Optional[float]:
    """An ORSO model value in the internal unit; None when absent, or in an
    unknown unit (warned: a guessed unit can be off by orders of magnitude)."""
    if value is None:
        return None
    unit = getattr(value, 'unit', None)
    if unit not in unit_factors:
        warnings.warn(
            f'Unknown ORSO {quantity} unit {unit!r} for "{material_name}"; the {quantity} is ignored.',
            UserWarning,
            stacklevel=5,
        )
        return None
    return float(getattr(value, 'magnitude', value)) * unit_factors[unit]


def _formula_weight(formula) -> Optional[float]:
    """Molecular weight of a formula; None when it is not a chemical formula."""
    try:
        weight = molecular_weight(formula)
    except Exception:
        return None
    return weight or None


def _get_sld_values(material, material_name):
    """Extract the SLD values of a material, 0 when it declares none.

    Density-defined materials are converted by `_convert_orso_material_to_erl`;
    a density reaching this point could not be used (no formula, or an unknown
    unit) and is not reinterpreted here.

    Note: ORSO stores SLD in absolute units (A^-2), but the internal representation
    uses 10^-6 A^-2. When reading directly from ORSO, we multiply by 1e6 to convert.
    """
    if material.sld is None:
        m_sld = 0.0
        m_isld = 0.0
    else:
        # ORSO stores SLD in absolute units (A^-2, or 1/nm^2 when declared).
        # Convert to internal representation (10^-6 A^-2).
        sld = material.sld
        unit = getattr(sld, 'unit', None)
        try:
            unit_factor = _SLD_UNIT_TO_INV_ANGSTROM_SQUARED[unit]
        except KeyError:
            warnings.warn(
                f'Unknown ORSO SLD unit {unit!r}; value used as 1/angstrom^2.',
                UserWarning,
                stacklevel=4,
            )
            unit_factor = 1.0
        if isinstance(sld, ComplexValue):
            raw_sld = sld.real
            m_sld = raw_sld * unit_factor * 1e6
            m_isld = (sld.imag if sld.imag is not None else 0.0) * unit_factor * 1e6
        else:
            raw_sld = getattr(sld, 'magnitude', sld)
            m_sld = raw_sld * unit_factor * 1e6
            m_isld = 0.0
        if raw_sld != 0.0 and abs(raw_sld) > 1e-2:
            warnings.warn(
                f'ORSO SLD value {raw_sld} for "{material_name}" seems large for '
                f'absolute units (A^-2). Verify the file stores SLD in A^-2, not '
                f'10^-6 A^-2, as the value is multiplied by 1e6 internally.',
                UserWarning,
                stacklevel=3,
            )

    return m_sld, m_isld


# ---------------------------------------------------------------------------
# Sample -> model language, and .ort/.orb export
# ---------------------------------------------------------------------------


def _sanitize_model_key(name: str) -> str:
    """Make a layer name safe for use in the model-language stack string."""
    cleaned = ''.join('_' if character in '|()' else character for character in str(name)).strip()
    return cleaned or 'layer'


def _unique_model_key(existing: dict, name: str) -> str:
    """A stack key not yet present in *existing* (appends a counter if needed)."""
    key = _sanitize_model_key(name)
    if key not in existing:
        return key
    counter = 2
    while f'{key}_{counter}' in existing:
        counter += 1
    return f'{key}_{counter}'


def _layer_material_to_orso(layer) -> model_language.Material:
    """Convert an ERL layer's material, and its magnetism, to an ORSO material.

    The model language stores a moment per formula unit, not a magnetic SLD or
    a direction, so only part of a magnetic layer can be written; whatever is
    lost is warned about. A layer whose material has a number density gets
    the moment matching its magnetic SLD (the material's own moment when the
    layer is coupled to it); the direction is always written as aligned with
    an in-plane field.
    """
    material = layer.material
    sld = ComplexValue(
        real=float(material.sld.value) * 1e-6,
        imag=float(material.isld.value) * 1e-6,
        unit='1/angstrom^2',
    )
    if not isinstance(material, MaterialDensity):
        orso_material = model_language.Material(sld=sld)
    else:
        orso_material = model_language.Material(
            formula=material.chemical_structure,
            mass_density=Value(float(material.density.value), 'g/cm^3'),
            # A manual SLD is written too; it wins over the formula on reload.
            sld=None if material.sld_coupled else sld,
        )

    magnetism = layer.magnetism
    if magnetism is None:
        return orso_material
    rho_m = float(magnetism.rho_m.value)
    if not isinstance(material, MaterialDensity) or material.number_density <= 0:
        if rho_m != 0.0:
            warnings.warn(
                f'Magnetic SLD of layer "{layer.name}" not written: the ORSO model language stores '
                'moments per formula unit, and its material has no density to convert with.',
                UserWarning,
                stacklevel=3,
            )
        return orso_material
    if layer.rho_m_coupled:
        moment = float(material.magnetic_moment.value)
    else:
        moment = rho_m / (material.number_density * MAGNETIC_SCATTERING_LENGTH * 1e6)
    orso_material.magnetic_moment = Value(moment, 'muB')
    if not math.isclose(math.cos(math.radians(magnetism.theta_m.value - 270.0)), 1.0, abs_tol=1e-9):
        warnings.warn(
            f'Moment direction of layer "{layer.name}" not written (theta_m = {magnetism.theta_m.value}); '
            'the ORSO model language has none, and it reloads aligned with an in-plane field.',
            UserWarning,
            stacklevel=3,
        )
    return orso_material


def sample_to_orso_model(sample: Sample) -> model_language.SampleModel:
    """Convert an ERL Sample into an ORSO simple-model ``SampleModel`` (slab model).

    Lengths are written in angstrom (declared via ``globals.length_unit``), SLDs
    in 1/angstrom^2.  :class:`RepeatingMultilayer` assemblies are written with
    the inline repetition syntax ``N ( layer1 | layer2 )``.

    Parameters
    ----------
    sample : Sample
        The sample to convert.

    Returns
    -------
    model_language.SampleModel
        The ORSO model-language representation.
    """
    layers = {}
    stack_parts = []

    def add_layer(erl_layer) -> str:
        key = _unique_model_key(layers, erl_layer.name or erl_layer.material.name)
        layers[key] = model_language.Layer(
            thickness=Value(float(erl_layer.thickness.value), 'angstrom'),
            roughness=Value(float(erl_layer.roughness.value), 'angstrom'),
            material=_layer_material_to_orso(erl_layer),
        )
        return key

    for assembly in sample:
        keys = [add_layer(erl_layer) for erl_layer in assembly.layers]
        if isinstance(assembly, RepeatingMultilayer) and int(assembly.repetitions.value) > 1:
            stack_parts.append(f'{int(assembly.repetitions.value)} ( ' + ' | '.join(keys) + ' )')
        else:
            stack_parts.extend(keys)

    return model_language.SampleModel(
        stack=' | '.join(stack_parts),
        layers=layers,
        globals=model_language.ModelParameters(length_unit='angstrom', sld_unit='1/angstrom^2'),
    )


_STANDARD_COLUMNS = [
    Column(name='Qz', unit='1/angstrom', physical_quantity='wavevector transfer'),
    Column(name='R', physical_quantity='reflectivity'),
    ErrorColumn(error_of='R', error_type='uncertainty', value_is='sigma'),
    ErrorColumn(error_of='Qz', error_type='resolution', value_is='sigma'),
]


def _orso_header_for_dataset(dataset: DataSet1D, model=None) -> Orso:
    """Build an Orso header for one dataset, reusing a preserved header when present.

    A header captured at load time (``dataset.orso_header``) keeps
    ``data_source``/``reduction`` provenance; otherwise a minimal header is
    synthesized.  Columns are always (re)set to the standard four with the
    sigma convention, matching the exported data.
    """
    import copy as _copy

    header_dict = getattr(dataset, 'orso_header', None)
    if header_dict:
        try:
            info = Orso.from_dict(_copy.deepcopy(dict(header_dict)))
        except Exception:
            info = Orso.empty()
    else:
        info = Orso.empty()
    info.columns = _copy.deepcopy(_STANDARD_COLUMNS)
    if model is not None and getattr(model, 'sample', None) is not None:
        info.data_source.sample.model = sample_to_orso_model(model.sample)
        if info.data_source.sample.name is None:
            info.data_source.sample.name = model.sample.name
    return info


def _dataset_to_data_array(dataset: DataSet1D) -> np.ndarray:
    """Assemble the Qz/R/sR/sQz array for export.

    ``DataSet1D`` stores **variances** in ``ye``/``xe``; ORSO columns are sigma,
    so the square root is taken here.  Absent errors are written as nan
    (the spec's "unknown" marker), never as zeros.
    """
    x = np.asarray(dataset.x, dtype=float)
    y = np.asarray(dataset.y, dtype=float)

    def sigma_column(variances) -> np.ndarray:
        if variances is None:
            return np.full_like(x, np.nan)
        variances = np.asarray(variances, dtype=float)
        if variances.size != x.size or not np.any(np.nan_to_num(variances) > 0):
            return np.full_like(x, np.nan)
        return np.sqrt(variances)

    return np.column_stack([x, y, sigma_column(dataset.ye), sigma_column(dataset.xe)])


def orso_datasets_from_experiment(experiment, model=None) -> List[OrsoDataset]:
    """Convert an experiment into a list of ``OrsoDataset`` objects.

    A plain :class:`DataSet1D` becomes one dataset.  A ``PolarizedDataSet``
    becomes one dataset per spin channel in a single multi-dataset file --
    the format's intended packing for spin states -- with ``data_set`` labels
    and per-dataset ``instrument_settings.polarization`` set to the channel.

    Parameters
    ----------
    experiment :
        A DataSet1D or PolarizedDataSet.
    model : optional
        The model whose sample is written into ``sample.model``. Defaults to
        ``experiment.model``.

    Returns
    -------
    List[OrsoDataset]
        The datasets ready for ``save_orso``/``save_nexus``.
    """
    from orsopy.fileio.data_source import InstrumentSettings
    from orsopy.fileio.data_source import Polarization

    from easyreflectometry.data.polarized import PolarizedDataSet

    if model is None:
        model = getattr(experiment, 'model', None)

    datasets = []
    if isinstance(experiment, PolarizedDataSet):
        for channel, channel_dataset in experiment.channels.items():
            info = _orso_header_for_dataset(channel_dataset, model)
            info.data_set = channel.value
            measurement = info.data_source.measurement
            if measurement.instrument_settings is None:
                measurement.instrument_settings = InstrumentSettings(incident_angle=None, wavelength=None)
            measurement.instrument_settings.polarization = Polarization(channel.value)
            datasets.append(OrsoDataset(info=info, data=_dataset_to_data_array(channel_dataset)))
    else:
        info = _orso_header_for_dataset(experiment, model)
        if info.data_set is None:
            info.data_set = 0
        datasets.append(OrsoDataset(info=info, data=_dataset_to_data_array(experiment)))
    return datasets


def save_orso_experiment(experiment, fname: str, model=None) -> None:
    """Write an experiment to an ORSO file (`.ort` text, or `.orb` binary).

    Parameters
    ----------
    experiment :
        A DataSet1D or PolarizedDataSet (the latter is written as one file with
        one ``data_set`` block per spin channel).
    fname : str
        Destination path; a ``.orb`` extension selects the binary (NeXus/HDF5)
        representation, anything else the text one.
    model : optional
        The model whose sample is exported as the ORSO ``sample.model``.
        Defaults to the experiment's model.
    """
    fname = str(fname)
    datasets = orso_datasets_from_experiment(experiment, model=model)
    if fname.lower().endswith('.orb'):
        orso.save_nexus(datasets, fname)
    else:
        orso.save_orso(datasets, fname)
