FROM python:3.7.17-slim-bullseye
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --no-cache-dir --upgrade pip==24.0 setuptools==68.0.0
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
WORKDIR /workspace
COPY pyproject.toml /workspace
RUN pip install --no-cache-dir --ignore-requires-python uv==0.7.8 && uv sync
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["inv", "test.coverage"]
