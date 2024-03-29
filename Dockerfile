FROM python:3.12.2-slim-bookworm
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --no-cache-dir --upgrade pip==24.0 setuptools==69.2.0
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /workspace
COPY . /workspace
RUN pip --no-cache-dir install pipenv==2023.12.1 \
 && pipenv install --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
