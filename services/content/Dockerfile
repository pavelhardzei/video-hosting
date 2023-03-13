FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    POETRY_HOME=/etc/poetry

WORKDIR /opt/

RUN apt-get update && \
    apt-get install -y git curl

RUN python -m pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN $POETRY_HOME/bin/poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /opt/
RUN $POETRY_HOME/bin/poetry install -n

COPY . /opt/
