# Invoke Lint

[![Test](https://github.com/yukihiko-shinoda/invoke-lint/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/invoke-lint/actions?query=workflow%3ATest)
[![CodeQL](https://github.com/yukihiko-shinoda/invoke-lint/workflows/CodeQL/badge.svg)](https://github.com/yukihiko-shinoda/invoke-lint/actions?query=workflow%3ACodeQL)
[![Test Coverage](https://api.codeclimate.com/v1/badges/935364d296051fb926c8/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/invoke-lint/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/935364d296051fb926c8/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/invoke-lint/maintainability)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/yukihiko-shinoda/invoke-lint)](https://codeclimate.com/github/yukihiko-shinoda/invoke-lint)
[![Python versions](https://img.shields.io/pypi/pyversions/invokelint.svg)](https://pypi.org/project/invokelint)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Finvoke-lint)](http://twitter.com/share?text=Invoke%20Lint&url=https://pypi.org/project/invokelint/&hashtags=python)

Invokes Python dev tools at once.

## Attention

- The development status of this package is Beta now. It may not be able to keep backward compatibility. Be careful to use, especially for CI.
- Currently, each commands require to run in project home directory.

## Advantage

1. Covers major development tools and they are optional to install
1. Quick response for developer, slow but detail for CI
1. Available to place commands into your selected namespace

### 1. Covers major development tools and they are optional to install

You can choose which dev tool you'll install, this package doesn't force to install each of dev tools. It helps you to avoid conflicts or breaking your project's dependencies.

Supporting tools:

Linters:

- [Xenon]
- [Ruff]
- [Bandit]
- [dodgy]
- [Flake8]
- [pydocstyle]
- [mypy]
- [Pylint]
- [Semgrep]

Formatters:

- [docformatter]
- [isort]
- [autoflake]
- [Black]

For test and coverage:

- [pytest]
- [Coverage.py]

Package build:

- [build]

### 2. Quick response for developer, slow but detailed for CI

The commands for each kind of tasks are designed as unified into 2 main commands:

- For developer: Runs only quick responsive dev tools at once
- For CI (or final check): Runs slow but detailed responsive tools at once

### 3. Available to place commands into your selected namespace

This doesn't pollute your comfortable namespaces of command line tools. Thanks to [Invoke], you can place commands into your selected namespace. (See: [Quickstart](#quickstart))

## Representative commands

(Note that the namespaces of following commands can be changed as you like. See: [Quickstart](#quickstart))

### `inv style`

Formats code by following tools at once:

1. [docformatter]
2. [isort]
3. [autoflake]
4. [Black]
5. [Ruff]

- `inv style --check` can only check.
- `inv style --ruff` can leave Ruff warnings.

### `inv lint`

Runs following fast lints at once:

1. [Xenon]
2. [Ruff]
3. [Bandit]
4. [dodgy]
5. [Flake8]
6. [pydocstyle]

The format task ([described later](#inv-style)) also run before run above lints. You can skip them by `--skip-format` option.

### `inv lint.deep`

Runs following slow but detailed lints at once:

1. [mypy]
2. [Pylint]
3. [Semgrep]

### `inv radon`

Reports [radon] both code complexity and maintainability index.

### `inv test`

Runs fast tests (which is not marked `@pytest.mark.slow`) by [pytest].

See:

- [How to mark test functions with attributes — pytest documentation]
- [Working with custom markers — pytest documentation]

### `inv test.cov`

Runs all tests and report coverage by [pytest] and [Coverage.py].

It also can dump coverage as XML or HTML format.

### `inv dist`

Builds source and wheel packages into `dist/` directory by [build].  
(Currently, not support in Windows)

See:

- [Building and Distributing Packages with Setuptools - setuptools latest documentation]
- [Package Discovery and Namespace Packages - setuptools latest documentation]

## Quickstart

### 1. Install

It's better to use one of [dependency management tools] to resolve dependencies of many dev tools.

For example, in case when use [Pipenv], `Pipfile`:

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[dev-packages]
autoflake = "*"
bandit = {version = "*", markers="python_version >= '3.7'"}
black = {version = "*", markers="python_version >= '3.7'"}
build = "*"
# Hotfix for Pipenv's Bug:
# - Pipenv should prioritize more cross-platform sys_platform condition between packages when lock
#   · Issue #4101 · pypa/pipenv
#   https://github.com/pypa/pipenv/issues/4101
colorama = "*"
coverage = ">=3.5.4"
# The dlint less than 0.14.0 limits max version of flake8.
dlint = ">=0.14.0"
docformatter = {extras = ["tomli"], version = "*"}
dodgy = "*"
# Since Pipenv can't lock for too much combinations to attempt lock:
# pip._vendor.resolvelib.resolvers.ResolutionTooDeep: 2000000
# The hacking depends flake8 ~=5.0.1 or ~=4.0.1.
flake8 = {version = "<=6.0.0>=5.0.1,==4.0.1", markers="python_version >= '3.6'"}
# To use flake8 --radon-show-closures
flake8-polyfill = "*"
# Latest hacking depends on legacy version of flake8, and legacy hacking doesn't narrow flake8 version.
# When unpin hacking, it has possibility to install too legacy version of hacking.
hacking = {version = ">=5.0.0", markers="python_version >= '3.8'"}
invokelint = {version = "*", markers="python_version >= '3.7'"}
isort = "*"
mypy = "*"
pydocstyle = {version = "*", markers="python_version >= '3.6'"}
pylint = "*"
pytest = "*"
radon = "*"
ruff = {version = "*", markers="python_version >= '3.7'"}
semgrep = {version = "*", markers="python_version >= '3.6'"}
tomli = {version = "*", markers="python_version >= '3.6'"}
xenon = "*"
```

then:

```console
pipenv install --dev
pipenv shell
```

### 2. Implement

Create `tasks.py` in project directory:

```python
"""Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
from invoke import Collection

from invokelint import dist, lint, path, style, test

ns = Collection()
ns.add_collection(dist)
ns.add_collection(lint)
ns.add_collection(path)
ns.add_collection(style)
ns.add_collection(test)
```

Commands may be explicitly place with a different name than they were originally given via a name kwarg (or the 2nd regular arg):

```python
ns.add_collection(lint, 'namespace-you-wish')
```

See: [Constructing namespaces — Invoke documentation]

### 3. Check installation

```console
inv --list
```

### 4. Setup target package

This package reuses `setuptools` settings for package discovery for linting, formatting, and measuring coverage. You can check which package are discovered by `setuptools` and your project's settings, by following command:

```console
$ inv path
Setuptools detected packages: ['invokelint', 'invokelint.path']
Root packages: ['invokelint']
Setuptools detected Python modules: ['setup', 'tasks']
Existing test packages: ['tests']
Python file or directories to lint: ['invokelint', 'setup.py', 'tasks.py', 'tests']
Python file or directories to lint excluding test packages: ['invokelint', 'setup.py', 'tasks.py']
```

If result is not your expected, follow official documentation of `setuptools` to configure `pyproject.toml` (recommended), `setup.cfg`, or `setup.py`.

See: [Package Discovery and Namespace Packages - setuptools latest documentation]

## Credits

This package was created with [Cookiecutter] and the [yukihiko-shinoda/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[yukihiko-shinoda/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[Invoke]: https://pypi.org/project/invoke/
[dependency management tools]: https://packaging.python.org/en/latest/tutorials/managing-dependencies/
[Pipenv]: https://pypi.org/project/pipenv/
[Ruff]: https://pypi.org/project/ruff/
[Bandit]: https://pypi.org/project/bandit/
[dodgy]: https://pypi.org/project/dodgy/
[Flake8]: https://pypi.org/project/flake8/
[pydocstyle]: https://pypi.org/project/pydocstyle/
[Xenon]: https://pypi.org/project/xenon/
[Pylint]: https://pypi.org/project/pylint/
[mypy]: https://pypi.org/project/mypy/
[Semgrep]: https://pypi.org/project/semgrep/
[radon]: https://pypi.org/project/radon/
[docformatter]: https://pypi.org/project/docformatter/
[isort]: https://pypi.org/project/isort/
[autoflake]: https://pypi.org/project/autoflake/
[Black]: https://pypi.org/project/black/
[pytest]: https://pypi.org/project/pytest/
[How to mark test functions with attributes — pytest documentation]: https://docs.pytest.org/en/latest/how-to/mark.html
[Working with custom markers — pytest documentation]: https://docs.pytest.org/en/latest/example/markers.html
[Coverage.py]: https://pypi.org/project/coverage/
[build]: https://pypi.org/project/build/
[Building and Distributing Packages with Setuptools - setuptools latest documentation]: https://setuptools.pypa.io/en/latest/setuptools.html
[Package Discovery and Namespace Packages - setuptools latest documentation]: https://setuptools.pypa.io/en/latest/userguide/package_discovery.html
[Constructing namespaces — Invoke documentation]: https://docs.pyinvoke.org/en/latest/concepts/namespaces.html#nesting-collections
