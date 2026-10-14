---
icon: material/magnet
---

# :material-magnet: Magnetism

A magnetic layer adds a spin-dependent part to the scattering length
density (SLD). Polarised neutron reflectometry measures it in up to four
spin channels: `pp`, `mm` (non-spin-flip) and `pm`, `mp` (spin-flip).
This page states the conventions EasyReflectometry uses, the two ways to
give a layer a magnetic SLD, how fitting and ORSO files treat them, and
what is not modelled. The
[Magnetism Simulation](../tutorials/simulation/magnetism.ipynb) and
[Polarized Fitting](../tutorials/advancedfitting/polarized_fitting.ipynb)
notebooks show the code in use.

Only the Refl1D calculator models magnetism; refnx refuses a magnetic
layer.

## The slab picture

Each layer has a nuclear SLD $\rho$ and, when it is magnetic, a magnetic
SLD $\rho_M$ with an in-plane direction $\theta_M$. Both live on a
`LayerMagnetism` attached to the layer:

```python
from easyreflectometry.sample import Layer, LayerMagnetism

film = Layer(material=iron, thickness=100, magnetism=LayerMagnetism(rho_m=5.0, theta_m=270))
```

As a rule of thumb, the non-spin-flip channels see the component of the
moment along the field and the spin-flip channels the component across
it. That is a reading of the physics, not an exact split of the
reflectivity: the calculator always solves the full spin-dependent
problem, and that is what is fitted.

## Angles and the field

`theta_m` is the angle of the moment in the sample plane, in degrees,
measured as Refl1D measures it. The field is set per model:

