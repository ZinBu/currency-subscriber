FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONPATH="/app/src:${PYTHONPATH}"

RUN pip install --upgrade pip && pip install --upgrade setuptools && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --ignore-pipfile

COPY src/ .

EXPOSE 80

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
