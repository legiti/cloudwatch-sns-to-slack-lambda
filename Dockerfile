# syntax=docker/dockerfile:experimental

# TODO delete this file?

FROM python:3.10.4

ARG PROJECT_NAME

COPY requirements.txt /$PROJECT_NAME/requirements.txt
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /$PROJECT_NAME/requirements.txt

COPY . /$PROJECT_NAME

WORKDIR /$PROJECT_NAME
