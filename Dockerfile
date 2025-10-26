FROM futureys/claude-code-python-development:20251026170000
# gcc: Dependency of semgrep (v1.140.0) which depends on `ruamel-yaml-clib`:
# - command 'cc' failed: No such file or directory
# - assert.h: No such file or directory
RUN apt-get update && apt-get install --no-install-recommends -y \
 build-essential/stable \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml /workspace/
# - Using uv in Docker | uv
#   https://docs.astral.sh/uv/guides/integration/docker/#caching
RUN --mount=type=cache,target=/root/.cache/uv \
# Reason: The dependency of docformatter: untokenize does not support Python 3.14 yet.
# - Installation failing with Python 3.14 · Issue #4 · myint/untokenize
#   https://github.com/myint/untokenize/issues/4
# And the uv can't lock even if we limit the Python version for docformatter in pyproject.toml:
# # uv sync
#   × Failed to build `untokenize==0.1.1`
#   ├─▶ The build backend returned an error
#   ╰─▶ Call to `setuptools.build_meta:__legacy__.build_wheel` failed (exit status: 1)
# 
#       [stderr]
#       Traceback (most recent call last):
#         File "<string>", line 14, in <module>
#           requires = get_requires_for_build({})
#         File "/root/.cache/uv/builds-v0/.tmpLGGZWk/lib/python3.14/site-packages/setuptools/build_meta.py", line 331, in get_requires_for_build_wheel
#           return self._get_build_requires(config_settings, requirements=[])
#                  ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#         File "/root/.cache/uv/builds-v0/.tmpLGGZWk/lib/python3.14/site-packages/setuptools/build_meta.py", line 301, in _get_build_requires
#           self.run_setup()
#           ~~~~~~~~~~~~~~^^
#         File "/root/.cache/uv/builds-v0/.tmpLGGZWk/lib/python3.14/site-packages/setuptools/build_meta.py", line 512, in run_setup
#           super().run_setup(setup_script=setup_script)
#           ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
#         File "/root/.cache/uv/builds-v0/.tmpLGGZWk/lib/python3.14/site-packages/setuptools/build_meta.py", line 317, in run_setup
#           exec(code, locals())
#           ~~~~^^^^^^^^^^^^^^^^
#         File "<string>", line 19, in <module>
#           json.dump(requires, fp)
#                              ^^^^
#         File "<string>", line 14, in version
#       AttributeError: 'Constant' object has no attribute 's'
# 
#       hint: This usually indicates a problem with the package or the build environment.
#   help: `untokenize` (v0.1.1) was included because `invokelint:dev` (v0.14.0) depends on `docformatter` (v1.7.7) which depends on `untokenize>=0.1.1, <0.2.0`
    uv sync --python 3.13
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["invoke", "test.coverage"]
