FROM python:3.11-slim

RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.in-project true

WORKDIR /app
COPY . .

RUN poetry install

ENV PATH .venv/bin:$PATH
ENV PYTHONUNBUFFERD on

CMD uvicorn main:app --host 0.0.0.0 --port 8080
