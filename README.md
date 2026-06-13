# Invoke Lint

[![Test](https://github.com/yukihiko-shinoda/invoke-lint/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/invoke-lint/actions?query=workflow%3ATest)
[![CodeQL](https://github.com/yukihiko-shinoda/invoke-lint/workflows/CodeQL/badge.svg)](https://github.com/yukihiko-shinoda/invoke-lint/actions?query=workflow%3ACodeQL)
[![Code Coverage](https://qlty.sh/gh/yukihiko-shinoda/projects/invoke-lint/coverage.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/invoke-lint)
[![Maintainability](https://qlty.sh/gh/yukihiko-shinoda/projects/invoke-lint/maintainability.svg)](https://qlty.sh/gh/yukihiko-shinoda/projects/invoke-lint)
[![Dependabot](https://flat.badgen.net/github/dependabot/yukihiko-shinoda/invoke-lint?icon=dependabot)](https://github.com/yukihiko-shinoda/invoke-lint/security/dependabot)
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

- [Xenon] (Optional)
- [radon] (Optional)
- [Ruff]
- [Bandit]
- [Cohesion]
- [dodgy]
- [Flake8]
- [pydocstyle] (Optional)
- [mypy]
- [Pylint]
- [Semgrep]

Formatters:

- [docformatter]
- [Ruff]
- [autoflake] (If you want to use it instead of Ruff)
- [isort] (If you want to use it instead of Ruff)
- [Black] (If you want to use it instead of Ruff)

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
2. [Ruff] format
3. [Ruff] check --fix

Optionally, you can use [autoflake], [isort], and [Black] instead of [Ruff] format by `inv style --no-ruff`:

1. [docformatter]
2. [autoflake]
3. [isort]
4. [Black]
5. [Ruff] check --fix

- `inv style --check` can only check.
- `inv style --ruff` can skip `ruff check --fix`.

### `inv lint`

Runs following fast linters at once:

1. [Xenon] (Optional)
2. [Ruff]
3. [Bandit]
4. [dodgy]
5. [Flake8]
6. [pydocstyle] (Optional)

The format task ([described later](#inv-style)) also run before running above linters. You can skip them by `--skip-format` option. Use `--xenon` to enable Xenon, and `--pydocstyle` to enable pydocstyle.

### `inv lint.deep`

Runs following slow but detailed linters at once:

1. [mypy]
2. [Pylint]
3. [Semgrep]

### `inv lint.radon`

Reports [radon] both code complexity and maintainability index. (Requires [radon] to be installed)

### `inv test`

Runs fast tests (which is not marked `@pytest.mark.slow`) by [pytest].

See:

- [How to mark test functions with attributes — pytest documentation]
- [Working with custom markers — pytest documentation]

### `inv test.all`

Runs all tests including those marked `@pytest.mark.slow` by [pytest].

### `inv test.cov`

Runs all tests and report those coverage by [pytest] and [Coverage.py].

It also can dump the coverage as XML or HTML format.

### `inv dist`

Builds source and wheel packages into `dist/` directory by [build].  
(Currently, not support in Windows)

See:

- [Building and Distributing Packages with Setuptools - setuptools latest documentation]
- [Package Discovery and Namespace Packages - setuptools latest documentation]

## Quickstart

### 1. Install

We should use [uv] or one of the [dependency management tools] to resolve dependencies of many dev tools.

For example, in case when we use the [uv], then, `pyproject.toml` is like below:

```toml
[dependency-groups]
dev = [
    "autoflake",
    "bandit; python_version >= '3.7'",
    # If you want to use not Ruff but Black for formatting
    "black; python_version >= '3.7'",
    "build",
    "bump-my-version",
    "cohesion",
    # The coverage==3.5.3 is difficult to analyze its dependencies by dependencies management tool,
    # so we should avoid 3.5.3 or lower.
    # - Command: "pipenv install --skip-lock" fails 
    #   since it tries to parse legacy package metadata and raise InstallError
    #   · Issue #5595 · pypa/pipenv
    #   https://github.com/pypa/pipenv/issues/5595
    "coverage>=3.5.4",
    # The dlint less than 0.14.0 limits max version of flake8.
    # - dlint/requirements.txt at 0.13.0 · dlint-py/dlint
    #   https://github.com/dlint-py/dlint/blob/0.13.0/requirements.txt#L1
    "dlint>=0.14.0",
    # To the docformatter load pyproject.toml settings:
    # docformatter < 1.7.8 depends on untokenize==0.1.1, whose setup.py uses ast.Constant.s removed in Python 3.14.
    # docformatter >= 1.7.8 dropped untokenize but requires Python >= 3.10.
    "docformatter[tomli]>=1.7.8; python_version >= '3.10' and python_version < '3.11'",
    "docformatter>=1.7.8; python_version >= '3.11'",
    "dodgy",
    # The hacking depends flake8 ~=6.1.0 or ~=5.0.1 or ~=4.0.1.
    # We should avoid the versions that is not compatible with the hacking,
    # considering the speed of dependency calculation process
    "flake8!=6.0.0,!=5.0.0,>=4.0.1; python_version >= '3.6'",
    # To replace E501 in pycodestyle with B950 in flake8-bugbear:
    # - Using Black with other tools - Black 25.1.0 documentation
    #   https://black.readthedocs.io/en/stable/guides/using_black_with_other_tools.html#bugbear
    "flake8-bugbear",
    # To use flake8 --radon-show-closures
    "flake8-polyfill",
    # To use pyproject.toml for Flake8 configuration
    "Flake8-pyproject",
    # Latest hacking depends on legacy version of flake8, and legacy hacking doesn't narrow flake8 version.
    # When unpin hacking, it has possibility to install too legacy version of hacking.
    "hacking>=5.0.0; python_version >= '3.8'",
    "invokelint; python_version >= '3.7'",
    # If you want to use not Ruff but isort for formatting
    "isort",
    "mypy",
    # If you want to use
    "pydocstyle; python_version >= '3.6'",
    "pylint",
    "pytest",
    # If you want to use Radon for code complexity and maintainability index checking
    # Note that the version should be less than 6.0.0 because of the issue of Radon with pytest log format.
    # - Radon can't run when use pytest log fornat: `$()d` · Issue #251 · rubik/radon
    #   https://github.com/rubik/radon/issues/251
    "radon<6.0.0",
    "ruff; python_version >= '3.7'",
    # If we simply lock as "semgrep; python_version >= '3.9' or python_version>='3.6' and platform_system=='Linux'",
    # the semgrep 1.121.0 is installed in Python 3.14 and cause following error:
    #     File "/root/.local/share/uv/python/cpython-3.14.5-linux-aarch64-gnu/lib/python3.14/importlib/__init__.py", line 88, in import_module
    #       return _bootstrap._gcd_import(name[level:], package, level)
    #              ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #   TypeError: Metaclasses with custom tp_new are not supported.
    "semgrep; python_version >= '3.9' and python_version < '3.10' or python_version>='3.6' and platform_system=='Linux'",
    "semgrep>=1.122.0;python_version >= '3.10'",
    # To resolve type checking for `from invoke import Collection` in tasks.py
    "types-invoke",
    # If you want to use not Ruff but Xenon for complexity checking
    "xenon",
]
```

then:

```console
uv sync
source .venv/bin/activate
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

### 5. Set up CI/CD workflows

This package provides reusable GitHub Actions workflows. Create the following files in `.github/workflows/`:

**`.github/workflows/test.yml`** — runs tests and linters on push/PR to `main`:

```yaml
name: Test
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
permissions:
  contents: read
jobs:
  call-workflow-test:
    uses: yukihiko-shinoda/reusable-workflow-invoke-lint-test/.github/workflows/workflow.yml@v1
    with:
      support-python-versions: "[ '3.14', '3.13', '3.12', '3.11', '3.10' ]"
  call-workflow-lint:
    uses: yukihiko-shinoda/reusable-workflow-invoke-lint-lint/.github/workflows/workflow.yml@v1
```

**`.github/workflows/qlty.yml`** — uploads coverage to [Qlty] on push to `main`:

```yaml
on:
  push:
    branches:
      - main
# For OIDC token exchange with Qlty:
# - Configuring OpenID Connect in cloud providers - GitHub Docs
#   https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers#adding-permissions-settings
permissions:
  contents: read
  id-token: write
jobs:
  analyze:
    uses: yukihiko-shinoda/reusable-workflow-invoke-lint-qlty/.github/workflows/workflow.yml@v1
    permissions:
      contents: read
      id-token: write
```

**`.github/workflows/deploy.yml`** — publishes to PyPI on version tag push (`v*.*.*`):

```yaml
on:
  push:
    tags:
      - 'v[0-9]+.[0-9]+.[0-9]+'
permissions:
  contents: read
jobs:
  call-workflow:
    uses: yukihiko-shinoda/reusable-workflow-invoke-lint-deploy/.github/workflows/workflow.yml@v1
    secrets:
      pypi_password: ${{ secrets.pypi_password }}
```

Check the respective repositories for the latest commit hashes if you want to use them for lock:

- [reusable-workflow-invoke-lint-test]
- [reusable-workflow-invoke-lint-lint]
- [reusable-workflow-invoke-lint-qlty]
- [reusable-workflow-invoke-lint-deploy]

<!-- markdownlint-disable no-trailing-punctuation -->
## How do I...
<!-- markdownlint-enable no-trailing-punctuation -->

### Suppress [`B101: assert_used`] in Bandit and [`assert (S101)`] in Ruff only in test files?

Set below configuration in `pyproject.toml`:

```toml
[tool.bandit.assert_used]
skips = ["tests/*"]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]
```

Note that invoke-lint executes [Bandit] with option `--configfile=pyproject.toml`, so upper configuration will be applied.

See: [Configuration — Bandit documentation]

## Credits

This package was created with [Cookiecutter] and the [yukihiko-shinoda/cookiecutter-pypackage] project template.

[Cookiecutter]: https://github.com/audreyr/cookiecutter
[yukihiko-shinoda/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage
[Invoke]: https://pypi.org/project/invoke/
[dependency management tools]: https://packaging.python.org/en/latest/tutorials/managing-dependencies/
[uv]: https://pypi.org/project/uv/
[Ruff]: https://pypi.org/project/ruff/
[Bandit]: https://pypi.org/project/bandit/
[Cohesion]: https://pypi.org/project/cohesion/
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
[`B101: assert_used`]: https://bandit.readthedocs.io/en/latest/plugins/b101_assert_used.html
[`assert (S101)`]: https://docs.astral.sh/ruff/rules/assert/
[Configuration — Bandit documentation]: https://bandit.readthedocs.io/en/latest/config.html#scanning-behavior
[Qlty]: https://qlty.sh
[reusable-workflow-invoke-lint-test]: https://github.com/yukihiko-shinoda/reusable-workflow-invoke-lint-test
[reusable-workflow-invoke-lint-lint]: https://github.com/yukihiko-shinoda/reusable-workflow-invoke-lint-lint
[reusable-workflow-invoke-lint-qlty]: https://github.com/yukihiko-shinoda/reusable-workflow-invoke-lint-qlty
[reusable-workflow-invoke-lint-deploy]: https://github.com/yukihiko-shinoda/reusable-workflow-invoke-lint-deploy
