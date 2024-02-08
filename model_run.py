from EasyReflectometry.calculators import CalculatorFactory
from EasyReflectometry.experiment.model import Model
from EasyReflectometry.sample.items import RepeatingMultiLayer
from EasyReflectometry.sample.layer import Layer
from EasyReflectometry.sample.layers import Layers
from EasyReflectometry.sample.material import Material
from EasyReflectometry.sample.structure import Structure

interface = CalculatorFactory()
m1 = Material.from_pars(6.908, -0.278, 'Boron')
m2 = Material.from_pars(0.487, 0.000, 'Potassium')
l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
o1 = RepeatingMultiLayer.from_pars(ls1, 2.0, 'twoLayerItem1')
o2 = RepeatingMultiLayer.from_pars(ls2, 1.0, 'oneLayerItem2')
d = Structure.from_pars(o1, name='myModel')
mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
print('hello')
