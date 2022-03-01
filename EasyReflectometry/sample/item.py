"""The :py:mod:`item` library is the backbone of :py:mod:`EasyReflectometry`.
An :py:mod:`EasyReflectometry.sample.item` allows for the inclusion of physical and 
chemical parameterisation into our reflectometry model.  
For more information please look at the `item library documentation`_

.. _`item library documentation`: ./library.html
"""

__author__ = 'github.com/arm61'

from copy import deepcopy
from typing import Union, List

import yaml
import periodictable as pt
from easyCore import np
from easyCore.Fitting.Constraints import ObjConstraint
from easyCore.Objects.ObjectClasses import Parameter, BaseObj

from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.layer import Layer, LayerApm, LAYERAPM_DETAILS
from EasyReflectometry.sample.layers import Layers

REPEATINGMULTILAYER_DETAILS = {
    'repetitions': {
        'description': 'Number of repetitions of the given series of layers',
        'value': 1,
        'min': 1,
        'max': 9999,
        'fixed': True
    }
}


class MultiLayer(BaseObj):
    """
    A :py:class:`MultiLayer` consists of a series of 
    :py:class:`EasyReflectometry.sample.layer.Layer` or 
    :py:class:`EasyReflectometry.sample.layers.Layers`. 
    This :py:mod:`item` will arrange the layers as slabs, one on top of another, 
    allowing the reflectometry to be determined from them. 
    
    More information about the usage of this item is available in the `item library documentation`_

    .. _`item library documentation`: ./item_library.html#multilayer
    """

    def __init__(self,
                 layers: Union[Layers, Layer, List[Layer]],
                 name: str = 'EasyMultiLayer',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = Layers(*layers, name='/'.join([layer.name for layer in layers]))
        self.type = 'Multi-layer'
        super().__init__(name, layers=layers)
        self.interface = interface

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "MultiLayer":
        """
        Default constructor for a multi-layer item.

        :return: MultiLayer container
        :rtype: MultiLayer
        """
        layers = Layers.default()
        return cls(layers, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  name: str = "EasyMultiLayer",
                  interface=None) -> "MultiLayer":
        """
        Constructor of a multi-layer item where the parameters are known.

        :param layers: The layers in the multi-layer
        :type layers: EasyReflectometry.layers.Layers
        :return: MultiLayer container
        :rtype: MultiLayer
        """
        return cls(layers=layers, name=name, interface=interface)

    def add_layer(self, *layers):
        """
        Add a layer to the item.

        :param *layers: Layers to add to item
        :type layers: Layer
        """
        for arg in layers:
            if issubclass(arg.__class__, Layer):
                self.layers.append(arg)
                if self.interface is not None:
                    self.interface().add_layer_to_item(arg.uid, self.uid)

    def duplicate_layer(self, idx):
        """
        Duplicate a given layer.

        :param idx: index of layer to duplicate
        :type idx: int
        """
        to_duplicate = self.layers[idx]
        duplicate_layer = Layer.from_pars(material=to_duplicate.material,
                                          thickness=to_duplicate.thickness.raw_value,
                                          roughness=to_duplicate.roughness.raw_value,
                                          name=to_duplicate.name + ' duplicate')
        self.add_layer(duplicate_layer)

    def remove_layer(self, idx):
        """
        Remove a layer from the item.

        :param idx: index of layer to remove
        :type idx: int
        """
        if self.interface is not None:
            self.interface().remove_layer_from_item(self.layers[idx].uid, self.uid)
        del self.layers[idx]

    @property
    def uid(self):
        """
        Return a UID from the borg map
        """
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        if len(self.layers) == 1:
            return self.layers[0]._dict_repr
        return {self.name: self.layers._dict_repr}

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        :rtype: str
        """
        return yaml.dump(self._dict_repr, sort_keys=False)


class RepeatingMultiLayer(MultiLayer):
    """
    A :py:class:`RepeatingMultiLayer` takes a :py:class:`MultiLayer` and repeats
    it a some number of times. This enables a computational efficiency in many 
    reflectometry engines as the operation can be performed for a single 
    :py:class:`MultiLayer` and cheaply combined for the appropriate number of 
    :py:attr:`repetitions`. 

    More information about the usage of this item is available in the `item library documentation`_

    .. _`item library documentation`: ./item_library.html#repeatingmultilayer
    """

    def __init__(self,
                 layers: Union[Layers, Layer, List[Layer]],
                 repetitions: Parameter,
                 name: str = 'EasyRepeatingMultiLayer',
                 interface=None):
        if isinstance(layers, Layer):
            layers = Layers(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = Layers(*layers, name='/'.join([layer.name for layer in layers]))
        super().__init__(layers, name, interface)
        self._add_component("repetitions", repetitions)
        self.interface = interface
        self.type = 'Repeating Multi-layer'

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "RepeatingMultiLayer":
        """
        Default constructor for the reflectometry repeating multi layer. 

        :return: Default repeating multi-layer container
        """
        layers = Layers.default()
        repetitions = Parameter('repetitions',
                                **REPEATINGMULTILAYER_DETAILS['repetitions'])
        return cls(layers, repetitions, interface=interface)

    @classmethod
    def from_pars(cls,
                  layers: Layers,
                  repetitions: float = 1.0,
                  name: str = 'EasyRepeatingMultiLayer',
                  interface=None) -> "RepeatingMultiLayer":
        """
        Constructor of a reflectometry repeating multi layer where the parameters are known.

        :param layers: The layers in the repeating multi layer
        :param repetitions: Number of repetitions, defaults to :py:attr`1`. 
        :return: Repeating multi-layer container
        """
        default_options = deepcopy(REPEATINGMULTILAYER_DETAILS)
        del default_options['repetitions']['value']

        repetitions = Parameter('repetitions', repetitions,
                                **default_options['repetitions'])

        return cls(layers=layers,
                   repetitions=repetitions,
                   name=name,
                   interface=interface)

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
        d_dict = {self.name: self.layers._dict_repr}
        d_dict[self.name]['repetitions'] = self.repetitions.raw_value
        return d_dict

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        """
        return yaml.dump(self._dict_repr, sort_keys=False)


class SurfactantLayer(MultiLayer):
    """
    A :py:class:`SurfactantLayer` constructs a series of layers representing the head and tail 
    groups of a surfactant. This item allows the definition of a surfactant or lipid using the 
    chemistry of the head and tail regions, additionally this approach will make the application of 
    constraints such as conformal roughness or area per molecule more straight forward.

    More information about the usage of this item is available in the `item library documentation`_

    .. _`item library documentation`: ./item_library.html#surfactantlayer 
    """

    def __init__(self,
                 head: LayerApm,
                 tail: LayerApm,
                 flip: bool = False,
                 name: str = 'EasySurfactantLayer',
                 interface=None):
        """
        :param head: Head layer object
        :param tail: Tail layer object
        :param flip: Should the surfactant layer be flipped over
        :param name: Name for surfactant layer 
        """
        surfactant = Layers(tail, head, name=name)
        if flip:
            surfactant = Layers(head, tail, name=name)
        super().__init__(surfactant, name, interface)
        self._add_component('head', head)
        self._add_component('tail', tail)
        default_options = deepcopy(LAYERAPM_DETAILS)

        del default_options['area_per_molecule']['value']
        area_per_molecule = Parameter('area_per_molecule',
                                      head.area_per_molecule.raw_value,
                                      **default_options['area_per_molecule'])
        self._add_component('area_per_molecule', area_per_molecule)
        apm1 = ObjConstraint(head.area_per_molecule, '', area_per_molecule)
        apm2 = ObjConstraint(tail.area_per_molecule, '', area_per_molecule)
        area_per_molecule.user_constraints['head_apm'] = apm1
        area_per_molecule.user_constraints['tail_apm'] = apm2

        del default_options['roughness']['value']
        roughness = Parameter('roughness', head.roughness.raw_value,
                              **default_options['roughness'])
        self._add_component('roughness', roughness)
        rough1 = ObjConstraint(head.roughness, '', roughness)
        rough2 = ObjConstraint(tail.roughness, '', roughness)
        roughness.user_constraints['head_rough'] = rough1
        roughness.user_constraints['tail_rough'] = rough2

        self.flip = flip
        self.interface = interface
        self.type = "Surfactant Layer"

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> "SurfactantLayer":
        """
        Default constructor for a surfactant layer object. The default lipid type is DPPC.

        :return: Surfactant layer object.
        """
        d2o = Material.from_pars(6.36, 0, 'D2O')
        air = Material.from_pars(0, 0, 'Air')
        head = LayerApm.from_pars('C10H18NO8P', 10., d2o, 0.2, 48.2, 3.0, 'DPPC Head')
        tail = LayerApm.from_pars('C32D64', 16, air, 0., 48.2, 3, 'DPPC Tail')
        return cls(head, tail, flip=False, name='DPPC', interface=interface)

    @classmethod
    def from_pars(cls,
                  head_chemical_structure: str,
                  head_thickness: float,
                  head_solvent: Material,
                  head_solvation: float,
                  head_area_per_molecule: float,
                  head_roughness: float,
                  tail_chemical_structure: str,
                  tail_thickness: float,
                  tail_solvent: Material,
                  tail_solvation: float,
                  tail_area_per_molecule: float,
                  tail_roughness: float,
                  flip: bool = False,
                  name: str = 'EasySurfactantLayer',
                  interface=None) -> "SurfactantLayer":
        """
        Constructor for the surfactant layer where the parameters are known.
    
        :param head_chemical_structure: Chemical formula for surfactant head
        :param head_thickness: Thicknkess of head group
        :param head_solvent: Solvent in head group
        :param head_solvation: Fractional solvation of head group by :py:attr:`head_solvent`
        :param head_area_per_molecule: Area per molecule of head group
        :param head_roughness: Roughness of head group layer
        :param tail_chemical_structure: Chemical formula for surfactant tail
        :param tail_thickness: Thicknkess of tail group
        :param tail_solvent: Solvent in tail group
        :param tail_solvation: Fractional solvation of tail group by :py:attr:`tail_solvent`
        :param tail_area_per_molecule: Area per molecule of tail group
        :param tail_roughness: Roughness of tail group layer
        :param flip: Should the surfactant layer be flipped over
        :param name: Name for surfactant layer 
        """
        head = LayerApm.from_pars(head_chemical_structure,
                                  head_thickness,
                                  head_solvent,
                                  head_solvation,
                                  head_area_per_molecule,
                                  head_roughness,
                                  name=name + ' Head')
        tail = LayerApm.from_pars(tail_chemical_structure,
                                  tail_thickness,
                                  tail_solvent,
                                  tail_solvation,
                                  tail_area_per_molecule,
                                  tail_roughness,
                                  name=name + ' Tail')
        return cls(head, tail, flip, name, interface)

    @property
    def constrain_apm(self) -> bool:
        """
        :return: if the area per molecule is constrained
        """
        return (self.area_per_molecule.user_constraints['head_apm'].enabled
                and self.area_per_molecule.user_constraints['tail_apm'].enabled)

    @constrain_apm.setter
    def constrain_apm(self, x: bool):
        """
        Set the constraint such that the head and tail layers have the same area per molecule. 

        :param x: Boolean description the presence of the constraint.
        """
        self.area_per_molecule.user_constraints['head_apm'].enabled = x
        self.area_per_molecule.user_constraints['tail_apm'].enabled = x
        self.head.area_per_molecule.enabled = not x
        self.tail.area_per_molecule.enabled = not x

    @property
    def conformal_roughness(self) -> bool:
        """
        :return: is the roughness is the same for both layers.
        """
        return (self.roughness.user_constraints['head_rough'].enabled
                and self.roughness.user_constraints['tail_rough'].enabled)

    @conformal_roughness.setter
    def conformal_roughness(self, x: bool):
        """
        Set the roughness to be the same for both layers.
        """
        self.roughness.user_constraints['head_rough'].enabled = x
        self.roughness.user_constraints['tail_rough'].enabled = x

    def constrain_solvent_roughness(self, solvent_roughness: Parameter):
        """
        Add the constraint to the solvent roughness. 

        :param solvent_roughness: The solvent roughness parameter.

        """
        rough = ObjConstraint(solvent_roughness, '', self.roughness)
        self.roughness.user_constraints['solvent_roughness'] = rough

    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation. 
        
        :return: Simple dictionary
        """
        if self.flip:
            return {
                'head': self.layers[0]._dict_repr,
                'tail': self.layers[1]._dict_repr,
                'area per molecule constrained': self.constrain_apm,
                'conformal roughness': self.conformal_roughness
            }
        return {
            'head': self.layers[1]._dict_repr,
            'tail': self.layers[0]._dict_repr,
            'area per molecule constrained': self.constrain_apm,
            'conformal roughness': self.conformal_roughness
        }

    def __repr__(self) -> str:
        """
        String representation of the layer.

        :return: a string representation of the layer
        """
        return yaml.dump(self._dict_repr, sort_keys=False)
