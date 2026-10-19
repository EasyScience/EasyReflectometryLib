# Reference costs for the convergence tests

Cost = classical χ² = Σ (y − R)² / σ² over the points with σ² > 0, at
the end of a fit. The tests assert a run ends within a tolerance of the
reference, never parameter values (weakly identified parameters can
differ with an equally good curve).

Environment: `pixi run python` — Python 3.13.13, easyscience 2.5.1,
lmfit 1.3.4, scipy 1.17.1, bumps 1.0.4, refnx 0.1.63, 2026-10-08.

Models, bounds and starts are those in `test_convergence.py`
(`film_model`), which follow `tests/test_fitting.py::test_fitting` for
`example.ort` and refnx's own `test_reflect.py` setup for `e361r.txt`.

| Fixture       | Resolution                | Reference | How it was obtained                                                                                                                       | Cross-check                                                                                                  |
| ------------- | ------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `example.ort` | model, 0.02 % FWHM        | 1262.352  | LMFit differential evolution, `seed=1`, `polish=True`, notebook path                                                                      | refnx 0.1.63 `CurveFitter('differential_evolution', seed=1)`, same structure and bounds, linear χ²: 1263.172 |
| `example.ort` | its own sQz (`Pointwise`) | 1008.59   | `LMFit_leastsq` and `LMFit_scipy_least_squares` from the test start agree to 0.01; a DE run stopped on its 4000-evaluation budget at 1555 | none                                                                                                         |
| `e361r.txt`   | model, 5 % FWHM           | 380.506   | LMFit differential evolution, `seed=1`, `polish=True`, notebook path                                                                      | refnx as above: 381.172                                                                                      |

refnx and easyreflectometry use different reflectivity kernels, so their
costs differ by 0.1–0.2 %; refnx is a sanity check, not the reference.
