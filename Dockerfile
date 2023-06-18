FROM python:3.10.9-slim-buster

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==1.4.2"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
