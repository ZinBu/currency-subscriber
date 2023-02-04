FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN pip install --upgrade pip setuptools

COPY requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt --no-cache-dir

COPY . /app

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
