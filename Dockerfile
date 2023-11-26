FROM python:3.12.0-slim-bookworm
# FROM python:3.7.16-slim-bullseye
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --no-cache-dir --upgrade pip==23.3.1 setuptools==69.0.2
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /workspace
COPY . /workspace
RUN pip --no-cache-dir install pipenv==2023.11.15 \
 && pipenv install --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
