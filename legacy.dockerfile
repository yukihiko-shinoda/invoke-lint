FROM python:3.7.16-slim-bullseye
# setuptools 65.3.0 can't lock package defined its dependencies by pyproject.toml
RUN pip install --no-cache-dir --upgrade pip==23.3.1 setuptools==68.0.0
# see: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /workspace
COPY . /workspace
RUN pip --no-cache-dir install pipenv==2023.10.03 \
 && pipenv install --dev
ENTRYPOINT [ "pipenv", "run" ]
CMD ["pytest"]
