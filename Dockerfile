# syntax=docker/dockerfile:experimental

FROM python:3.8.5

ARG PROJECT_NAME
# REPO_SETUP: These next two arguments may be removed if your project will not install packages from our internal PyPI
# repository
ARG PYPI_USER
ARG PYPI_PASSWORD

COPY requirements.txt /$PROJECT_NAME/requirements.txt
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /$PROJECT_NAME/requirements.txt

COPY . /$PROJECT_NAME

WORKDIR /$PROJECT_NAME
