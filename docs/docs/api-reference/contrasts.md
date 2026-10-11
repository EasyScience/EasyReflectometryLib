# Contrasts

A contrast is one structure measured under another SLD condition: the
same film in D2O and in H2O, or a monolayer with deuterated and
hydrogenated tails. Each contrast is an ordinary `Model`, with its own
scale, background and resolution; what the contrasts have in common is
shared in one of two ways:

- **by identity**: an assembly or material is one object used by several
  models, so it has one set of parameters;
- **by equality**: a parameter of one model follows the corresponding
  parameter of another, where the objects must differ (a hydrated layer
  whose solvent differs between contrasts).

The `Project` offers two routes to that state. **Adding a contrast**
derives a new model from a reference with `derive_contrast`: assemblies
the substitutions do not touch are shared, touched ones are copied with
every parameter tied to the reference's except those of the replacement.

```python
from easyreflectometry.contrasts import ReplaceFormula
from easyreflectometry.contrasts import ReplaceMaterial

h2o_index = project.add_contrast(0, 'Film in H2O', [ReplaceMaterial(d2o, h2o)])
h_tails = project.add_contrast(0, 'h-tails', [ReplaceFormula(tail_layer, 'C32H64')])
project.parameter_models(film_layer.thickness)  # [0, 1, 2]: one parameter of three models
```

**Linking contrasts** ties two models that exist already. Parameters
correspond by their path within the model, so the models need the same
layout: the same assemblies and layers, with materials of the same kind
(a `MaterialDensity` and a plain `Material` do not correspond);
`plan_link` raises `LayoutMismatch` otherwise. The plan changes nothing:
each `LinkRow` says what linking would do with one pair of parameters
(`'tie'`, `'skip'`, `'already_tied'`, `'conflict'`), and with the
reason. Scale and background always stay per contrast. A material's
chemistry (`CHEMISTRY`: SLD, density, scattering lengths) is
`'undecided'` until `materials='tie'` or `materials='skip'` is given,
since contrasts usually differ in it.

```python
plan = project.plan_link(follower_index, reference_index, materials='skip')
[(row.path, row.action, row.reason) for row in plan.rows]
record = project.apply_link(plan)  # ties the 'tie' rows, all or none
project.unlink(record)  # restores each follower's value and bounds from before the link
```

`apply_link` refuses a plan with undecided rows, or one the project has
outdated since it was made. `Project.detach` frees a shared parameter in
one model, which then gets its own copy of the assembly. The derivation
of each contrast, the links and the sharing are saved with the project.
See the
[contrasts tutorial](../tutorials/advancedfitting/contrasts.ipynb) for a
worked example.

::: easyreflectometry.contrasts options: members: - CHEMISTRY -
ReplaceMaterial - ReplaceFormula - derive_contrast -
substitution_candidates - UnsupportedSubstitution - plan_link -
LinkPlan - LinkRow - LinkRecord - LayoutMismatch - follows -
tie_corresponding - snapshot - restore
