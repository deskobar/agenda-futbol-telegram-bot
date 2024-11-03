FROM python:3.10.9-slim

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip && pip install "poetry==1.8.3"

COPY poetry.lock pyproject.toml ./

ENV POETRY_VIRTUALENVS_IN_PROJECT=true

RUN poetry install --no-root

COPY . .

# Create non-root user and set up directories
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser
RUN chown -R appuser:appuser /app

# Create a writable directory for Matplotlib's cache
RUN mkdir -p /app/.config/matplotlib && chown -R appuser:appuser /app/.config

# Set the MPLCONFIGDIR environment variable
ENV MPLCONFIGDIR=/app/.config/matplotlib

# Switch to non-root user
USER appuser

ENV PORT=8080
ENV HOME=/home/appuser

EXPOSE ${PORT}

CMD poetry run uvicorn api.app:app --host 0.0.0.0 --port $PORT
