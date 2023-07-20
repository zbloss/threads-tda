FROM python:3.10.5

ENV PYTHONUNBUFFERED=1

RUN pip install 'poetry==1.5.1'

RUN mkdir /code

COPY src /code/src

COPY poetry.lock pyproject.toml /code/

WORKDIR /code

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

CMD ["python", "src/run.py"]