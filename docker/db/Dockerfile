FROM postgres:11.4

ENV POSTGRES_INITDB_ARGS="-A trust"

COPY ./entrypoint docker-entrypoint-initdb.d/
