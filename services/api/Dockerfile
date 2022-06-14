FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED=1
WORKDIR /opt/
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false --local
COPY poetry.lock pyproject.toml /opt/
RUN poetry install -n
COPY . /opt/
