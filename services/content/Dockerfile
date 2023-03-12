FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

WORKDIR /opt/

RUN apt-get update && \
    apt-get install -y git openssh-client

RUN python -m pip install --upgrade pip

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml /opt/
RUN poetry install -n

COPY . /opt/
