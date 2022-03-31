__author__ = 'github.com/arm61'

from typing import ClassVar, Tuple
from copy import deepcopy

import yaml
from easyCore import np
from easyCore.Objects.ObjectClasses import Parameter, BaseObj
from easyCore.Fitting.Constraints import FunctionalConstraint

from EasyReflectometry.sample.material import Material, MaterialMixture, MATERIAL_DEFAULTS
from EasyReflectometry.special.calculations import neutron_scattering_length, apm_to_sld

LAYER_DETAILS = {
    'thickness': {
        'description': 'The thickness of the layer in angstroms',
        'url':
        'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 10.0,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    },
    'roughness': {
        'description':
        'The interfacial roughness, Nevot-Croce, for the layer in angstroms.',
        'url': 'https://doi.org/10.1051/rphysap:01980001503076100',
        'value': 3.3,
        'units': 'angstrom',
        'min': 0.0,
        'max': np.Inf,
        'fixed': True
    }
}

LAYERAPM_DETAILS = {
    'thickness': {
        'description': 'The thickness of the layer in angstroms',
        'value': 10.0,
        'units': 'angstrom',
        'min': 0,
        'max': np.inf,
        'fixed': True
    },
    'chemical_structure': 'C10H18NO8P',
    'roughness': {
        'description': 'Conformal roughness',
        'value': 3.0,
        'units': 'angstrom',
        'min': 0,
        'max': np.inf,
        'fixed': True
    },
    'area_per_molecule': {
        'description': 'Surface coverage',
        'value': 48.2,
        'units': 'angstrom ** 2',
        'min': 0,
        'max': np.inf,
        'fixed': True
    },
    'solvation': {
        'description': 'Fraction of solvent present',
        'value': 0.2,
        'units': 'dimensionless',
        'min': 0,
        'max': 1,
        'fixed': True
    },
    'sl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 4.186,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    },
    'isl': {
        'description': 'The real scattering length for a chemical formula in angstrom.',
        'url': 'https://www.ncnr.nist.gov/resources/activation/',
        'value': 0.0,
        'units': 'angstrom',
        'min': -np.Inf,
        'max': np.Inf,
        'fixed': True
    }
}


class Layer(BaseObj):

    def __init__(self,
                 material: Material,
                 thickness: Parameter,
                 roughness: Parameter,
                 name: str = 'EasyLayer',
                 interface=None):
        super().__init__(name,
                         material=material,
                         thickness=thickness,
                         roughness=roughness)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "Layer":
        """
        Default constructor for the reflectometry layer. 

        :return: Default layer container
        :rtype: Layer
        """
        material = Material.default()
        thickness = Parameter('thickness', **LAYER_DETAILS['thickness'])
        roughness = Parameter('roughness', **LAYER_DETAILS['roughness'])
        return cls(material, thickness, roughness, interface=interface)

    @classmethod
    def from_pars(cls,
                  material: Material,
                  thickness: float,
                  roughness: float,
                  name: str = 'EasyLayer',
                  interface=None) -> "Layer":
        """
        Constructor of a reflectometry layer where the parameters are known.

        :param material: The material that makes up the layer
        :type material: EasyReflectometry.material.Material
        :param thickness: Layer thickness in angstrom
        :type thickness: float
        :param roughness: Layer roughness in angstrom
        :type roughness: float
        :return: Layer container
        :rtype: Layer
        """
        default_options = deepcopy(LAYER_DETAILS)
        del default_options['thickness']['value']
        del default_options['roughness']['value']

        thickness = Parameter('thickness', thickness, **default_options['thickness'])
        roughness = Parameter('roughness', roughness, **default_options['roughness'])

        return cls(material=material,
                   thickness=thickness,
                   roughness=roughness,
                   name=name,
                   interface=interface)

    def assign_material(self, material):
        """
        Assign a material to the layer interface
        """
        self.material = material
        if self.interface is not None:
            self.interface().assign_material_to_layer(self.material.uid, self.uid)

    @property
    def uid(self) -> int:
        """
        :return: UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        return {
            self.name: {
                'material': self.material._dict_repr,
                'thickness': f'{self.thickness.raw_value:.3f} {self.thickness.unit}',
                'roughness': f'{self.roughness.raw_value:.3f} {self.roughness.unit}'
            }
        }

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return yaml.dump(self._dict_repr, sort_keys=False)


class LayerApm(Layer):
    """
    The :py:class:`LayerApm` class allows a layer to be defined in terms of some chemical 
    structure (given as a chemical formula) and area per molecule. 

    """
    area_per_molecule: ClassVar[
        Parameter]  #= ('area_per_molecule', LAYERAPM_DETAILS['area_per_molecule'])
    _solvent: ClassVar[Material]
    solvation: ClassVar[Parameter]

    def __init__(self,
                 chemical_structure: str,
                 thickness: Parameter,
                 solvent: Material,
                 solvation: Parameter,
                 area_per_molecule: Parameter,
                 roughness: Parameter,
                 name: str = 'EasyLayerApm',
                 interface=None):
        """
        :param chemical_structure: Chemical formula for the material in the layer
        :param thickness: Layer thickness
        :param solvent: Solvent present in material
        :param solvation: Fraction of solvent present
        :param area_per_molecule: Area per molecule for the chemical material
        :param roughness: Upper roughness on the layer
        :param name: Identifier, defaults to :py:attr:`EasyLayerApm`
        :param interface: Interface object, defaults to :py:attr:`None`
        """
        scattering_length = neutron_scattering_length(chemical_structure)  #* 1e6
        default_options = deepcopy(LAYERAPM_DETAILS)
        del default_options['sl']['value']
        del default_options['isl']['value']
        scattering_length_real = Parameter('scattering_length_real',
                                           scattering_length.real,
                                           **default_options['sl'])
        scattering_length_imag = Parameter('scattering_length_imag',
                                           scattering_length.imag,
                                           **default_options['isl'])
        sld = apm_to_sld(scattering_length_real.raw_value, thickness.raw_value,
                         area_per_molecule.raw_value)
        isld = apm_to_sld(scattering_length_imag.raw_value, thickness.raw_value,
                          area_per_molecule.raw_value)

        material = Material.from_pars(sld,
                                      isld,
                                      name=chemical_structure,
                                      interface=interface)

        constraint = FunctionalConstraint(
            material.sld, apm_to_sld,
            [scattering_length_real, thickness, area_per_molecule])
        thickness.user_constraints['apm'] = constraint
        area_per_molecule.user_constraints['apm'] = constraint
        scattering_length_real.user_constraints['apm'] = constraint

        iconstraint = FunctionalConstraint(
            material.isld, apm_to_sld,
            [scattering_length_imag, thickness, area_per_molecule])
        thickness.user_constraints['iapm'] = iconstraint
        area_per_molecule.user_constraints['iapm'] = iconstraint
        scattering_length_imag.user_constraints['iapm'] = iconstraint

        solvated_material = MaterialMixture(material,
                                            solvent,
                                            solvation,
                                            name=chemical_structure + '/' + solvent.name,
                                            interface=interface)
        super().__init__(material=solvated_material,
                         thickness=thickness,
                         roughness=roughness,
                         name=name,
                         interface=interface)
        self._add_component('scattering_length_real', scattering_length_real)
        self._add_component('scattering_length_imag', scattering_length_imag)
        self._add_component('area_per_molecule', area_per_molecule)
        self._add_component('roughness', roughness)
        self._chemical_structure = chemical_structure
        self.interface = interface

    @property
    def solvent(self) -> Material:
        """
        :return: Solvent material
        """
        return self.material.material_b

    @solvent.setter
    def solvent(self, new_solvent):
        """
        :param new_solvent: New solvent material.
        """
        self.material.material_b = new_solvent

    @property
    def solvation(self) -> Parameter:
        """
        :return: Solvation fraction.
        """
        return self.material.fraction

    @solvation.setter
    def solvation(self, fraction: float):
        """
        :param fraction: Fraction of solvent.
        """
        self.material.fraction = fraction

    #Class constructors
    @classmethod
    def default(cls, interface=None) -> "LayerApm":
        """
        Default constructor for layer defined from chemical structure and area per molecule.

        :param interface: Interface object, defaults to :py:attr:`None`
        :return: Layer with correct structure
        """
        area_per_molecule = Parameter('area_per_molecule',
                                      **LAYERAPM_DETAILS['area_per_molecule'])
        thickness = Parameter('thickness', **LAYERAPM_DETAILS['thickness'])
        roughness = Parameter('roughness', **LAYERAPM_DETAILS['roughness'])
        solvent = Material.from_pars(6.36, 0, 'D2O', interface=interface)
        solvation = Parameter('solvation', **LAYERAPM_DETAILS['solvation'])
        return cls(LAYERAPM_DETAILS['chemical_structure'],
                   thickness,
                   solvent,
                   solvation,
                   area_per_molecule,
                   roughness,
                   interface=interface)

    @classmethod
    def from_pars(cls,
                  chemical_structure: str,
                  thickness: float,
                  solvent: Material,
                  solvation: float,
                  area_per_molecule: float,
                  roughness: float,
                  name: str = 'EasyLayerApm',
                  interface=None) -> "LayerApm":
        """
        Constructor for a layer described with the area per molecule, where the parameters are known.
        
        :param chemical_structure: Chemical formula for the material in the layer
        :param thickness: Layer thickness
        :param solvent: Solvent present in material
        :param solvation: Fraction of solvent present
        :param area_per_molecule: Area per molecule for the chemical material
        :param roughness: Upper roughness on the layer
        :param name: Identifier, defaults to :py:attr:`EasyLayerApm`
        :param interface: Interface object, defaults to :py:attr:`None`
        :return: Layer with correct structure
        """
        default_options = deepcopy(LAYERAPM_DETAILS)
        del default_options['area_per_molecule']['value']
        del default_options['thickness']['value']
        del default_options['roughness']['value']
        del default_options['solvation']['value']
        del default_options['chemical_structure']

        area_per_molecule = Parameter('area_per_molecule', area_per_molecule,
                                      **default_options['area_per_molecule'])
        thickness = Parameter('thickness', thickness, **default_options['thickness'])
        roughness = Parameter('roughness', roughness, **default_options['roughness'])
        solvation = Parameter('solvation', solvation, **default_options['solvation'])

        return cls(chemical_structure,
                   thickness,
                   solvent,
                   solvation,
                   area_per_molecule,
                   roughness,
                   name=name,
                   interface=interface)

    @property
    def chemical_structure(self) -> str:
        """
        :return: Chemical structure
        """
        return self._chemical_structure
    
    @chemical_structure.setter
    def chemical_structure(self, structure_string: str):
       """
       :param structure_string: String that defines the chemical structure.
       """ 
       self._chemical_structure = structure_string
       scattering_length = neutron_scattering_length(structure_string)
       self.scattering_length_real.value = scattering_length.real
       self.scattering_length_imag.value = scattering_length.imag
       self.material.name = structure_string

    @property
    def _dict_repr(self) -> dict:
        """
        Dictionary representation of the :py:class:`LayerApm` object. 
        
        :return: Simple dictionary
        """
        layerapm_dict = super()._dict_repr
        layerapm_dict['chemical_structure'] = self._chemical_structure
        layerapm_dict[
            'area_per_molecule'] = f'{self.area_per_molecule.raw_value:.1f} {self.area_per_molecule.unit}'
        return layerapm_dict
