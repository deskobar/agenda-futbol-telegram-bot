FROM python:3.10.9

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==1.4.2"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "bot.py"]

