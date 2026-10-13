<p>
  <picture>
    <!-- light mode logo -->
    <source media='(prefers-color-scheme: light)' srcset='https://raw.githubusercontent.com/easyscience/assets-branding/refs/heads/master/easyreflectometry/logos/light.svg'>
    <!-- dark mode logo -->
    <source media='(prefers-color-scheme: dark)' srcset='https://raw.githubusercontent.com/easyscience/assets-branding/refs/heads/master/easyreflectometry/logos/dark.svg'>
    <!-- default logo == light mode logo -->
    <img src='https://raw.githubusercontent.com/easyscience/assets-branding/refs/heads/master/easyreflectometry/logos/light.svg' alt='EasyReflectometry'>
  </picture>
</p>

**EasyReflectometry** is a Python library for simulating reflectometry
profiles from layered sample models and refining their parameters
against experimental data.

It supports multiple contrasts and simultaneous fitting, polarised
reflectometry channels, Bayesian (MCMC) analysis, ORSO data and model
import/export, and a choice of calculation engines (refnx or refl1d).

<!-- HOME REPOSITORY SECTION -->

**EasyReflectometry** is built on the
[EasyScience framework](https://easyscience.org) and maintained by the
[European Spallation Source (ESS)](https://ess.eu).

## Installation

**EasyReflectometry** requires Python 3.11–3.13 and is available on
PyPI:

```bash
pip install easyreflectometry
```

The `dev` extra is only needed if you want to contribute to the library
or build the documentation. It adds the tooling for testing (pytest),
linting and formatting (ruff, pre-commit), building the docs (mkdocs)
and running the tutorial notebooks. To install it from PyPI:

```bash
pip install 'easyreflectometry[dev]'
```

See the
[Installation & Setup](https://easyscience.github.io/reflectometry-lib/latest/installation-and-setup)
guide for the recommended Pixi-based setup.

License:
[BSD 3-Clause](https://github.com/easyscience/reflectometry-lib/blob/master/LICENSE)

## Useful Links

### For Users

- 📖
  [Documentation](https://easyscience.github.io/reflectometry-lib/latest)
- 🚀
  [Getting Started](https://easyscience.github.io/reflectometry-lib/latest/installation-and-setup)
- 🧪
  [Tutorials](https://easyscience.github.io/reflectometry-lib/latest/tutorials)
- 💬
  [Get in Touch](https://easyscience.github.io/reflectometry-lib/latest/introduction/#get-in-touch)
- 🧾
  [Citation](https://easyscience.github.io/reflectometry-lib/latest/introduction/#citation)

### For Contributors

- 🧑‍💻 [Source Code](https://github.com/easyscience/reflectometry-lib)
- 🐞
  [Issue Tracker](https://github.com/easyscience/reflectometry-lib/issues)
- 💡
  [Discussions](https://github.com/easyscience/reflectometry-lib/discussions)
- 🤝
  [Contributing Guide](https://github.com/easyscience/reflectometry-lib/blob/master/CONTRIBUTING.md)
- 🛡
  [Code of Conduct](https://github.com/easyscience/.github/blob/master/CODE_OF_CONDUCT.md)
