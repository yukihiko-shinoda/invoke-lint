FROM python:3.13.3-slim-bookworm
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
WORKDIR /workspace
COPY pyproject.toml /workspace
RUN pip --no-cache-dir install uv==0.7.8 && uv sync
COPY . /workspace
ENTRYPOINT [ "uv", "run" ]
CMD ["inv", "test.coverage"]