- `Model.guide_field_angle` is the angle of the field about the beam
  axis (Refl1D's `Aguide`). It is 270 by default.
- `Model.applied_field` is the field strength in tesla (Refl1D's `H`).
  It is 0 by default. It adds a Zeeman term along the field direction,
  so its effect depends on the field and on its orientation relative to
  the moments.

| `guide_field_angle` | Field direction                |
| ------------------- | ------------------------------ |
| 270 or −90          | in the sample plane            |
| 90                  | in the sample plane, reversed  |
| 0 or 180            | along the surface normal       |
| anything else       | tilted out of the sample plane |

With an in-plane field at 270, `theta_m = 270` puts the moment along the
field and gives no spin-flip scattering. `theta_m = 90` is the reversed
moment, and 0 or 180 is fully transverse.

Both field parameters are fixed by default and can be fitted. A derived
contrast keeps them. They are disabled, and so not offered for fitting,
when the model is not magnetic or the calculator cannot model magnetism.
The ORSO model language has no field, so they are not written to ORSO
files.

## The depth profiles

`Project.magnetic_sld_data_for_model_at_index` returns the profiles
versus depth: the nuclear SLD, $\rho_M$, $\theta_M$, the magnitude of
$\rho_M$ across the field, and two curves $\rho \pm \rho_{M\parallel}$.
The last two are the nuclear SLD plus or minus the part of the magnetic
SLD along the field.

Those two curves are the potentials the two spin states see **only when
every moment is parallel to the field and the applied field is zero**.
With a moment across the field the two spin states mix, and their
potentials split by $\pm|\rho_M|$ whatever the field direction. For
example, a moment fully across the field gives two identical curves, yet
the critical edges still move. The applied field is not included in the
curves.

## Two ways to set the magnetic SLD

**Directly**, by setting `LayerMagnetism.rho_m` in units of $10^{-6}$
Å⁻², like any other SLD.

**From a moment**, with a `MaterialMagnetic` and a layer coupled to it:

```python
from easyreflectometry.sample import Layer, MaterialMagnetic

iron = MaterialMagnetic(chemical_structure='Fe', density=7.874, magnetic_moment=2.2)
film = Layer(material=iron, thickness=100, rho_m_coupled=True)
film.magnetism.rho_m.value  # 5.042, i.e. 5.042e-6 1/Å^2
```

`MaterialMagnetic` is a `MaterialDensity` with a `magnetic_moment` in
Bohr magnetons **per formula unit**. That is the moment per atom only
for a one-element formula. Its magnetic SLD is derived:

$$
\rho_M = N \mu p, \qquad N = \frac{N_A d}{M}, \qquad
p = \frac{m_n |\mu_n| \mu_0 \mu_B}{2\pi\hbar^2} = 2.6991 \times 10^{-5}\ \text{Å}
$$

Here $N$ is the number of formula units per volume and $p$ is the
magnetic scattering length of one Bohr magneton.
`MaterialDensity.number_density` gives $N$ in Å⁻³. It is read-only:
density is the parameter, and
`easyreflectometry.special.calculations.mass_density_from_number_density`
converts a known $N$ into a density.

orsopy's SLD database uses a value of $p$ about 2 % lower. The often
quoted $\gamma r_0 / 2 = 2.6955 \times 10^{-5}$ Å drops the factor
$m_n/m_p$.

The moment is the **effective in-plane net moment** per formula unit. It
is not the atomic or saturation moment: a moment canted out of the plane
appears smaller, and an antiferromagnet has no net moment.

`Layer.rho_m_coupled` makes the layer's `rho_m` follow the material's.
The layer keeps its own `theta_m`, so two layers of one material can
point in different directions. Coupling is opt-in because the same
chemistry can carry different net moments in different layers. The
coupling is dropped when:

- the layer gets a material without a moment, with a warning;
- its magnetism is removed;
- `rho_m` is unconstrained by hand;
- `rho_m_coupled` is set to `False`.

When the coupling is dropped, `rho_m` keeps its value and becomes an
ordinary fixed parameter again.

Switching off `sld_coupled` on a `MaterialMagnetic` frees the nuclear
SLD only. The magnetic SLD stays derived from density and moment.

## Fitting

- Fit `magnetic_moment` or `rho_m`, not both: one derives the other in a
  coupled layer.
- When the nuclear SLD is decoupled, the data only constrain density ×
  moment, so free one of the two, not both.
- A material's moment has no effect unless some layer is coupled to it.
- A moment $\mu$ at $\theta_M$ and $-\mu$ at $\theta_M + 180°$ are the
  same state. `magnetic_moment` is non-negative by default, and the
  direction is `theta_m`. A layer's `rho_m` stays signed.

## ORSO model files

The ORSO model language describes a material by formula, density and
`magnetic_moment` (µB per formula unit). It has no magnetic direction
and no field.

On import:

- A formula with a mass or number density and a moment becomes a
  `MaterialMagnetic`. Its layer is coupled to it with `theta_m = 270`.
- An explicit SLD next to them overrides the formula's nuclear SLD.
- A moment with an SLD and a number density but no formula becomes a
  direct `rho_m`.
- A moment that cannot be converted, because there is no density or the
  unit is unknown, is skipped with a warning.
- An explicitly unknown unit is never read as the default unit.
- `relative_density` is not applied, and the importer warns about it.

On export:

- A magnetic layer on a density-defined material is written with the
  moment that reproduces its `rho_m`.
- A magnetic SLD on a material without a density cannot be written, and
  the exporter warns.
- A direction other than `theta_m = 270` is lost, with a warning.
- A manually set nuclear SLD is written next to the formula, so it
  survives a reload.

## Not modelled

- **Out-of-plane moments.** The slab model has no out-of-plane moment
  angle. A moment canted out of the plane fits as a smaller in-plane
  moment. This matters most when the field is tilted out of the plane: a
  fitted moment is then only its in-plane projection.
- **Magnetic roughness and dead layers.** The magnetic profile shares
  the nuclear roughness. Use extra layers for a dead layer.
- **Polarisation efficiency.** The four channels are ideal
  cross-sections. There is no correction for beam polarisation or
  flipper efficiency, and the alignment offset `theta_offset` is fixed
  at 0.
- **Domains and off-specular scattering.** Neither domain averaging nor
  off-specular scattering is modelled.
- **Repeating multilayers.** Refl1D cannot calculate magnetism inside a
  `RepeatingMultilayer`, and it raises an error.
- **Other magnetic materials.** `MaterialMixture`, `MaterialSolvated`
  and `LayerAreaPerMolecule` have no moment. Use a direct `rho_m` on
  their layers.
