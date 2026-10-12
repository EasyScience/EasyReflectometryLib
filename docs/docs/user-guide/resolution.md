---
icon: material/blur
---

# :material-blur: Resolution

The instrument smears a reflectivity curve: at every $q$ the measured
value is a weighted average of the ideal curve over neighbouring $q$,
with Gaussian weights whose width depends on the wavelength spread and
the angular divergence. EasyReflectometry describes that width with a
**resolution function**, and this page explains which resolution is used
where: by a model, by a dataset, by a fit, and by a polarised
experiment. The functions themselves are introduced in
[Creating a Model](../tutorials/basic/model.md#resolution-functions) and
the
[Resolution Functions](../tutorials/simulation/resolution_functions.ipynb)
notebook.

## The three resolution functions

| Class            | Width at $q$                                          | Typical use                                   |
| ---------------- | ----------------------------------------------------- | --------------------------------------------- |
| `PercentageFwhm` | a fixed percentage of $q$ (FWHM)                      | simulations; data without a resolution column |
| `LinearSpline`   | interpolated between given $(q, \mathrm{FWHM})$ pairs | a resolution known at a few points            |
| `Pointwise`      | one width per measured point, exact at those points   | the sQz column of a measured file             |

All three are `ResolutionFunction` objects with a `smearing(q)` method
returning the Gaussian $\sigma$ at each $q$; the calculator (refnx or
Refl1D) converts it to its own convention.

## The model's resolution

Every `Model` has a `resolution_function` (5 % FWHM by default). It is
used for

- simulations, i.e. `Project.model_data_for_model_at_index` and the
  calculator's `reflectity_profile` when no other resolution is given;
- any dataset whose own resolution is `None` (see below);
- the resolution field of the GUI.

A project has one calculator for all its models, and the calculator
keeps one resolution per model, so two contrasts with different measured
widths are each smeared with their own. Switching the calculation engine
keeps them.

```python
from easyreflectometry.model import Model, PercentageFwhm

model = Model(resolution_function=PercentageFwhm(2.0))
model.resolution_function = PercentageFwhm(1.1)  # takes effect at once
```

## A dataset's own resolution

A `DataSet1D` carries the resolution it was measured with in
`resolution_function`. Loading a file with a fourth column (`sQz`,
either as $\sigma$ or as FWHM in an ORSO header) sets a `Pointwise` on
the dataset; a two- or three-column file leaves it `None`, which means
_the model's resolution applies_.

```python
from easyreflectometry.data import load_as_dataset, resolution_from_dataset

dataset = load_as_dataset('film.ort')
dataset.resolution_function          # Pointwise, or None
resolution_from_dataset(dataset)     # the same, built from xe
dataset.resolution_function = None   # fall back to the model's
```

A fit smears each dataset with its own resolution. Several datasets of
one model (different angles, contrasts measured with another slit
setting, spin channels) are each compared to the model smeared with the
width they were measured with. The curve a dataset is compared to is
available as

```python
project.model_data_for_experiment_at_index(index)            # unpolarised
project.model_data_for_experiment_at_index(index, 'pp')      # one channel
project.model_data_for_model_at_index(i, q, resolution_function=dataset.resolution_function)
```

The same holds for Bayesian sampling: `Project.prepare_sample()` (or
`MultiFitter.for_experiments(...)` followed by `mcmc_sample()` without a
`DataGroup`) samples each dataset with its own resolution, and
`posterior_predictive_reflectivity(..., resolution_function=...)` draws
the band with it.

### What loading a dataset does to its model

The first dataset loaded onto a model sets the model's background (the
smallest measured value) and resolution (the dataset's `Pointwise`, or 5
% when the file has no resolution column). Later datasets loaded onto
the same model change nothing on it: they keep their own resolution and
are fitted with it. Edit `model.resolution_function` yourself when the
model should use something else, for instance a percentage for
simulations while the data keep their measured widths.

Project files store each dataset's resolution next to its arrays, so a
saved project fits exactly as before it was saved.

## One contrast from several files

A contrast is often measured as several curves, one per incident angle
or wavelength band, each with its own resolution. They can be combined
into a single experiment:

```python
index = project.load_experiment_from_files(['angle1.ort', 'angle2.ort', 'angle3.ort'])
project.append_to_experiment_at_index(index, 'angle4.ort')
```

The points are concatenated and sorted by $q$ and every point keeps the
width it was measured with; overlapping $q$ ranges with different widths
are honoured because a `Pointwise` is exact at its stored points. A
polarised experiment and a file holding several datasets cannot be
merged this way.

Files without a resolution column are handled as follows:

- **Mixed with files that have one.** Their points get the model's
  resolution when that is a `PercentageFwhm`, and the default 5 % FWHM
  otherwise, and a warning says so. The second case is the common one:
  after the first measured file the model usually holds that file's
  `Pointwise`, so a three-column file appended later is smeared with 5
  %, not with an extrapolation of the measured widths. Set the merged
  experiment's `resolution_function` yourself if that is not what you
  want.
- **None of the files has one.** The merged experiment has no resolution
  of its own (`None`) and follows the model's, like a single
  three-column file. No warning is emitted.

For scripts working on datasets directly,
`easyreflectometry.data.merge_datasets` does the same without a project.

## Polarised experiments

Each spin channel of a `PolarizedDataSet` is a `DataSet1D` and keeps the
resolution of its own file. The fit and the per-channel model curves use
it; the model's resolution follows the first channel only for
simulations and the GUI's resolution field. An earlier release applied
the first channel's resolution to every channel.

## Getting an unsmeared curve

Pass a zero-width resolution to one calculation instead of changing the
model:

```python
sharp = project.model_data_for_model_at_index(0, q, resolution_function=PercentageFwhm(0))
sharp = project.sample_data_for_model_at_index(0, q)   # the same
```

The model's resolution is calculator state that a fit running in another
thread reads, so it should not be swapped back and forth for a plot.
