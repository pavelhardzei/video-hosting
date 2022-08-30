FROM python:3.8.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONBUFFERED=1

WORKDIR /opt/

RUN python -m pip install --upgrade pip

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml /opt/
RUN poetry install -n

COPY . /opt/
