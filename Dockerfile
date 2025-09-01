FROM node:24.4.1-bookworm-slim
WORKDIR /workspace
RUN npm install -g @anthropic-ai/claude-code@1.0.61
COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/
# The uv command also errors out when installing semgrep:
# - Getting semgrep-core in pipenv · Issue #2929 · semgrep/semgrep
#   https://github.com/semgrep/semgrep/issues/2929#issuecomment-818994969
ENV SEMGREP_SKIP_BIN=true
COPY pyproject.toml /workspace/
RUN uv sync
COPY . /workspace/
ENTRYPOINT [ "uv", "run", "--no-sync" ]
CMD ["invoke", "test.coverage"]